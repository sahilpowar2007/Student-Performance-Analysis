"""
Preprocessing pipeline – missing values, duplicates, derived features.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

from src.utils import get_performance_category


# ──────────────────────────── INDIVIDUAL STEPS ───────────────────────────
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill numeric NaNs with column median; categorical NaNs with mode."""
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode().iloc[0])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact-duplicate rows, keeping the first occurrence."""
    return df.drop_duplicates(keep="first").reset_index(drop=True)


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create useful derived columns for analysis and modelling."""
    df = df.copy()

    # Total assessment marks (internal + assignment + practical)
    mark_cols = ["internal_marks", "assignment_marks", "practical_marks"]
    if all(c in df.columns for c in mark_cols):
        df["total_marks"] = df[mark_cols].sum(axis=1).round(2)

    # Performance category label
    if "final_score" in df.columns:
        df["performance_category"] = df["final_score"].apply(get_performance_category)

    # Engagement score (weighted composite 0-100)
    eng_cols = ["attendance_pct", "participation_score", "study_hours_per_day"]
    if all(c in df.columns for c in eng_cols):
        df["engagement_score"] = (
            df["attendance_pct"] / 100 * 0.3
            + df["participation_score"] / 10 * 0.3
            + df["study_hours_per_day"] / 8 * 0.4
        ).mul(100).round(2)

    return df


# ──────────────────────────── FULL PIPELINE ──────────────────────────────
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the complete preprocessing pipeline."""
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = add_derived_features(df)
    return df


# ──────────────────────────── REPORT ─────────────────────────────────────
def get_preprocessing_report(
    original: pd.DataFrame, processed: pd.DataFrame
) -> Dict[str, Any]:
    """Summarise what changed during preprocessing."""
    missing: Dict[str, int] = {
        k: int(v) for k, v in original.isnull().sum().items() if v > 0
    }
    return {
        "original_rows": len(original),
        "processed_rows": len(processed),
        "duplicates_removed": int(len(original) - len(original.drop_duplicates())),
        "missing_values_filled": missing,
        "columns_added": [c for c in processed.columns if c not in original.columns],
    }
