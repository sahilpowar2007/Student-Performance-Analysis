"""
Data loading utilities – handles default CSV and user-uploaded files.
"""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Tuple, List

from src.utils import FEATURE_COLS, SUBJECTS, TARGET_COL


def get_default_data_path() -> Path:
    """Return the path to the bundled sample dataset."""
    return Path(__file__).resolve().parent.parent / "data" / "student_performance.csv"


@st.cache_data(show_spinner=False)
def load_default_data() -> pd.DataFrame:
    """Load the default CSV dataset (cached)."""
    path = get_default_data_path()
    if path.exists():
        return pd.read_csv(path)
    st.error("Default dataset not found. Please run `python data/generate_dataset.py` first.")
    return pd.DataFrame()


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Load data from a Streamlit UploadedFile (CSV or Excel).

    Returns an empty DataFrame on failure.
    """
    if uploaded_file is None:
        return pd.DataFrame()
    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        if name.endswith((".xls", ".xlsx")):
            return pd.read_excel(uploaded_file)
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return pd.DataFrame()
    except Exception as exc:
        st.error(f"Error reading file: {exc}")
        return pd.DataFrame()


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Check that *df* contains all required columns.

    Returns ``(is_valid, list_of_missing_columns)``.
    """
    if df is None or df.empty:
        return False, ["(empty DataFrame)"]
    required = set(FEATURE_COLS + SUBJECTS + [TARGET_COL])
    missing = sorted(required - set(df.columns))
    return len(missing) == 0, missing
