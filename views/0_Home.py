import streamlit as st
from src.utils import create_header, COLORS, create_kpi_card, apply_custom_css

apply_custom_css()
create_header()

st.markdown(
    f"""
    <div class="glass-card">
        <h2 style="margin-top:0">Welcome 👋, {st.session_state.get('username', '')}</h2>
        <p style="font-size:1.05rem;color:{COLORS['text_secondary']}">
            This interactive dashboard provides comprehensive insights into
            student academic performance, attendance patterns, and engagement
            metrics. Navigate through the pages in the sidebar to explore
            trends, compare subjects, predict outcomes, and generate reports.
        </p>
    </div>""",
    unsafe_allow_html=True,
)

if "processed_data" in st.session_state:
    df = st.session_state["processed_data"]
    # Quick KPI strip
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            create_kpi_card("Total Students", str(len(df)), "👥",
                            color=COLORS["accent"]),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            create_kpi_card("Average Score", f"{df['final_score'].mean():.1f}%", "📈",
                            color=COLORS["success"]),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            create_kpi_card("Avg Attendance", f"{df['attendance_pct'].mean():.1f}%", "📅",
                            color=COLORS["secondary"]),
            unsafe_allow_html=True,
        )
    with c4:
        at_risk = int((df["final_score"] < 50).sum())
        st.markdown(
            create_kpi_card("At-Risk Students", str(at_risk), "⚠️",
                            color=COLORS["danger"]),
            unsafe_allow_html=True,
        )

# Navigation guide
st.markdown("---")
st.markdown(
    f"""
    <div class="glass-card">
        <h3 style="margin-top:0">🗺️ Navigation Guide</h3>
        <table style="width:100%;border-collapse:collapse">
            <tr><td style="padding:10px 8px">📊 <b>Overview</b></td>
                <td style="color:{COLORS['text_secondary']}">KPIs, performance distribution, top performers</td></tr>
            <tr><td style="padding:10px 8px">🔍 <b>EDA</b></td>
                <td style="color:{COLORS['text_secondary']}">Distributions, correlations, scatter plots, box plots</td></tr>
            <tr><td style="padding:10px 8px">👨‍🎓 <b>Student Analysis</b></td>
                <td style="color:{COLORS['text_secondary']}">Individual radar chart, subject breakdown, peer comparison</td></tr>
            <tr><td style="padding:10px 8px">📚 <b>Subject Analysis</b></td>
                <td style="color:{COLORS['text_secondary']}">Pass rates, averages, inter-subject correlation</td></tr>
            <tr><td style="padding:10px 8px">🎯 <b>Prediction</b></td>
                <td style="color:{COLORS['text_secondary']}">Predict a student's score & category from input features</td></tr>
            <tr><td style="padding:10px 8px">🤖 <b>Model Comparison</b></td>
                <td style="color:{COLORS['text_secondary']}">Accuracy, confusion matrices, feature importance</td></tr>
            <tr><td style="padding:10px 8px">📋 <b>Reports</b></td>
                <td style="color:{COLORS['text_secondary']}">Download CSV / PDF reports, at-risk indicators</td></tr>
        </table>
    </div>""",
    unsafe_allow_html=True,
)
