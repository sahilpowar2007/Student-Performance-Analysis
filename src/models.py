"""
Machine-learning models – data preparation, training, evaluation,
feature importance, and single-student prediction.

NOTE: If scikit-learn cannot be loaded (e.g. due to Windows Application
Control policies), the module exposes the same public API but every
function raises a clear ``RuntimeError`` so that the Streamlit pages
can show a user-friendly message.
"""

import os
from typing import Dict, List, Optional, Any

import numpy as np
import pandas as pd
import joblib

from src.utils import FEATURE_COLS, TARGET_COL, get_performance_category

# ── Attempt to load sklearn ──────────────────────────────────────────────
_SKLEARN_AVAILABLE = True
_SKLEARN_ERROR = ""

try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report,
        mean_absolute_error, mean_squared_error, r2_score,
    )
except Exception as exc:
    _SKLEARN_AVAILABLE = False
    _SKLEARN_ERROR = str(exc)

    # Minimal stubs so the rest of the module can still be imported.
    class StandardScaler:  # type: ignore[no-redef]
        pass

    class LabelEncoder:  # type: ignore[no-redef]
        pass


def _require_sklearn() -> None:
    """Raise a clear error when sklearn is missing."""
    if not _SKLEARN_AVAILABLE:
        raise RuntimeError(
            f"scikit-learn could not be loaded on this system.\n"
            f"Original error: {_SKLEARN_ERROR}\n\n"
            f"This is typically caused by a Windows Application Control (WDAC) "
            f"policy blocking compiled DLL files.  Try one of:\n"
            f"  1. Run the app in a different Python environment (e.g. Anaconda).\n"
            f"  2. Ask your system administrator to whitelist the Python path.\n"
            f"  3. Temporarily disable the Application Control policy."
        )


# ─────────────────────── DATA PREPARATION ────────────────────────────────
def prepare_data(
    df: pd.DataFrame,
    feature_cols: Optional[List[str]] = None,
    target_col: Optional[str] = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Prepare features / labels, encode, scale, and split."""
    _require_sklearn()
    feature_cols = feature_cols or FEATURE_COLS
    target_col = target_col or TARGET_COL

    clean = df.dropna(subset=feature_cols + [target_col]).copy()

    X = clean[feature_cols].values
    y_score = clean[target_col].values
    y_class = clean[target_col].apply(get_performance_category).values

    le = LabelEncoder()
    y_class_enc = le.fit_transform(y_class)

    (X_tr, X_te,
     y_s_tr, y_s_te,
     y_c_tr, y_c_te) = train_test_split(
        X, y_score, y_class_enc,
        test_size=test_size, random_state=random_state,
    )

    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)

    return {
        "X_train": X_tr_s, "X_test": X_te_s,
        "y_class_train": y_c_tr, "y_class_test": y_c_te,
        "y_score_train": y_s_tr, "y_score_test": y_s_te,
        "scaler": scaler,
        "feature_names": list(feature_cols),
        "label_encoder": le,
    }


# ─────────────────────── TRAINING ────────────────────────────────────────
def train_all_classifiers(
    X_train: np.ndarray, y_train: np.ndarray
) -> Dict[str, Any]:
    """Train five classifiers and return ``{name: fitted_model}``."""
    _require_sklearn()
    specs = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=10),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(kernel="rbf", probability=False, random_state=42),
    }
    return {name: m.fit(X_train, y_train) for name, m in specs.items()}


def train_regressor(
    X_train: np.ndarray, y_train: np.ndarray,
):
    """Fit a simple Linear Regression for score prediction."""
    _require_sklearn()
    return LinearRegression().fit(X_train, y_train)


# ─────────────────────── EVALUATION ──────────────────────────────────────
def evaluate_classifier(
    model, X_test: np.ndarray, y_test: np.ndarray,
    label_encoder=None,
) -> Dict[str, Any]:
    """Return accuracy, precision, recall, F1, confusion matrix, and report."""
    _require_sklearn()
    y_pred = model.predict(X_test)
    names = label_encoder.classes_ if label_encoder else None
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(
            y_test, y_pred, target_names=names, output_dict=True, zero_division=0,
        ),
        "y_pred": y_pred,
    }


def evaluate_regressor(
    model, X_test: np.ndarray, y_test: np.ndarray,
) -> Dict[str, Any]:
    """Return MAE, RMSE, R² and predictions."""
    _require_sklearn()
    y_pred = model.predict(X_test)
    return {
        "mae": mean_absolute_error(y_test, y_pred),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "r2": r2_score(y_test, y_pred),
        "y_pred": y_pred,
        "y_test": y_test,
    }


# ─────────────────────── FEATURE IMPORTANCE ──────────────────────────────
def get_feature_importance(
    model, feature_names: List[str],
) -> pd.DataFrame:
    """Extract feature importances (tree-based or coefficient-based)."""
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
    elif hasattr(model, "coef_"):
        coef = model.coef_
        imp = np.abs(coef[0]) if coef.ndim > 1 else np.abs(coef)
    else:
        imp = np.ones(len(feature_names)) / len(feature_names)

    return (
        pd.DataFrame({"feature": feature_names, "importance": imp})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )


# ─────────────────────── PREDICTION ──────────────────────────────────────
def predict_performance(
    features_dict: Dict[str, float],
    clf_model,
    reg_model,
    scaler,
    feature_cols: List[str],
    label_encoder=None,
) -> Dict[str, Any]:
    """Predict category + score for a single student from raw inputs."""
    X = np.array([[features_dict.get(c, 0) for c in feature_cols]])
    X_s = scaler.transform(X)

    pred_score = float(reg_model.predict(X_s)[0])
    pred_idx = clf_model.predict(X_s)[0]
    pred_cat = (
        label_encoder.inverse_transform([pred_idx])[0]
        if label_encoder else str(pred_idx)
    )

    probs: Dict[str, float] = {}
    if hasattr(clf_model, "predict_proba"):
        raw = clf_model.predict_proba(X_s)[0]
        if label_encoder is not None:
            probs = {label_encoder.classes_[i]: float(p) for i, p in enumerate(raw)}
        else:
            probs = {str(i): float(p) for i, p in enumerate(raw)}
    elif hasattr(clf_model, "decision_function"):
        df_vals = np.array(clf_model.decision_function(X_s)[0], dtype=float)
        exp_vals = np.exp(df_vals - np.max(df_vals))
        raw = exp_vals / np.sum(exp_vals)
        if label_encoder is not None and len(label_encoder.classes_) == len(raw):
            probs = {label_encoder.classes_[i]: float(p) for i, p in enumerate(raw)}
        else:
            probs = {str(i): float(p) for i, p in enumerate(raw)}

    return {
        "predicted_category": pred_cat,
        "predicted_score": pred_score,
        "probabilities": probs,
    }


# ─────────────────────── PERSISTENCE ─────────────────────────────────────
def save_models(models_dict: Dict[str, Any], directory: str = "models") -> None:
    """Persist every model to disk with joblib."""
    os.makedirs(directory, exist_ok=True)
    for name, model in models_dict.items():
        fn = name.replace(" ", "_").lower() + ".joblib"
        joblib.dump(model, os.path.join(directory, fn))


def load_saved_models(directory: str = "models") -> Dict[str, Any]:
    """Load all ``.joblib`` files from *directory*."""
    out: Dict[str, Any] = {}
    if not os.path.isdir(directory):
        return out
    for fn in os.listdir(directory):
        if fn.endswith(".joblib"):
            key = fn.replace(".joblib", "").replace("_", " ").title()
            out[key] = joblib.load(os.path.join(directory, fn))
    return out
