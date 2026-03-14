"""
Predictions route: run ML models and display evaluation metrics.
"""

import json
from flask import Blueprint, render_template, request, flash
from app.data.data_loader import load_students
from app.ml.predictor import get_model_metrics, predict_student

predictions_bp = Blueprint("predictions", __name__, url_prefix="/predictions")


@predictions_bp.route("/", methods=["GET", "POST"])
def predictions():
    metrics = get_model_metrics()
    prediction_results = None
    form_data = {}
    selected_student = None

    # Build dropdown list — only the fields we need
    df = load_students()
    students = []
    if not df.empty:
        keep = ["student_id", "name", "gender", "age",
                "attendance_pct", "assignments_submitted",
                "study_hours_per_week", "previous_gpa"]
        available = [c for c in keep if c in df.columns]
        recs = df[available].to_dict("records")
        # Derive first_name / last_name from the single 'name' column
        for r in recs:
            parts = str(r.get("name", "")).split(" ", 1)
            r["first_name"] = parts[0]
            r["last_name"] = parts[1] if len(parts) > 1 else ""
        students = recs

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()

        if student_id and not df.empty:
            # Load the selected student's behavioural data
            row = df[df["student_id"] == int(student_id)]
            if not row.empty:
                r = row.iloc[0]
                form_data = {
                    "student_id": int(student_id),
                    "gender": r.get("gender", "Male"),
                    "age": float(r.get("age", 18)),
                    "attendance_pct": float(r.get("attendance_pct", 75)),
                    "assignments_submitted": float(r.get("assignments_submitted", 8)),
                    "study_hours_per_week": float(r.get("study_hours_per_week", 7)),
                    "previous_gpa": float(r.get("previous_gpa", 2.5)),
                }
                selected_student = r.to_dict()
                # Derive first_name / last_name for the template
                parts = str(selected_student.get("name", "")).split(" ", 1)
                selected_student["first_name"] = parts[0]
                selected_student["last_name"] = parts[1] if len(parts) > 1 else ""
            else:
                flash("Student not found.", "warning")
        else:
            # Custom / hypothetical student
            form_data = {
                "gender": request.form.get("gender", "Male"),
                "age": _safe_float(request.form.get("age", "18")),
                "attendance_pct": _safe_float(request.form.get("attendance_pct", "75")),
                "assignments_submitted": _safe_float(request.form.get("assignments_submitted", "8")),
                "study_hours_per_week": _safe_float(request.form.get("study_hours_per_week", "7")),
                "previous_gpa": _safe_float(request.form.get("previous_gpa", "2.5")),
            }

        if form_data:
            raw = predict_student(form_data)
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
        students=students,
        selected_student=selected_student,
        students_json=json.dumps(students),
    )


def _safe_float(val: str) -> float:
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

