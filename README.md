# Student Success Analytics | Enterprise Edition

> An advanced, end-to-end data science and machine learning dashboard for tracking, analysing, and predicting student academic performance.

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Usage](#-usage)
- [Data Science Pipeline](#-data-science-pipeline)
- [License](#-license)

---

## 📖 About

The **Student Success Analytics Platform** is a professional-grade Streamlit application designed for modern educational institutions. This platform ingests structured academic and engagement data, processes it through an automated machine learning pipeline, and presents the insights via an elegant, responsive dark-themed dashboard.

It features secure authentication, interactive predictive modeling (with what-if sensitivity analysis), advanced EDA, and automated reporting. 

---

## ✨ Features

| Page | Highlights |
|------|-----------|
| **🔒 Authentication** | Built-in sign-in and sign-up with SHA-256 password hashing and secure session routing. |
| **📊 Overview** | High-level KPI cards, performance donut charts, top performers, and attendance distributions. |
| **🔍 EDA** | 5-tab exploratory data analysis with interactive distribution histograms, correlation heatmaps, scatter trends, and box-plots. |
| **👨‍🎓 Student Analysis** | Searchable student selector, normalised radar charts comparing individuals to class averages, and subject-wise grouped bars. |
| **📚 Subject Analysis** | Deep-dive into pass rates, mean score comparisons, and inter-subject correlations. |
| **🎯 Prediction** | ML-powered prediction interface (sliders for 7 features) yielding predicted performance categories and exact scores, complete with actionable recommendations. |
| **🤖 Model Comparison** | Side-by-side evaluation of 5 classification models and regression models (Accuracy, Precision, Recall, F1, RMSE, R²). Features confusion matrices and feature importance rankings. |
| **📋 Reports** | Dynamic CSV and PDF report generation for both students and the entire cohort. Configurable at-risk student identifiers. |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **UI Framework** | Streamlit 1.28+ |
| **Language** | Python 3.10+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn, Joblib |
| **Reports** | FPDF2, XlsxWriter |
| **Styling** | Custom CSS (Inter font, glassmorphism, CSS animations) |

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.10** or higher
- **pip** package manager

### Steps

```bash
# 1. Clone / download the project
git clone <repository_url>
cd student-performance-analysis

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the sample dataset (if not already present)
python data/generate_dataset.py

# 5. Launch the dashboard
streamlit run app.py
```

The app will securely launch at **http://localhost:8501**. You will be prompted to create an account first.

---

## 💻 Usage

1. **Sign Up / Log In** – Create an account to access the secure enterprise dashboard.
2. **Dashboard Overview** – View automated key performance indicators.
3. **Data Uploader** – Use the sidebar to upload custom `CSV/XLSX` datasets with matching schemas.
4. **Interactive ML** – Navigate to the **Prediction** page, adjust sliders, and instantly query the trained scikit-learn models.
5. **Exports** – Generate PDFs from the **Reports** page.

---

## 🔄 Data Science Pipeline

```
Raw Data Ingestion ──► Preprocessing ──► EDA ──► Feature Engineering
       │                                            │
       ▼                                            ▼
  CSV / XLSX          Missing values,         Correlations,
                      duplicates,              distributions
                      encoding, scaling
                                                    │
                                                    ▼
                                           Train / Test Split
                                                    │
                           ┌────────────────────────┼────────────────────────┐
                           ▼                        ▼                        ▼
                    Classification            Regression              Prediction
                    (5 models)            (Linear Regression)        (Single student)
                           │                        │                        │
                           ▼                        ▼                        ▼
                    Evaluation              Evaluation               Dashboard
                    (Acc, F1, CM)           (MAE, RMSE, R²)          & PDF Reports
```

---

## 📄 License

This enterprise edition software is provided under the MIT License.
