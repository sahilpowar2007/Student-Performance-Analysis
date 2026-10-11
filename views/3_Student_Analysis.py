"""Page 3 – Student Analysis: individual profile, radar chart, subject bars, comparison."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from src.utils import (
    apply_custom_css, get_plotly_layout,
    SUBJECTS, SUBJECT_NAMES, COLORS,
)
from src.data_loader import load_default_data
from src.preprocessing import preprocess_data
from src.eda import get_student_data

# ── Setup ────────────────────────────────────────────────────────────────

apply_custom_css()
st.markdown("<h1 class='hero-header'>👨‍🎓 Student Analysis</h1>", unsafe_allow_html=True)

if "processed_data" not in st.session_state:
    with st.spinner("Loading data…"):
        st.session_state["data"] = load_default_data()
        st.session_state["processed_data"] = preprocess_data(st.session_state["data"])

df = st.session_state["processed_data"]

# ── Student Selector ────────────────────────────────────────────────────
name_col = "name" if "name" in df.columns else None
if name_col:
    options = [f"{r['student_id']} – {r[name_col]}" for _, r in df.iterrows()]
else:
    options = df["student_id"].tolist()

selected = st.selectbox("🔎 Search & Select Student", options)
sid = selected.split(" – ")[0].split(" - ")[0].strip() if selected else ""
student = get_student_data(df, sid)

if student.empty:
    st.warning("Student not found.")
    st.stop()

st.markdown("---")

# ── Layout: Profile | Charts ────────────────────────────────────────────
left, right = st.columns([1, 2])

cat = student.get("performance_category", "N/A")
cat_color = {"High": COLORS["success"], "Average": COLORS["warning"]}.get(
    cat, COLORS["danger"]
)

# ── LEFT: Profile Card + Comparison ─────────────────────────────────────
with left:
    st.markdown("### 🧑‍🎓 Profile")
    st.markdown(f"**ID:** {student.get('student_id', 'N/A')}")
    if name_col:
        st.markdown(f"**Name:** {student[name_col]}")
    if "gender" in student:
        st.markdown(f"**Gender:** {student['gender']}")
    st.markdown(
        f"**Category:** <span style='color:{cat_color};font-weight:700'>{cat}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        f"<h2 style='text-align:center;color:{cat_color}'>"
        f"{student.get('final_score', 0):.1f}%</h2>"
        f"<p style='text-align:center;color:{COLORS['text_secondary']}'>Final Score</p>",
        unsafe_allow_html=True,
    )

    # Comparison table
    st.markdown("### 📊 vs Class Average")
    compare_cols = [
        ("attendance_pct", "Attendance %"),
        ("internal_marks", "Internal Marks"),
        ("assignment_marks", "Assignment"),
        ("practical_marks", "Practical"),
        ("study_hours_per_day", "Study Hrs/Day"),
        ("participation_score", "Participation"),
        ("final_score", "Final Score"),
    ]
    for col, label in compare_cols:
        if col in student and col in df.columns:
            val = float(student[col])
            avg = float(df[col].mean())
            diff = val - avg
            arrow = "🟢 ↑" if diff >= 0 else "🔴 ↓"
            st.markdown(f"**{label}:** {val:.1f}  ({arrow} {abs(diff):.1f})")

# ── RIGHT: Radar Chart + Subject Bars ───────────────────────────────────
with right:
    # Radar chart
    st.markdown("### 🎯 Performance Indicators (Radar)")
    radar_labels = ["Attendance", "Internal", "Assignment",
                    "Practical", "Study Hours", "Participation"]
    stu_vals = [
        student.get("attendance_pct", 0) / 100,
        student.get("internal_marks", 0) / 50,
        student.get("assignment_marks", 0) / 25,
        student.get("practical_marks", 0) / 25,
        student.get("study_hours_per_day", 0) / 8,
        student.get("participation_score", 0) / 10,
    ]
    avg_vals = [
        df["attendance_pct"].mean() / 100,
        df["internal_marks"].mean() / 50,
        df["assignment_marks"].mean() / 25,
        df["practical_marks"].mean() / 25,
        df["study_hours_per_day"].mean() / 8,
        df["participation_score"].mean() / 10,
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=stu_vals + [stu_vals[0]], theta=radar_labels + [radar_labels[0]],
        fill="toself", name="Student", line_color=COLORS["accent"],
    ))
    fig.add_trace(go.Scatterpolar(
        r=avg_vals + [avg_vals[0]], theta=radar_labels + [radar_labels[0]],
        fill="toself", name="Class Avg", line_color=COLORS["secondary"], opacity=0.45,
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
            bgcolor="rgba(0,0,0,0)",
        ),
        **get_plotly_layout(),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Normalised 0-1 scale. Outer edge = maximum.")

    # Subject-wise grouped bars
    st.markdown("### 📚 Subject Breakdown vs Class Average")
    valid = [s for s in SUBJECTS if s in student and s in df.columns]
    if valid:
        sub_names = [SUBJECT_NAMES.get(s, s) for s in valid]
        stu_scores = [float(student[s]) for s in valid]
        avg_scores = [float(df[s].mean()) for s in valid]
        fig2 = go.Figure(data=[
            go.Bar(name="Student", x=sub_names, y=stu_scores,
                   marker_color=COLORS["accent"]),
            go.Bar(name="Class Avg", x=sub_names, y=avg_scores,
                   marker_color=COLORS["text_secondary"]),
        ])
        fig2.update_layout(barmode="group", **get_plotly_layout(),
                           yaxis_title="Score")
        st.plotly_chart(fig2, use_container_width=True)
    st.caption("Side-by-side comparison per subject.")
