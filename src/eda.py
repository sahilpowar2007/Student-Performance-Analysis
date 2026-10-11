"""
Exploratory-Data-Analysis helpers – summary stats, correlations,
performance distribution, subject stats, at-risk identification.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

from src.utils import SUBJECTS, SUBJECT_NAMES, FEATURE_COLS, TARGET_COL, get_performance_category


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics for every numeric column."""
    return df.describe().T.round(2)


def get_correlation_matrix(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Pearson correlation matrix for the requested (or default) columns."""
    if columns is None:
        columns = [c for c in FEATURE_COLS + SUBJECTS + [TARGET_COL] if c in df.columns]
    return df[columns].corr(numeric_only=True).round(3)


def get_performance_distribution(
    df: pd.DataFrame, low: float = 50, high: float = 75
) -> Dict[str, int]:
    """Count students in each performance band."""
    if TARGET_COL not in df.columns:
        return {"Low": 0, "Average": 0, "High": 0}
    cats = df[TARGET_COL].apply(lambda x: get_performance_category(x, low, high))
    counts = cats.value_counts().to_dict()
    for cat in ("Low", "Average", "High"):
        counts.setdefault(cat, 0)
    return counts


def get_subject_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Per-subject summary: mean, median, std, min, max, pass rate (≥ 50)."""
    rows = []
    for sub in SUBJECTS:
        if sub not in df.columns:
            continue
        s = df[sub].dropna()
        rows.append({
            "subject": SUBJECT_NAMES.get(sub, sub),
            "column": sub,
            "mean": round(s.mean(), 2),
            "median": round(s.median(), 2),
            "std": round(s.std(), 2),
            "min": round(s.min(), 2),
            "max": round(s.max(), 2),
            "pass_rate": round((s >= 50).mean() * 100, 2),
        })
    return pd.DataFrame(rows)


def get_at_risk_students(
    df: pd.DataFrame,
    attendance_threshold: float = 60,
    score_threshold: float = 50,
) -> pd.DataFrame:
    """Identify students who may need additional support.

    Risk levels
    -----------
    * **High Risk** – both low attendance *and* low score
    * **Medium Risk** – one of the two conditions
    """
    needed = {"attendance_pct", "final_score"}
    if not needed.issubset(df.columns):
        return pd.DataFrame()

    att_risk = df["attendance_pct"] < attendance_threshold
    score_risk = df["final_score"] < score_threshold
    mask = att_risk | score_risk
    out = df.loc[mask].copy()

    if out.empty:
        return out

    out["risk_level"] = np.where(
        att_risk[mask] & score_risk[mask], "High Risk", "Medium Risk"
    )
    out["status_color"] = out["risk_level"].map(
        {"High Risk": "#FF6B6B", "Medium Risk": "#FFB347"}
    )
    # Sort: high-risk first, then by score ascending
    order = {"High Risk": 0, "Medium Risk": 1}
    out = (
        out.assign(_order=out["risk_level"].map(order))
        .sort_values(["_order", "final_score"])
        .drop(columns="_order")
        .reset_index(drop=True)
    )
    return out


def get_student_data(df: pd.DataFrame, student_id: str) -> pd.Series:
    """Fetch a single student's row as a Series."""
    rows = df.loc[df["student_id"] == student_id]
    if rows.empty:
        return pd.Series(dtype=object)
    return rows.iloc[0]
