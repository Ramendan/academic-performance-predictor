# Academic Performance Monitoring & Prediction System

A full-stack web application for monitoring student academic records and predicting performance trends using machine learning. Built with Flask, Pandas, Scikit-learn, and a modern dark dashboard UI.

---

## Features

- **Dark Dashboard** — KPI cards, grade distribution, subject radar chart, and study-hours trend
- **Student Management** — Add, view, edit, and delete student records via modal forms
- **Performance Analytics** — Top/bottom performers, GPA histogram, gender comparison, attendance scatter plot
- **ML Predictions** — Four models (Linear Regression, Logistic Regression, Random Forest, Decision Tree) with live evaluation metrics
- **At-Risk Detection** — Automatic flagging of students with low scores or attendance
- **100 Demo Students** — Works out of the box with realistic sample data

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Ramendan/academic-performance-predictor.git
cd academic-performance-predictor
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install all dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate sample data

```bash
python app/data/generate_sample_data.py
```

### 5. Run the application

```bash
python run.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## Project Structure

```
academic-performance-predictor/
├── app/
│   ├── __init__.py              ← Flask app factory
│   ├── routes/
│   │   ├── main.py              ← Dashboard route
│   │   ├── students.py          ← Student CRUD routes
│   │   ├── analytics.py         ← Analytics route
│   │   └── predictions.py       ← ML prediction route
│   ├── ml/
│   │   ├── preprocessing.py     ← Feature engineering & scaling
│   │   ├── trainer.py           ← Model training
│   │   └── predictor.py         ← Prediction interface
│   ├── data/
│   │   ├── data_loader.py       ← Data access layer
│   │   ├── generate_sample_data.py
│   │   └── sample_students.csv  ← 100 demo students
│   ├── templates/               ← Jinja2 HTML templates
│   └── static/                  ← CSS & JS
├── docs/                        ← Project documentation
│   ├── 01_project_overview.md
│   ├── 02_data_collection_management.md
│   ├── 03_performance_analysis.md
│   ├── 04_ml_prediction_models.md
│   └── 05_deployment_guide.md
├── config.py
├── run.py
├── requirements.txt
└── .gitignore
```

---

## Tech Stack

| Component     | Technology                    |
|---------------|-------------------------------|
| Backend       | Python 3.10+, Flask 3.0       |
| Data          | Pandas 2.2, NumPy 1.26        |
| Machine Learning | Scikit-learn 1.5           |
| Frontend      | Bootstrap 5.3 (dark), Chart.js 4.4, Font Awesome 6.5 |
| Storage       | CSV file (no database needed) |

---

## ML Models

| Model              | Task           | Target Variable    |
|--------------------|----------------|--------------------|
| Linear Regression  | Regression     | `avg_score` (0–100)|
| Logistic Regression| Classification | `pass_fail` (0/1)  |
| Random Forest      | Classification | `pass_fail` (0/1)  |
| Decision Tree      | Classification | `pass_fail` (0/1)  |

---

## Pages

| URL              | Description                                       |
|------------------|---------------------------------------------------|
| `/`              | Dashboard with KPI cards and charts               |
| `/students`      | Student list with search, add, delete             |
| `/students/<id>` | Individual student profile with radar chart       |
| `/analytics`     | Class-wide analytics and visualizations           |
| `/predictions`   | Run all 4 ML models + view evaluation metrics     |

---

## Documentation

Full project documentation is in the [`docs/`](docs/) folder:

1. [Project Overview](docs/01_project_overview.md)
2. [Data Collection & Management](docs/02_data_collection_management.md)
3. [Performance Analysis](docs/03_performance_analysis.md)
4. [ML Prediction Models](docs/04_ml_prediction_models.md)
5. [Deployment Guide](docs/05_deployment_guide.md)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Make sure venv is activated: `.\venv\Scripts\Activate.ps1` |
| Blank charts | Allow CDN access (Bootstrap, Chart.js) or use offline copies |
| "Not enough data" on predictions | Add at least 10 students first |
| Port 5000 in use | Edit `run.py` and change `port=5000` to another port |

---

## License

MIT License — free to use, modify, and distribute.
