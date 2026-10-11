"""Page 5 – Prediction: input student features → predicted category + score."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.utils import (
    apply_custom_css, get_plotly_layout, create_kpi_card,
    FEATURE_COLS, TARGET_COL, COLORS, get_status_color,
)
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data
from src.models import _SKLEARN_AVAILABLE, _SKLEARN_ERROR

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>🎯 Performance Prediction</h1>", unsafe_allow_html=True)

if not _SKLEARN_AVAILABLE:
    st.error(
        "⚠️ **scikit-learn could not be loaded** on this system.\n\n"
        f"Error: `{_SKLEARN_ERROR}`\n\n"
        "**Fix:** Install Python via [Anaconda](https://www.anaconda.com/download) "
        "or ask your admin to whitelist the Python DLL path in Windows Application Control."
    )
    st.stop()

# Only import ML functions after confirming sklearn is available
from src.models import (
    prepare_data, train_all_classifiers, train_regressor,
    evaluate_classifier, predict_performance,
)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]


# ── Train models (cached) ───────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _train_models(_df: pd.DataFrame):
    """Train all classifiers + regressor; pick the best classifier."""
    data = prepare_data(_df, FEATURE_COLS, TARGET_COL)
    clfs = train_all_classifiers(data["X_train"], data["y_class_train"])
    reg = train_regressor(data["X_train"], data["y_score_train"])

    best_name, best_acc, best_clf = "", 0.0, None
    for name, clf in clfs.items():
        ev = evaluate_classifier(clf, data["X_test"], data["y_class_test"], data["label_encoder"])
        if ev["accuracy"] > best_acc:
            best_acc, best_name, best_clf = ev["accuracy"], name, clf

    return best_clf, reg, data["scaler"], data["label_encoder"], best_name, best_acc


with st.spinner("Training models (cached after first run)…"):
    best_clf, regressor, scaler, le, best_name, best_acc = _train_models(df)

st.markdown(
    f"<div class='glass-card' style='padding:12px 20px'>"
    f"<b>Best Classifier:</b> {best_name} &nbsp;|&nbsp; "
    f"<b>Accuracy:</b> {best_acc:.2%}</div>",
    unsafe_allow_html=True,
)

# ── Input Form ───────────────────────────────────────────────────────────
st.markdown("### 📝 Enter Student Data")
c1, c2 = st.columns(2)
with c1:
    att = st.slider("Attendance %", 0.0, 100.0, 75.0, step=1.0)
    int_m = st.slider("Internal Marks (out of 50)", 0.0, 50.0, 30.0, step=1.0)
    ass_m = st.slider("Assignment Marks (out of 25)", 0.0, 25.0, 15.0, step=1.0)
    prac_m = st.slider("Practical Marks (out of 25)", 0.0, 25.0, 15.0, step=1.0)
with c2:
    prev = st.slider("Previous Semester Result", 0.0, 100.0, 60.0, step=1.0)
    study = st.slider("Study Hours / Day", 0.0, 8.0, 4.0, step=0.5)
    part = st.slider("Participation Score (0-10)", 0.0, 10.0, 5.0, step=1.0)

predict_btn = st.button("🔮 Predict Performance", use_container_width=True)

if predict_btn:
    features = {
        "attendance_pct": att, "internal_marks": int_m,
        "assignment_marks": ass_m, "practical_marks": prac_m,
        "previous_sem_result": prev, "study_hours_per_day": study,
        "participation_score": part,
    }
    result = predict_performance(features, best_clf, regressor, scaler, FEATURE_COLS, le)
    cat = result["predicted_category"]
    score = result["predicted_score"]
    probs = result["probabilities"]
    color = get_status_color(cat)

    st.markdown("---")
    st.markdown("### 📊 Prediction Results")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(
            f"""<div class='glass-card' style='text-align:center'>
                <p style='color:{COLORS["text_secondary"]};font-size:1rem'>Predicted Category</p>
                <h1 style='color:{color};margin:8px 0'>{cat}</h1>
                <p style='color:{COLORS["text_secondary"]};font-size:1rem'>Predicted Score</p>
                <h2 style='color:{color};margin:8px 0'>{score:.1f}</h2>
            </div>""",
            unsafe_allow_html=True,
        )
        if cat == "Low":
            st.error("⚠️ **Recommendation:** Focus on improving attendance and daily study hours. "
                     "Seek additional support for weaker subjects.")
        elif cat == "Average":
            st.warning("💡 **Recommendation:** Target specific weak areas. Consistent practice "
                       "and active participation can push you into the High category.")
        else:
            st.success("🎉 **Excellent!** Keep maintaining your study habits and engagement. "
                       "Consider mentoring peers to reinforce your understanding.")

    with r2:
        if probs:
            prob_df = pd.DataFrame([
                {"Category": k, "Probability": v} for k, v in probs.items()
            ])
            fig = px.bar(prob_df, x="Probability", y="Category", orientation="h",
                         color="Category",
                         color_discrete_map={"Low": COLORS["danger"],
                                             "Average": COLORS["warning"],
                                             "High": COLORS["success"]},
                         text=prob_df["Probability"].apply(lambda x: f"{x:.1%}"))
            fig.update_layout(**get_plotly_layout(), showlegend=False,
                              title="Confidence / Probability",
                              xaxis=dict(range=[0, 1], tickformat=".0%"))
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

    # ── What-If Analysis ─────────────────────────────────────────────────
    st.markdown("### 🔄 What-If Analysis")
    st.caption("How much would the predicted score change if you improved one area?")
    improvements = [
        ("attendance_pct", "Attendance +10%", min(100, att + 10)),
        ("study_hours_per_day", "Study Hours +1 hr", min(8, study + 1)),
        ("participation_score", "Participation +2", min(10, part + 2)),
        ("internal_marks", "Internal Marks +5", min(50, int_m + 5)),
    ]
    wi_cols = st.columns(len(improvements))
    for i, (col, label, new_val) in enumerate(improvements):
        mod = features.copy()
        mod[col] = new_val
        res2 = predict_performance(mod, best_clf, regressor, scaler, FEATURE_COLS, le)
        delta = res2["predicted_score"] - score
        with wi_cols[i]:
            st.markdown(
                create_kpi_card(label, f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}",
                                "📈" if delta >= 0 else "📉",
                                color=COLORS["success"] if delta >= 0 else COLORS["danger"]),
                unsafe_allow_html=True,
            )
