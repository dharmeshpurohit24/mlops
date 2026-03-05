# -*- coding: utf-8 -*-
"""
Fraud model training with robust preprocessing, calibration, and
data-driven threshold selection (F-beta, default beta=2).

Outputs:
  - credit_card_fraud.pkl                 : Trained (preprocessing + model [+ calibration]) pipeline
  - credit_card_fraud_threshold.json      : Decision threshold & metadata
"""

from __future__ import annotations

import json
import os
from typing import Dict, Tuple, Optional

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    confusion_matrix,
)

import joblib

# Your data loader/ETL; expected to return (X, y)
from data_analysis import data_analysis


# ----------------------------- Utilities ----------------------------- #

def infer_feature_types(X: pd.DataFrame) -> Tuple[list, list]:
    """
    Identify numeric and categorical columns. Works even if X is all-numeric or all-categorical.
    """
    if not isinstance(X, pd.DataFrame):
        # Best-effort conversion; if already array-like, caller should provide DataFrame.
        X = pd.DataFrame(X)

    numeric_cols = X.select_dtypes(include=[np.number, "float", "int"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    # If no column types detected, treat everything as numeric (safe fallback)
    if not numeric_cols and not categorical_cols:
        numeric_cols = list(X.columns)

    return numeric_cols, categorical_cols


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    Build a ColumnTransformer that scales numeric columns and one-hot encodes categoricals.
    """
    num_cols, cat_cols = infer_feature_types(X)

    transformers = []
    if num_cols:
        transformers.append(("num", StandardScaler(), num_cols))
    if cat_cols:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), cat_cols))

    # If only numeric or only categorical, ColumnTransformer still works.
    preprocessor = ColumnTransformer(transformers, remainder="drop", n_jobs=None)
    return preprocessor


def select_threshold_from_pr(
    y_true: np.ndarray,
    probs: np.ndarray,
    beta: float = 2.0,
    min_precision: Optional[float] = None,
    min_recall: Optional[float] = None,
) -> Dict[str, float]:
    """
    Choose a probability threshold using the Precision-Recall curve.

    By default maximizes F-beta (beta>1 emphasizes recall).
    You may optionally enforce min_precision and/or min_recall constraints.

    Returns dict with threshold and corresponding metrics.
    """
    precision, recall, thresholds = precision_recall_curve(y_true, probs)
    # precision_recall_curve returns len(thresholds)+1 points; align by ignoring the last P/R point
    precision, recall = precision[:-1], recall[:-1]

    # Avoid division-by-zero; classic F-beta formula
    beta2 = beta ** 2
    denom = (beta2 * precision + recall)
    fbeta = np.where(denom > 0, (1 + beta2) * (precision * recall) / denom, 0.0)

    # Apply constraints if provided
    valid = np.ones_like(fbeta, dtype=bool)
    if min_precision is not None:
        valid &= (precision >= min_precision)
    if min_recall is not None:
        valid &= (recall >= min_recall)

    if not np.any(valid):
        # If constraints are too strict, fall back to global max F-beta
        best_idx = int(np.argmax(fbeta))
    else:
        best_idx = int(np.argmax(np.where(valid, fbeta, -1.0)))

    best_thr = float(thresholds[best_idx])
    return {
        "threshold": best_thr,
        "precision": float(precision[best_idx]),
        "recall": float(recall[best_idx]),
        "fbeta": float(fbeta[best_idx]),
        "beta": float(beta),
    }


def predict_with_threshold(probs: np.ndarray, threshold: float) -> np.ndarray:
    return (probs >= threshold).astype(int)


# ----------------------------- Training ----------------------------- #

def train_fraud_model(
    use_calibration: bool = True,
    calibration_method: str = "sigmoid",  # "sigmoid" is robust; "isotonic" needs more data
    random_state: int = 45,
    beta_for_threshold: float = 2.0,
    min_precision: Optional[float] = None,
    min_recall: Optional[float] = None,
    model_path: str = "credit_card_fraud.pkl",
    threshold_path: str = "credit_card_fraud_threshold.json",
) -> None:
    """
    End-to-end training:
      - Split into train/val/test (60/20/20, stratified)
      - Preprocess (scale numeric, one-hot categorical)
      - Train Logistic Regression with class_weight='balanced'
      - Optional probability calibration
      - Pick decision threshold on validation set using PR curve (F-beta)
      - Evaluate on test set at chosen threshold
      - Persist pipeline and threshold metadata
    """
    # 1) Load data
    X, y = data_analysis()
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)  # for preprocessing convenience

    # 2) 60/20/20 stratified split: train / validation / test
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=random_state
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.25, stratify=y_trainval, random_state=random_state
    )
    # Now: train 60%, val 20%, test 20%

    # 3) Build preprocessing
    preprocessor = build_preprocessor(X_train)

    # 4) Base classifier
    base_clf = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs",  # good default for L2
        n_jobs=None,
        random_state=random_state,
    )

    # 5) Pipeline: preprocess -> classifier
    base_pipe = Pipeline([
        ("pre", preprocessor),
        ("clf", base_clf),
    ])

    # 6) Optional calibration: wraps the pipeline as one estimator
    if use_calibration:
        clf = CalibratedClassifierCV(
            base_estimator=base_pipe,
            method=calibration_method,  # "sigmoid" | "isotonic"
            cv=5,
        )
    else:
        clf = base_pipe

    # 7) Fit on TRAIN only (val/test untouched)
    clf.fit(X_train, y_train)

    # 8) Select threshold on VALIDATION using PR curve
    val_probs = clf.predict_proba(X_val)[:, 1]
    thr_info = select_threshold_from_pr(
        y_true=y_val,
        probs=val_probs,
        beta=beta_for_threshold,
        min_precision=min_precision,
        min_recall=min_recall,
    )
    best_thr = thr_info["threshold"]

    # 9) Evaluate on TEST at chosen threshold
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_preds = predict_with_threshold(test_probs, best_thr)

    # Standard metrics
    accuracy = accuracy_score(y_test, test_preds)
    precision = precision_score(y_test, test_preds, zero_division=0)
    recall = recall_score(y_test, test_preds, zero_division=0)
    f1 = f1_score(y_test, test_preds, zero_division=0)

    # Threshold‑free metrics (on probabilities)
    roc_auc = roc_auc_score(y_test, test_probs)
    auprc = average_precision_score(y_test, test_probs)

    cm = confusion_matrix(y_test, test_preds, labels=[0, 1])  # [[TN, FP],[FN, TP]]
    tn, fp, fn, tp = cm.ravel()

    # 10) Persist model + threshold metadata
    joblib.dump(clf, model_path)

    meta = {
        "threshold": best_thr,
        "threshold_selection": thr_info,  # includes beta, P, R, Fbeta on VAL
        "calibration": bool(use_calibration),
        "calibration_method": calibration_method if use_calibration else None,
        "class_weight": "balanced",
        "random_state": random_state,
        "metrics_test": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "roc_auc": roc_auc,
            "auprc": auprc,
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        },
        "splits": {"train": 0.6, "val": 0.2, "test": 0.2},
    }
    with open(threshold_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # 11) Console summary
    print("\n==================== MODEL SUMMARY ====================")
    print(f"Saved pipeline        : {os.path.abspath(model_path)}")
    print(f"Saved threshold meta  : {os.path.abspath(threshold_path)}")
    print("\n-- Threshold (from VALIDATION set) --")
    print(f"Threshold (p>=thr -> 1): {best_thr:.4f}")
    print(f"Val F{thr_info['beta']:.0f}           : {thr_info['fbeta']:.4f}")
    print(f"Val Precision         : {thr_info['precision']:.4f}")
    print(f"Val Recall            : {thr_info['recall']:.4f}")

    print("\n-- TEST metrics at chosen threshold --")
    print(f"Accuracy              : {accuracy:.4f}")
    print(f"Precision             : {precision:.4f}")
    print(f"Recall                : {recall:.4f}")
    print(f"F1                    : {f1:.4f}")
    print(f"ROC-AUC (probs)       : {roc_auc:.4f}")
    print(f"Average Precision     : {auprc:.4f}")
    print(f"Confusion Matrix [[TN, FP],[FN, TP]]: {cm.tolist()}")


# ------------------------------- Entry ------------------------------- #

if __name__ == "__main__":
    train_fraud_model(
        use_calibration=True,          # Turn off if you want a faster baseline
        calibration_method="sigmoid",  # "isotonic" if you have lots of data
        random_state=42,
        beta_for_threshold=2.0,        # Emphasize recall
        min_precision=None,            # e.g., set to 0.10 to ensure at least 10% precision
        min_recall=None,               # e.g., set to 0.80 to ensure at least 80% recall
        model_path="credit_card_fraud.pkl",
        threshold_path="credit_card_fraud_threshold.json",
    )