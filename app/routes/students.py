"""
Student management routes: list, add, view, edit, delete.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.data.data_loader import (
    load_students,
    get_student_by_id,
    add_student,
    update_student,
    delete_student,
)
from app.ml.predictor import invalidate_cache

students_bp = Blueprint("students", __name__, url_prefix="/students")

SUBJECT_COLS = ["math", "science", "english", "history", "cs"]
NUMERIC_FIELDS = SUBJECT_COLS + [
    "age", "attendance_pct", "assignments_submitted",
    "study_hours_per_week", "previous_gpa",
]


@students_bp.route("/")
def student_list():
    df = load_students()
    students = df.to_dict("records") if not df.empty else []
    return render_template("students.html", students=students)


@students_bp.route("/add", methods=["POST"])
def student_add():
    data = _parse_form(request.form)
    add_student(data)
    invalidate_cache()
    flash("Student added successfully.", "success")
    return redirect(url_for("students.student_list"))


@students_bp.route("/<int:student_id>")
def student_detail(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("students.student_list"))
    return render_template("student_detail.html", student=student)


@students_bp.route("/<int:student_id>/edit", methods=["POST"])
def student_edit(student_id):
    data = _parse_form(request.form)
    success = update_student(student_id, data)
    invalidate_cache()
    if success:
        flash("Student updated successfully.", "success")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for("students.student_detail", student_id=student_id))


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
def student_delete(student_id):
    success = delete_student(student_id)
    invalidate_cache()
    if success:
        flash("Student deleted.", "info")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for("students.student_list"))


def _parse_form(form) -> dict:
    data = {}
    for key in form:
        val = form[key].strip()
        if key in NUMERIC_FIELDS:
            try:
                data[key] = float(val) if "." in val or key in ["attendance_pct", "study_hours_per_week", "previous_gpa"] else int(val)
            except ValueError:
                data[key] = 0
        else:
            data[key] = val
    # Derive pass_fail from subject scores
    scores = [data.get(s, 0) for s in SUBJECT_COLS if s in data]
    if scores:
        avg = sum(scores) / len(scores)
        data["pass_fail"] = 1 if avg >= 50 else 0
    return data
