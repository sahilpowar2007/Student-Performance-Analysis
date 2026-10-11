"""Page 2 – Exploratory Data Analysis: distributions, correlations, scatter, box-plots, rankings."""

import streamlit as st
import plotly.express as px

from src.utils import (
    apply_custom_css, get_plotly_layout,
    FEATURE_COLS, SUBJECTS, TARGET_COL, SUBJECT_NAMES, COLORS,
)
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data, get_preprocessing_report
from src.eda import get_summary_statistics, get_correlation_matrix

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>🔍 Exploratory Data Analysis</h1>", unsafe_allow_html=True)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]
original_df = st.session_state["data"]

# ── Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distributions", "🧮 Correlations", "📈 Scatter Analysis",
    "📚 Subject Box-plots", "🏆 Student Rankings",
])

# ── Tab 1: Distribution ─────────────────────────────────────────────────
with tab1:
    cols = [c for c in SUBJECTS + [TARGET_COL] + FEATURE_COLS if c in df.columns]
    sel = st.selectbox("Column to visualise", cols,
                       format_func=lambda c: SUBJECT_NAMES.get(c, c.replace("_", " ").title()))
    fig = px.histogram(df, x=sel, marginal="box",
                       color_discrete_sequence=[COLORS["accent"]])
    fig.add_vline(x=df[sel].mean(), line_dash="dash",
                  line_color=COLORS["warning"], annotation_text="Mean")
    fig.add_vline(x=df[sel].median(), line_dash="dot",
                  line_color=COLORS["success"], annotation_text="Median")
    fig.update_layout(**get_plotly_layout(), xaxis_title=sel.replace("_", " ").title())
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Dashed = Mean, Dotted = Median.")

# ── Tab 2: Correlation ──────────────────────────────────────────────────
with tab2:
    st.markdown("### Correlation Heatmap")
    corr_cols = [c for c in FEATURE_COLS + SUBJECTS + [TARGET_COL] if c in df.columns]
    corr = get_correlation_matrix(df, corr_cols)
    # Prettify axis labels
    rename = {c: SUBJECT_NAMES.get(c, c.replace("_", " ").title()) for c in corr.columns}
    corr = corr.rename(index=rename, columns=rename)
    fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(**get_plotly_layout())
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Pearson coefficients – values near ±1 indicate strong linear relationships.")

# ── Tab 3: Scatter Analysis ─────────────────────────────────────────────
with tab3:
    cat_col = "performance_category" if "performance_category" in df.columns else None
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Attendance vs Final Score")
        fig1 = px.scatter(df, x="attendance_pct", y=TARGET_COL, color=cat_col,
                          trendline="ols",
                          color_discrete_map={"Low": COLORS["danger"],
                                              "Average": COLORS["warning"],
                                              "High": COLORS["success"]})
        fig1.update_layout(**get_plotly_layout())
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.markdown("### Study Hours vs Final Score")
        fig2 = px.scatter(df, x="study_hours_per_day", y=TARGET_COL, color=cat_col,
                          trendline="ols",
                          color_discrete_map={"Low": COLORS["danger"],
                                              "Average": COLORS["warning"],
                                              "High": COLORS["success"]})
        fig2.update_layout(**get_plotly_layout())
        st.plotly_chart(fig2, use_container_width=True)

# ── Tab 4: Subject Box-plots ────────────────────────────────────────────
with tab4:
    st.markdown("### Subject-wise Score Distributions")
    avail = [s for s in SUBJECTS if s in df.columns]
    if avail:
        melted = df.melt(value_vars=avail, var_name="Subject", value_name="Score")
        melted["Subject"] = melted["Subject"].map(lambda x: SUBJECT_NAMES.get(x, x))
        fig = px.box(melted, x="Subject", y="Score", color="Subject",
                     color_discrete_sequence=[COLORS["accent"], COLORS["secondary"],
                                              COLORS["success"], COLORS["warning"],
                                              "#E056A0"])
        fig.update_layout(**get_plotly_layout(), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Box-plots: median, IQR, and outliers for each subject.")

# ── Tab 5: Student Rankings ─────────────────────────────────────────────
with tab5:
    top_n = st.slider("Number of students", 10, min(100, len(df)), 25, step=5)
    sorted_df = df.nlargest(top_n, TARGET_COL)
    id_col = "name" if "name" in df.columns else "student_id"
    cat_col = "performance_category" if "performance_category" in df.columns else None
    fig = px.bar(sorted_df, x=id_col, y=TARGET_COL, color=cat_col,
                 color_discrete_map={"Low": COLORS["danger"],
                                     "Average": COLORS["warning"],
                                     "High": COLORS["success"]})
    fig.update_layout(**get_plotly_layout(),
                      xaxis=dict(categoryorder="total descending", tickangle=-45),
                      xaxis_title="Student", yaxis_title="Final Score")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Top {top_n} students ranked by final score.")

# ── Preprocessing Summary ───────────────────────────────────────────────
st.markdown("---")
with st.expander("🛠️ Preprocessing Summary & Statistics", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Data Transformations")
        st.json(get_preprocessing_report(original_df, df))
    with c2:
        st.markdown("#### Summary Statistics")
        st.dataframe(get_summary_statistics(df), use_container_width=True)
