"""Page 6 – Model Comparison: metrics table, confusion matrices, feature importance, regression."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.utils import (
    apply_custom_css, get_plotly_layout, create_kpi_card,
    FEATURE_COLS, TARGET_COL, COLORS,
)
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data
from src.models import _SKLEARN_AVAILABLE, _SKLEARN_ERROR

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>🤖 Model Comparison</h1>", unsafe_allow_html=True)

if not _SKLEARN_AVAILABLE:
    st.error(
        "⚠️ **scikit-learn could not be loaded** on this system.\n\n"
        f"Error: `{_SKLEARN_ERROR}`\n\n"
        "**Fix:** Install Python via [Anaconda](https://www.anaconda.com/download) "
        "or ask your admin to whitelist the Python DLL path in Windows Application Control."
    )
    st.stop()

from src.models import (
    prepare_data, train_all_classifiers, train_regressor,
    evaluate_classifier, evaluate_regressor, get_feature_importance,
)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]


@st.cache_resource(show_spinner=False)
def _train_and_eval(_df: pd.DataFrame):
    data = prepare_data(_df, FEATURE_COLS, TARGET_COL)
    clfs = train_all_classifiers(data["X_train"], data["y_class_train"])
    reg = train_regressor(data["X_train"], data["y_score_train"])

    evals = {}
    best_name, best_acc = "", 0.0
    for name, clf in clfs.items():
        ev = evaluate_classifier(clf, data["X_test"], data["y_class_test"], data["label_encoder"])
        evals[name] = ev
        if ev["accuracy"] > best_acc:
            best_acc, best_name = ev["accuracy"], name

    reg_ev = evaluate_regressor(reg, data["X_test"], data["y_score_test"])
    return clfs, reg, evals, reg_ev, best_name, data


with st.spinner("Training & evaluating models…"):
    clfs, reg, evals, reg_ev, best_name, data_dict = _train_and_eval(df)

# ═══════════════════════ CLASSIFICATION ═══════════════════════════════════
st.markdown("### 📊 Classification Models")
st.info(
    "ℹ️ The best-performing model is determined by evaluation metrics on this "
    "dataset — **no model is assumed best in advance**."
)

rows = []
for name, ev in evals.items():
    rows.append({
        "Model": name,
        "Accuracy": f"{ev['accuracy']:.4f}",
        "Precision": f"{ev['precision']:.4f}",
        "Recall": f"{ev['recall']:.4f}",
        "F1-Score": f"{ev['f1']:.4f}",
        "★": "⭐" if name == best_name else "",
    })
metrics_df = pd.DataFrame(rows)

def _highlight(row):
    if row["Model"] == best_name:
        return [f"background-color:rgba(20,184,196,0.15);color:{COLORS['accent']};font-weight:700"] * len(row)
    return [""] * len(row)

st.dataframe(
    metrics_df.style.apply(_highlight, axis=1),
    use_container_width=True, hide_index=True,
)

# Bar chart
num_df = pd.DataFrame([
    {"Model": n, "Accuracy": e["accuracy"], "Precision": e["precision"],
     "Recall": e["recall"], "F1-Score": e["f1"]}
    for n, e in evals.items()
])
fig_bar = px.bar(num_df, x="Model", y=["Accuracy", "Precision", "Recall", "F1-Score"],
                 barmode="group", title="Classifier Metrics Comparison")
fig_bar.update_layout(**get_plotly_layout())
st.plotly_chart(fig_bar, use_container_width=True)

# ═══════════════════════ REGRESSION ═══════════════════════════════════════
st.markdown("---")
st.markdown("### 📈 Regression Model (Linear Regression)")
r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(create_kpi_card("MAE", f"{reg_ev['mae']:.2f}", "📏",
                                color=COLORS["warning"]), unsafe_allow_html=True)
with r2:
    st.markdown(create_kpi_card("RMSE", f"{reg_ev['rmse']:.2f}", "📐",
                                color=COLORS["danger"]), unsafe_allow_html=True)
with r3:
    st.markdown(create_kpi_card("R² Score", f"{reg_ev['r2']:.4f}", "🎯",
                                color=COLORS["success"]), unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### Actual vs Predicted")
    fig_ap = px.scatter(x=reg_ev["y_test"], y=reg_ev["y_pred"],
                        labels={"x": "Actual", "y": "Predicted"},
                        color_discrete_sequence=[COLORS["accent"]])
    mn, mx = float(min(reg_ev["y_test"])), float(max(reg_ev["y_test"]))
    fig_ap.add_trace(go.Scatter(x=[mn, mx], y=[mn, mx], mode="lines",
                                line=dict(dash="dash", color=COLORS["danger"]),
                                name="Ideal"))
    fig_ap.update_layout(**get_plotly_layout())
    st.plotly_chart(fig_ap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### Residuals")
    residuals = np.array(reg_ev["y_test"]) - np.array(reg_ev["y_pred"])
    fig_res = px.scatter(x=reg_ev["y_pred"], y=residuals,
                         labels={"x": "Predicted", "y": "Residual"},
                         color_discrete_sequence=[COLORS["secondary"]])
    fig_res.add_hline(y=0, line_dash="dash", line_color=COLORS["danger"])
    fig_res.update_layout(**get_plotly_layout())
    st.plotly_chart(fig_res, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════ CONFUSION MATRICES ══════════════════════════════
st.markdown("---")
st.markdown("### 🔢 Confusion Matrices")
cm_tabs = st.tabs(list(evals.keys()))
le = data_dict["label_encoder"]
for i, (name, ev) in enumerate(evals.items()):
    with cm_tabs[i]:
        cm = ev["confusion_matrix"]
        labels = le.classes_ if le is not None else [str(j) for j in range(len(cm))]
        fig_cm = px.imshow(cm, text_auto=True, x=labels, y=labels,
                           color_continuous_scale="Teal",
                           labels={"x": "Predicted", "y": "Actual"})
        fig_cm.update_layout(**get_plotly_layout(), title=f"{name}")
        st.plotly_chart(fig_cm, use_container_width=True)

# ═══════════════════════ FEATURE IMPORTANCE ══════════════════════════════
st.markdown("---")
st.markdown("### 🏆 Feature Importance")
sel_model = st.selectbox("Select model", list(clfs.keys()))
fi = get_feature_importance(clfs[sel_model], data_dict["feature_names"])
fig_fi = px.bar(fi, x="importance", y="feature", orientation="h",
                color="importance", color_continuous_scale="Teal",
                title=f"Feature Importance — {sel_model}")
fig_fi.update_layout(**get_plotly_layout(),
                     yaxis=dict(categoryorder="total ascending"),
                     coloraxis_showscale=False)
st.plotly_chart(fig_fi, use_container_width=True)

# ═══════════════════════ DETAILED REPORTS ════════════════════════════════
st.markdown("---")
st.markdown("### 📄 Classification Reports")
for name, ev in evals.items():
    with st.expander(f"📋 {name}"):
        cr = ev.get("classification_report", {})
        if isinstance(cr, dict):
            st.dataframe(pd.DataFrame(cr).T.round(3), use_container_width=True)
        else:
            st.text(str(cr))
