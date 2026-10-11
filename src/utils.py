"""
Utility functions and shared constants for the Student Performance Analysis System.
Provides theme colours, chart helpers, KPI card HTML generators, and layout utilities.
"""

import os
from typing import Dict, Any, Optional

import streamlit as st

# ──────────────────────────── THEME CONSTANTS ────────────────────────────
COLORS: Dict[str, str] = {
    "bg": "#0A1128",
    "card_bg": "rgba(255,255,255,0.05)",
    "accent": "#14B8C4",
    "secondary": "#6C5CE7",
    "text": "#FFFFFF",
    "text_secondary": "#A0AEC0",
    "success": "#00D2A0",
    "warning": "#FFB347",
    "danger": "#FF6B6B",
    "border": "rgba(255,255,255,0.1)",
}

# ──────────────────────────── DATA CONSTANTS ─────────────────────────────
SUBJECTS: list[str] = [
    "math_score", "physics_score", "programming_score",
    "data_science_score", "statistics_score",
]

SUBJECT_NAMES: Dict[str, str] = {
    "math_score": "Mathematics",
    "physics_score": "Physics",
    "programming_score": "Programming",
    "data_science_score": "Data Science",
    "statistics_score": "Statistics",
}

FEATURE_COLS: list[str] = [
    "attendance_pct", "internal_marks", "assignment_marks",
    "practical_marks", "previous_sem_result",
    "study_hours_per_day", "participation_score",
]

TARGET_COL: str = "final_score"


# ──────────────────────────── CSS INJECTION ──────────────────────────────
def apply_custom_css() -> None:
    """Read assets/style.css and inject via st.markdown."""
    css_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets", "style.css",
    )
    try:
        with open(css_path, "r", encoding="utf-8") as fh:
            st.markdown(f"<style>{fh.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # graceful degradation


# ──────────────────────────── KPI CARD HTML ──────────────────────────────
def create_kpi_card(
    title: str,
    value: str,
    icon: str,
    delta: Optional[str] = None,
    color: Optional[str] = None,
) -> str:
    """Return HTML for a glassmorphism KPI card."""
    c = color or COLORS["accent"]
    delta_html = (
        f'<div style="font-size:0.85em;margin-top:6px;color:{COLORS["text_secondary"]}">'
        f"{delta}</div>"
        if delta
        else ""
    )
    return f"""
    <div style="
        background:{COLORS['card_bg']};
        border:1px solid {COLORS['border']};
        border-radius:16px;padding:24px;text-align:center;
        box-shadow:0 8px 32px rgba(0,0,0,0.25);
        backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
        margin-bottom:1rem;transition:transform .3s,box-shadow .3s;
    ">
        <div style="font-size:2.2em;margin-bottom:8px">{icon}</div>
        <div style="font-size:2em;font-weight:700;color:{c}">{value}</div>
        <div style="font-size:0.95em;color:{COLORS['text_secondary']};margin-top:4px">{title}</div>
        {delta_html}
    </div>"""


# ──────────────────────────── PLOTLY LAYOUT ──────────────────────────────
def get_plotly_layout(**kwargs: Any) -> Dict[str, Any]:
    """Return a consistent dark-themed Plotly layout dict."""
    layout: Dict[str, Any] = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], family="Inter, sans-serif", size=13),
        colorway=[
            COLORS["accent"], COLORS["secondary"], COLORS["success"],
            COLORS["warning"], COLORS["danger"], "#E056A0", "#00B4D8", "#FFD93D",
        ],
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kwargs)
    return layout


# ──────────────────────────── HELPERS ────────────────────────────────────
def get_performance_category(
    score: float,
    low_threshold: float = 50,
    high_threshold: float = 75,
) -> str:
    """Classify a score into Low / Average / High."""
    if score < low_threshold:
        return "Low"
    if score <= high_threshold:
        return "Average"
    return "High"


def format_metric(value: float, suffix: str = "", precision: int = 1) -> str:
    """Format a number for display (e.g. 78.3%)."""
    return f"{value:.{precision}f}{suffix}"


def get_status_color(category: str) -> str:
    """Map a performance category to a hex colour."""
    return {
        "low": COLORS["danger"],
        "average": COLORS["warning"],
        "high": COLORS["success"],
    }.get(str(category).lower(), COLORS["text"])


def create_header() -> None:
    """Render the hero header with title and professional branding."""
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,{COLORS['bg']} 0%,rgba(20,184,196,0.12) 100%);
            border:1px solid {COLORS['border']};
            border-bottom:3px solid {COLORS['accent']};
            padding:32px 20px;border-radius:16px;margin-bottom:28px;text-align:center;
            backdrop-filter:blur(12px); animation: fadeInDown 0.8s ease-out;
        ">
            <h1 style="color:{COLORS['text']};margin:0;font-size:2.4em; font-weight:800; letter-spacing:-0.5px;">
                Student Success Analytics
            </h1>
            <p style="color:{COLORS['accent']};margin-top:10px;font-size:1.05em; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">
                Advanced Machine Learning & Intelligence Suite
            </p>
        </div>
        
        <style>
            @keyframes fadeInDown {{
                from {{ opacity: 0; transform: translateY(-15px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
