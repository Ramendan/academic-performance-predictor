"""
Script to generate sample_students.csv with 100 realistic student records.
Run once: python app/data/generate_sample_data.py
"""

import os
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah",
    "Ivan", "Julia", "Kevin", "Laura", "Michael", "Nina", "Oscar", "Priya",
    "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander",
    "Yasmine", "Zack", "Aisha", "Brandon", "Carol", "David", "Elena", "Frank",
    "Grace", "Henry", "Irene", "James", "Karen", "Leo", "Mia", "Nathan",
    "Olivia", "Peter", "Queenie", "Ryan", "Sara", "Tom", "Ursula", "Vince",
    "Willow", "Xin",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Wilson", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Robinson", "Clark", "Lewis",
]


def generate_students(n=100):
    records = []
    for i in range(1, n + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        gender = random.choice(["Male", "Female"])
        age = random.randint(15, 22)

        # Previous GPA drives performance level
        prev_gpa = round(np.random.beta(5, 2) * 4.0, 2)
        perf_factor = prev_gpa / 4.0  # 0–1

        attendance = round(np.clip(np.random.normal(75 + perf_factor * 20, 10), 30, 100), 1)
        study_hours = round(np.clip(np.random.normal(5 + perf_factor * 10, 3), 1, 20), 1)
        assignments = random.randint(max(1, int(perf_factor * 8)), 12)

        def subject_score():
            base = perf_factor * 60 + np.random.normal(20, 12)
            return int(np.clip(base, 10, 100))

        math = subject_score()
        science = subject_score()
        english = subject_score()
        history = subject_score()
        cs = subject_score()

        avg = (math + science + english + history + cs) / 5
        pass_fail = 1 if avg >= 50 else 0

        records.append({
            "student_id": i,
            "name": name,
            "gender": gender,
            "age": age,
            "attendance_pct": attendance,
            "math": math,
            "science": science,
            "english": english,
            "history": history,
            "cs": cs,
            "assignments_submitted": assignments,
            "study_hours_per_week": study_hours,
            "previous_gpa": prev_gpa,
            "pass_fail": pass_fail,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "sample_students.csv")
    df = generate_students(100)
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} student records → {out_path}")
