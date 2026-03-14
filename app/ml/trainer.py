"""
Model trainer for the Academic Performance Monitoring & Prediction System.
Trains Linear Regression, Logistic Regression, Random Forest, and Decision Tree models.
"""

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def train_all_models(X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test):
    """
    Train all four models and return a results dict with metrics.

    Returns
    -------
    dict with keys: linear_regression, logistic_regression, random_forest, decision_tree
    """
    results = {}

    # ── Linear Regression ────────────────────────────────────
    lr = LinearRegression()
    lr.fit(X_train, y_reg_train)
    y_pred_lr = lr.predict(X_test)
    rmse_lr = float(np.sqrt(mean_squared_error(y_reg_test, y_pred_lr)))
    r2_lr = float(r2_score(y_reg_test, y_pred_lr))
    results["linear_regression"] = {
        "model": lr,
        "type": "regression",
        "name": "Linear Regression",
        "rmse": round(rmse_lr, 3),
        "r2": round(r2_lr, 3),
        "description": "Predicts the final average score (continuous value) based on student features.",
    }

    # ── Logistic Regression ───────────────────────────────────
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train, y_clf_train)
    y_pred_log = log_reg.predict(X_test)
    results["logistic_regression"] = {
        "model": log_reg,
        "type": "classification",
        "name": "Logistic Regression",
        **_clf_metrics(y_clf_test, y_pred_log),
        "description": "Predicts whether a student will pass or fail (binary classification).",
    }

    # ── Random Forest ─────────────────────────────────────────
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_train, y_clf_train)
    y_pred_rf = rf_clf.predict(X_test)
    results["random_forest"] = {
        "model": rf_clf,
        "type": "classification",
        "name": "Random Forest",
        **_clf_metrics(y_clf_test, y_pred_rf),
        "description": "Ensemble of decision trees for robust pass/fail classification.",
    }

    # ── Decision Tree ─────────────────────────────────────────
    dt_clf = DecisionTreeClassifier(max_depth=6, random_state=42)
    dt_clf.fit(X_train, y_clf_train)
    y_pred_dt = dt_clf.predict(X_test)
    results["decision_tree"] = {
        "model": dt_clf,
        "type": "classification",
        "name": "Decision Tree",
        **_clf_metrics(y_clf_test, y_pred_dt),
        "description": "Rule-based tree model for interpretable pass/fail prediction.",
    }

    return results


def _clf_metrics(y_true, y_pred) -> dict:
    cm = confusion_matrix(y_true, y_pred)
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 3),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 3),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 3),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 3),
        "confusion_matrix": cm.tolist(),
    }
