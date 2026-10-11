"""Page 4 – Subject Analysis: overview cards, comparisons, distributions, pass rates, correlations."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.utils import (
    apply_custom_css, get_plotly_layout, create_kpi_card,
    SUBJECTS, SUBJECT_NAMES, COLORS,
)
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data
from src.eda import get_subject_statistics

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>📚 Subject Analysis</h1>", unsafe_allow_html=True)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]
valid_subs = [s for s in SUBJECTS if s in df.columns]
if not valid_subs:
    st.error("No subject columns found in the data.")
    st.stop()

stats_df = get_subject_statistics(df)

# ── Section A: Overview Cards ────────────────────────────────────────────
st.markdown("### Subject Overviews")
cols = st.columns(len(stats_df))
icons = ["📐", "⚛️", "💻", "📊", "📉"]
for i, (_, row) in enumerate(stats_df.iterrows()):
    with cols[i]:
        st.markdown(
            create_kpi_card(
                title=row["subject"],
                value=f"{row['mean']:.1f}",
                icon=icons[i % len(icons)],
                delta=f"Pass rate: {row['pass_rate']:.0f}%",
                color=COLORS["accent"] if row["pass_rate"] >= 60 else COLORS["danger"],
            ),
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Section B + D: Mean Scores & Pass Rates ──────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Mean Score Comparison")
    fig1 = px.bar(stats_df, x="subject", y="mean", color="subject",
                  color_discrete_sequence=[COLORS["accent"], COLORS["secondary"],
                                           COLORS["success"], COLORS["warning"], "#E056A0"])
    fig1.update_layout(**get_plotly_layout(), showlegend=False,
                       xaxis_title="Subject", yaxis_title="Average Score")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Average score per subject across all students.")

with c2:
    st.markdown("### Pass Rate Analysis (≥ 50)")
    bar_colors = [COLORS["danger"] if r < 60 else COLORS["success"]
                  for r in stats_df["pass_rate"]]
    fig3 = go.Figure(go.Bar(
        x=stats_df["subject"], y=stats_df["pass_rate"],
        marker_color=bar_colors,
    ))
    fig3.update_layout(**get_plotly_layout(), yaxis_title="Pass Rate (%)")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Red = pass rate below 60 %. Green = 60 %+.")

# ── Section C + E: Distribution & Correlation ────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Score Distribution")
    sel = st.selectbox("Select Subject", valid_subs,
                       format_func=lambda x: SUBJECT_NAMES.get(x, x))
    fig2 = px.histogram(df, x=sel, marginal="box",
                        color_discrete_sequence=[COLORS["secondary"]])
    fig2.update_layout(**get_plotly_layout(),
                       xaxis_title=SUBJECT_NAMES.get(sel, sel))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f"Distribution for {SUBJECT_NAMES.get(sel, sel)}.")

with c2:
    st.markdown("### Inter-Subject Correlation")
    subj_corr = df[valid_subs].rename(columns=SUBJECT_NAMES).corr()
    fig4 = px.imshow(subj_corr, text_auto=".2f", aspect="auto",
                     color_continuous_scale="Viridis")
    fig4.update_layout(**get_plotly_layout())
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Correlation strictly between subject scores.")
