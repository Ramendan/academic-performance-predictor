"""
Predictions route: run ML models and display evaluation metrics.
"""

import json
from flask import Blueprint, render_template, request
from app.ml.predictor import get_model_metrics, predict_student

predictions_bp = Blueprint("predictions", __name__, url_prefix="/predictions")

SUBJECT_COLS = ["math", "science", "english", "history", "cs"]


@predictions_bp.route("/", methods=["GET", "POST"])
def predictions():
    metrics = get_model_metrics()
    prediction_results = None
    form_data = {}

    if request.method == "POST":
        form_data = {
            "gender": request.form.get("gender", "Male"),
            "age": _safe_float(request.form.get("age", "18")),
            "attendance_pct": _safe_float(request.form.get("attendance_pct", "75")),
            "math": _safe_float(request.form.get("math", "60")),
            "science": _safe_float(request.form.get("science", "60")),
            "english": _safe_float(request.form.get("english", "60")),
            "history": _safe_float(request.form.get("history", "60")),
            "cs": _safe_float(request.form.get("cs", "60")),
            "assignments_submitted": _safe_float(request.form.get("assignments_submitted", "8")),
            "study_hours_per_week": _safe_float(request.form.get("study_hours_per_week", "7")),
            "previous_gpa": _safe_float(request.form.get("previous_gpa", "2.5")),
        }
        raw = predict_student(form_data)
        # Guard: if models couldn't be trained, raw is {"error": "..."}
        if "error" in raw:
            flash(raw["error"], "warning")
            prediction_results = None
        else:
            prediction_results = raw

    return render_template(
        "predictions.html",
        metrics=metrics,
        metrics_json=json.dumps(metrics),
        prediction_results=prediction_results,
        form_data=form_data,
    )


def _safe_float(val: str) -> float:
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0
