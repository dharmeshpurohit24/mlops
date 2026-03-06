# -*- coding: utf-8 -*-
"""
Complex demo module to exercise Bito's Code Review Agent capabilities.

This file contains:
  1) A robust, production-style ML training workflow (good practices)
  2) Multiple intentionally problematic snippets, each labeled with
     "INTENTIONAL_ISSUE: <reason>" so review tools can catch them.

NOTE: The "INTENTIONAL_ISSUE" blocks are for demonstration only.
      Avoid these patterns in real systems.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------------
# Simulated data loader: replace with your project's data access layer.
# If you already have `from data_analysis import data_analysis`, keep that.
# ---------------------------------------------------------------------


def data_analysis() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Return features (X) and labels (y).

    For the demo we synthesize a highly imbalanced dataset to mimic fraud.
    Replace this with your real loader (CSV, parquet, DB, etc.).
    """
    rng = np.random.RandomState(7)
    n = 10_000
    # Numeric features
    X_num = rng.normal(size=(n, 5))
    # Categorical feature with low cardinality
    cat = rng.choice(["A", "B", "C"], size=n, p=[0.2, 0.5, 0.3])
    X = pd.DataFrame(X_num, columns=[f"f{i}" for i in range(X_num.shape[1])])
    X["segment"] = cat
    # Imbalanced target ~1.5% fraud
    y = pd.Series((rng.rand(n) < 0.015).astype(int), name="is_fraud")
    # Small signal for demo
    X["f3"] += y * rng.normal(2.0, 0.5, size=n)
    return X, y


# ----------------------------- Logging --------------------------------

def setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("fraud_demo")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(level.upper())
    return logger


# ----------------------------- Config ---------------------------------

@dataclass
class TrainConfig:
    test_size: float = 0.20
    val_size: float = 0.20  # portion of (train+val) that becomes val
    random_state: int = 42
    use_calibration: bool = True
    calibration_method: str = "sigmoid"  # "sigmoid" | "isotonic"
    beta_for_threshold: float = 2.0      # emphasize recall
    # Grid search over C for LR
    grid_C: Tuple[float, ...] = (0.1, 1.0, 3.0)
    cv_splits: int = 5
    model_path: str = "credit_card_fraud.pkl"
    meta_path: str = "credit_card_fraud_threshold.json"
    # Example of mutable default done safely:
    tags: Dict[str, str] = field(default_factory=lambda: {"owner": "ml-team", "env": "demo"})


# -------------------------- Preprocessing -----------------------------

def infer_feature_types(X: pd.DataFrame) -> Tuple[list, list]:
    numeric_cols = X.select_dtypes(include=[np.number, "float", "int"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    return numeric_cols, categorical_cols


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    num_cols, cat_cols = infer_feature_types(X)
    transformers = []
    if num_cols:
        transformers.append(("num", StandardScaler(), num_cols))
    if cat_cols:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), cat_cols))
    return ColumnTransformer(transformers, remainder="drop")


# ------------------------ Threshold selection -------------------------

def select_threshold_from_pr(
    y_true: np.ndarray,
    probs: np.ndarray,
    beta: float = 2.0,
    min_precision: Optional[float] = None,
    min_recall: Optional[float] = None,
) -> Dict[str, float]:
    precision, recall, thresholds = precision_recall_curve(y_true, probs)
    precision, recall = precision[:-1], recall[:-1]  # align with thresholds
    beta2 = beta ** 2
    denom = (beta2 * precision + recall)
    fbeta = np.where(denom > 0, (1 + beta2) * (precision * recall) / denom, 0.0)

    valid = np.ones_like(fbeta, dtype=bool)
    if min_precision is not None:
        valid &= (precision >= min_precision)
    if min_recall is not None:
        valid &= (recall >= min_recall)
    best_idx = int(np.argmax(np.where(valid, fbeta, -1.0)))

    return {
        "threshold": float(thresholds[best_idx]),
        "precision": float(precision[best_idx]),
        "recall": float(recall[best_idx]),
        "fbeta": float(fbeta[best_idx]),
        "beta": float(beta),
    }


# ------------------------------ Trainer -------------------------------

class FraudTrainer:
    def __init__(self, cfg: TrainConfig, logger: Optional[logging.Logger] = None):
        self.cfg = cfg
        self.logger = logger or setup_logger()

    def build_pipeline(self, X: pd.DataFrame) -> Pipeline:
        pre = build_preprocessor(X)
        lr = LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            solver="lbfgs",
            n_jobs=None,
            random_state=self.cfg.random_state,
        )
        pipe = Pipeline([("pre", pre), ("clf", lr)])
        return pipe

    def fit(self) -> Dict[str, object]:
        X, y = data_analysis()

        X_trainval, X_test, y_trainval, y_test = train_test_split(
            X, y, test_size=self.cfg.test_size, stratify=y, random_state=self.cfg.random_state
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_trainval,
            y_trainval,
            test_size=self.cfg.val_size / (1 - self.cfg.test_size),
            stratify=y_trainval,
            random_state=self.cfg.random_state,
        )
        self.logger.info("Split sizes -> train:%d, val:%d, test:%d", len(X_train), len(X_val), len(X_test))

        # Pipeline + grid search on C
        base_pipe = self.build_pipeline(X_train)
        grid = GridSearchCV(
            base_pipe,
            param_grid={"clf__C": list(self.cfg.grid_C)},
            scoring="average_precision",  # AUCPR surrogate
            cv=StratifiedKFold(n_splits=self.cfg.cv_splits, shuffle=True, random_state=self.cfg.random_state),
            n_jobs=-1,
        )
        grid.fit(X_train, y_train)
        self.logger.info("Best C from CV: %s (mean AP=%.4f)", grid.best_params_.get("clf__C"), grid.best_score_)

        best_est = grid.best_estimator_

        if self.cfg.use_calibration:
            self.logger.info("Applying probability calibration: %s", self.cfg.calibration_method)
            model = CalibratedClassifierCV(best_est, method=self.cfg.calibration_method, cv=3)
            model.fit(X_train, y_train)
        else:
            model = best_est

        # Threshold on validation set
        val_probs = model.predict_proba(X_val)[:, 1]
        thr_info = select_threshold_from_pr(
            y_true=y_val,
            probs=val_probs,
            beta=self.cfg.beta_for_threshold,
        )
        thr = thr_info["threshold"]
        self.logger.info("Selected threshold (VAL): %.4f | Fβ=%.4f P=%.4f R=%.4f",
                         thr, thr_info["fbeta"], thr_info["precision"], thr_info["recall"])

        # Test evaluation
        test_probs = model.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= thr).astype(int)

        metrics = {
            "accuracy": accuracy_score(y_test, test_preds),
            "precision": precision_score(y_test, test_preds, zero_division=0),
            "recall": recall_score(y_test, test_preds, zero_division=0),
            "f1": f1_score(y_test, test_preds, zero_division=0),
            "roc_auc": roc_auc_score(y_test, test_probs),
            "auprc": average_precision_score(y_test, test_probs),
            "cm": confusion_matrix(y_test, test_preds, labels=[0, 1]).tolist(),
        }
        self.logger.info("TEST metrics: %s", json.dumps(metrics, indent=2))

        # Save artifacts
        joblib.dump(model, self.cfg.model_path)
        meta = {
            "threshold": float(thr),
            "threshold_selection": thr_info,
            "class_weight": "balanced",
            "calibration": bool(self.cfg.use_calibration),
            "calibration_method": self.cfg.calibration_method if self.cfg.use_calibration else None,
            "grid_C": self.cfg.grid_C,
            "metrics_test": metrics,
            "tags": self.cfg.tags,
        }
        with open(self.cfg.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        self.logger.info("Saved model -> %s | meta -> %s", os.path.abspath(self.cfg.model_path), os.path.abspath(self.cfg.meta_path))

        return {"model": model, "threshold": thr, "meta": meta}


# ----------------------- Inference helper -----------------------------

def load_and_predict(input_df: pd.DataFrame, model_path: str, meta_path: str) -> pd.DataFrame:
    """
    Load the persisted pipeline and apply the saved decision threshold.
    """
    model = joblib.load(model_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    thr = float(meta["threshold"])
    probs = model.predict_proba(input_df)[:, 1]
    preds = (probs >= thr).astype(int)
    return pd.DataFrame({"prob": probs, "pred": preds})


# =====================================================================
# ============== INTENTIONALLY PROBLEMATIC EXAMPLES ====================
# =====================================================================

# 1) Hard-coded secret (security smell)
DEFAULT_API_KEY = "sk_test_12345"  # INTENTIONAL_ISSUE: Hard-coded credential in source


def print_api_key_for_debug():
    # INTENTIONAL_ISSUE: Logging secrets/keys to console is unsafe.
    print(f"[debug] Using API key: {DEFAULT_API_KEY}")


# 2) Mutable default argument (maintainability bug)
def accumulate_scores(x: float, scores: list = []):  # INTENTIONAL_ISSUE
    """Appends to a shared default list across calls."""
    scores.append(x)
    return scores


# 3) Catch-all exception swallowing root cause (reliability smell)
def unsafe_file_loader(path: str) -> Optional[pd.DataFrame]:
    try:
        return pd.read_csv(path)  # INTENTIONAL_ISSUE: No validation/sanitization of input path
    except Exception:
        # INTENTIONAL_ISSUE: Blanket except hides the error & makes debugging hard
        return None


# 4) Potential SQL injection risk via string formatting (security)
def fetch_user_by_id(conn: sqlite3.Connection, user_id: str):
    # INTENTIONAL_ISSUE: unparameterized query; use parameterized queries instead
    q = f"SELECT id, name FROM users WHERE id = '{user_id}'"
    cur = conn.cursor()
    cur.execute(q)
    return cur.fetchall()


# 5) Data leakage example (ML pitfall) - DO NOT USE IN PRODUCTION
def leaky_fit_predict(X: pd.DataFrame, y: pd.Series):
    """
    INTENTIONAL_ISSUE:
    Fits StandardScaler on the FULL dataset (train + test) then evaluates,
    leaking information from the test set into training.
    """
    pre = ColumnTransformer([("num", StandardScaler(), X.columns)], remainder="drop")
    clf = Pipeline([("pre", pre), ("lr", LogisticRegression(max_iter=200, class_weight="balanced"))])
    # WRONG: splitting after fitting the transformer
    clf.named_steps["pre"].fit(X)  # leakage
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    return accuracy_score(y_test, preds)


# 6) Non-determinism via time-based seed (reproducibility)
def time_seed_random_number() -> int:
    # INTENTIONAL_ISSUE: Seed changes per run, harming repeatability in tests.
    random.seed(int(time.time()))
    return random.randint(1, 1000)


# 7) Dead code / unused variable / shadowing built-ins
def compute_sum(list):  # INTENTIONAL_ISSUE: shadows built-in 'list'
    unused = 42  # INTENTIONAL_ISSUE: unused variable
    total = 0
    for i in list:
        total += i
    if False:
        return -1  # INTENTIONAL_ISSUE: dead branch
    return total


# 8) Performance smell: needless Python loop over vectorizable ops
def slow_probability_threshold(probs: np.ndarray, thr: float) -> np.ndarray:
    # INTENTIONAL_ISSUE: could be (probs >= thr).astype(int)
    out = []
    for p in probs:
        out.append(1 if p >= thr else 0)
    return np.array(out, dtype=int)


# =====================================================================
# =============================== CLI =================================
# =====================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fraud model training (complex demo for code review)")
    p.add_argument("--no-calibration", action="store_true", help="Disable probability calibration")
    p.add_argument("--level", default="INFO", help="Log level (DEBUG/INFO/WARN/ERROR)")
    p.add_argument("--model-path", default="credit_card_fraud.pkl")
    p.add_argument("--meta-path", default="credit_card_fraud_threshold.json")
    return p.parse_args()


def main():
    args = parse_args()
    logger = setup_logger(args.level)

    # Demonstration: call a couple of problematic functions to ensure Bito flags them
    print_api_key_for_debug()                  # INTENTIONAL_ISSUE
    _ = accumulate_scores(0.5)                 # INTENTIONAL_ISSUE
    _ = time_seed_random_number()              # INTENTIONAL_ISSUE

    cfg = TrainConfig(
        use_calibration=not args.no_calibration,
        model_path=args.model_path,
        meta_path=args.meta_path,
    )
    trainer = FraudTrainer(cfg, logger)
    trainer.fit()

    # Show a small inference pass with saved artifacts
    X, _ = data_analysis()
    sample = X.sample(5, random_state=1)
    preds = load_and_predict(sample, cfg.model_path, cfg.meta_path)
    logger.info("Sample predictions:\n%s", preds)


if __name__ == "__main__":
    main()