"""Page 1 – Performance Overview: KPIs, donut chart, trend chart, top performers."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.utils import apply_custom_css, create_kpi_card, COLORS, get_plotly_layout
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data
from src.eda import get_performance_distribution

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>📊 Performance Overview</h1>", unsafe_allow_html=True)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]

# ── ROW 1: KPI cards ────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(create_kpi_card("Total Students", str(len(df)), "👥",
                                color=COLORS["accent"]), unsafe_allow_html=True)
with c2:
    st.markdown(create_kpi_card("Avg Score", f"{df['final_score'].mean():.1f}%", "📈",
                                color=COLORS["success"]), unsafe_allow_html=True)
with c3:
    st.markdown(create_kpi_card("Avg Attendance", f"{df['attendance_pct'].mean():.1f}%", "📅",
                                color=COLORS["secondary"]), unsafe_allow_html=True)
with c4:
    at_risk = int((df["final_score"] < 50).sum())
    st.markdown(create_kpi_card("At-Risk Count", str(at_risk), "⚠️",
                                color=COLORS["danger"]), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 2: Donut + Category Averages ────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Performance Distribution")
    dist = get_performance_distribution(df)
    # Order: Low, Average, High
    labels = ["Low", "Average", "High"]
    values = [dist.get(l, 0) for l in labels]
    colors = [COLORS["danger"], COLORS["warning"], COLORS["success"]]
    fig = px.pie(names=labels, values=values, hole=0.55,
                 color_discrete_sequence=colors)
    fig.update_traces(textinfo="label+percent", textfont_size=13)
    fig.update_layout(**get_plotly_layout(), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Students split by Low (<50), Average (50–75), High (>75).")

with c2:
    st.markdown("### Average Score by Category")
    if "performance_category" in df.columns:
        avg = df.groupby("performance_category")["final_score"].mean().reset_index()
        fig2 = px.bar(avg, x="performance_category", y="final_score",
                      color="performance_category",
                      color_discrete_map={"Low": COLORS["danger"],
                                          "Average": COLORS["warning"],
                                          "High": COLORS["success"]})
        fig2.update_layout(**get_plotly_layout(), showlegend=False,
                           xaxis_title="Category", yaxis_title="Avg Score")
        st.plotly_chart(fig2, use_container_width=True)
    st.caption("Mean final score per performance band.")

# ── ROW 3: Top 10 + Attendance Distribution ─────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 🏆 Top 10 Performers")
    top10 = df.nlargest(10, "final_score")
    y_col = "name" if "name" in top10.columns else "student_id"
    fig3 = px.bar(top10, x="final_score", y=y_col, orientation="h",
                  color="final_score",
                  color_continuous_scale=["#14B8C4", "#00D2A0"])
    fig3.update_layout(**get_plotly_layout(),
                       yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Students with the highest final scores.")

with c2:
    st.markdown("### Attendance Distribution")
    fig4 = px.histogram(df, x="attendance_pct", nbins=20,
                        color_discrete_sequence=[COLORS["secondary"]])
    fig4.update_layout(**get_plotly_layout(),
                       xaxis_title="Attendance %", yaxis_title="Count")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Frequency distribution of attendance percentages.")
