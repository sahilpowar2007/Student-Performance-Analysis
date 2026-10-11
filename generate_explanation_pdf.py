"""
Script to generate comprehensive project explanation PDF.
Run this from the project root: python generate_explanation_pdf.py
"""

from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(18, 20, 18)

    def header(self):
        self.set_fill_color(10, 17, 40)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(20, 184, 196)
        self.cell(0, 12, 'Student Performance Analysis System - Project Documentation', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
        self.set_text_color(0, 0, 0)

    def chapter_title(self, title):
        self.set_fill_color(10, 17, 40)
        self.set_text_color(20, 184, 196)
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def section_title(self, title):
        self.set_text_color(10, 50, 120)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(self.epw, 7, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(self.epw, 6, '  - ' + text)
        self.set_text_color(0, 0, 0)

    def q_and_a(self, q, a):
        self.set_fill_color(235, 245, 255)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 60, 140)
        self.multi_cell(self.epw, 7, 'Q: ' + q, fill=True)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(self.epw, 7, 'A: ' + a)
        self.ln(3)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

# ========== COVER PAGE ==========
pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(10, 17, 40)
pdf.ln(20)
pdf.cell(0, 14, 'Student Performance Analysis System', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(20, 184, 196)
pdf.cell(0, 10, 'Project Report & Viva Preparation Guide', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(5)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, 'A comprehensive explanation for external examiners', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(15)
pdf.set_draw_color(20, 184, 196)
pdf.set_line_width(1)
pdf.line(30, pdf.get_y(), 180, pdf.get_y())
pdf.ln(10)
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(100, 100, 100)
for line in ['Technology: Python, Streamlit, scikit-learn, Pandas, Plotly', 'Deployment: Streamlit Community Cloud + GitHub', 'Type: Machine Learning Web Application']:
    pdf.cell(0, 7, line, align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_text_color(0, 0, 0)
pdf.ln(10)

# ========== SECTION 1: PROJECT OVERVIEW ==========
pdf.add_page()
pdf.chapter_title('1. PROJECT OVERVIEW')
pdf.body_text(
    'The Student Performance Analysis System is a full-stack data analytics and machine learning '
    'web application built using Python and Streamlit. It allows educators and administrators to '
    'upload student data, explore trends through interactive charts, predict student performance '
    'using machine learning models, and generate downloadable reports.'
)
pdf.section_title('1.1 Main Objectives')
for b in [
    'Analyze academic performance of 500+ students across 5 subjects (Math, Physics, Programming, Data Science, Statistics)',
    'Provide interactive visualizations using Plotly for charts and graphs',
    'Apply machine learning models (5 classifiers + 1 regressor) to predict performance category (Low, Average, High)',
    'Allow secure login/logout system with user authentication',
    'Generate downloadable PDF and CSV reports for student-wise data',
]:
    pdf.bullet(b)
pdf.ln(3)

pdf.section_title('1.2 Technology Stack')
tech = [
    ('Frontend / UI', 'Streamlit (Python web framework) - renders dashboard, charts, inputs'),
    ('Data Processing', 'Pandas - reads CSV/Excel, cleans missing values, computes statistics'),
    ('Visualization', 'Plotly Express and Plotly Graph Objects - interactive bar, pie, scatter, heatmap charts'),
    ('Machine Learning', 'scikit-learn - trains classifiers (Logistic Regression, Decision Tree, Random Forest, KNN, SVM) and a Linear Regression model'),
    ('Authentication', 'hashlib (SHA-256 password hashing), JSON file-based user storage'),
    ('Reports', 'fpdf2 - generates professional PDF reports; openpyxl/xlsxwriter - generates Excel files'),
    ('Deployment', 'GitHub + Streamlit Community Cloud (free hosting with auto-deploy on push)'),
    ('Version Control', 'Git + GitHub repository (sahilpowar2007/Student-Performance-Analysis)'),
]
for k, v in tech:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(10, 50, 120)
    pdf.cell(50, 7, k + ':', new_x='RIGHT', new_y='LAST')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(pdf.epw, 7, v)
    pdf.set_text_color(0, 0, 0)
pdf.ln(3)

# ========== SECTION 2: PROJECT STRUCTURE ==========
pdf.add_page()
pdf.chapter_title('2. PROJECT STRUCTURE & FILES EXPLAINED')
pdf.body_text(
    'The project follows a clean MVC-like (Model-View-Controller) structure. '
    'All pages are in the views/ folder, business logic is in src/, and static assets like CSS are in assets/.'
)
files = [
    ('app.py', 'Main entry point. Handles routing, authentication gate, sidebar with file upload, and navigation to all 8 pages.'),
    ('src/auth.py', 'Authentication module. Contains Sign In and Sign Up forms with SHA-256 password hashing and JSON-based user storage.'),
    ('src/data_loader.py', 'Loads CSV or Excel data uploaded by the user, or falls back to the default sample dataset (data/student_performance.csv).'),
    ('src/preprocessing.py', 'Cleans the raw data: removes duplicates, fills missing values, applies performance categorization (Low/Average/High based on final_score).'),
    ('src/models.py', 'Trains 5 ML classifiers and 1 regressor. Returns predictions, probabilities, confusion matrix, classification report, and feature importances.'),
    ('src/utils.py', 'Shared constants (COLORS, SUBJECTS, FEATURE_COLS), CSS injection function, KPI card HTML generator, and Plotly layout settings.'),
    ('src/eda.py', 'EDA helper functions: subject statistics, correlation matrix, scatter data, top performers, boxplot data.'),
    ('views/0_Home.py', 'Dashboard home/welcome page shown after login.'),
    ('views/1_Overview.py', 'Shows 4 KPI cards (Total, Avg, Pass Rate, At-Risk %), Performance Distribution donut chart, Average Score by Category, Top 10 Performers, Attendance Distribution.'),
    ('views/2_EDA.py', 'Exploratory Data Analysis: Distribution plots, Correlation Heatmap, Scatter plots, Boxplots, Top/Bottom 10 rankings.'),
    ('views/3_Student_Analysis.py', 'Search and select individual students. Shows their profile, radar chart, subject bars, and comparison table.'),
    ('views/4_Subject_Analysis.py', 'Subject-level analysis: mean comparison bar chart, pass rate analysis, score distribution histogram, inter-subject correlation heatmap.'),
    ('views/5_Prediction.py', 'Input sliders for student features -> ML model predicts performance category and score. What-If analysis shows impact of improvements.'),
    ('views/6_Model_Comparison.py', 'Compares all 5 ML classifiers on Accuracy, Precision, Recall, F1. Shows confusion matrices, feature importance, regression model metrics.'),
    ('views/7_Reports.py', 'Generates and downloads student-wise PDF report, full data Excel export, and At-Risk student list with risk level coloring.'),
    ('assets/style.css', 'Custom CSS for the dark navy theme, glassmorphism cards, animations, high-contrast dropdown options, button styles.'),
    ('.streamlit/config.toml', 'Streamlit configuration: enforces native dark theme, sets primaryColor to cyan (#14B8C4), and text color to white.'),
    ('data/student_performance.csv', 'Built-in sample dataset with 500+ students and 15 columns used as default data source.'),
    ('data/sample_student_records.csv', 'Ready-made 40-student sample CSV file that can be downloaded and re-uploaded for testing the upload feature.'),
    ('requirements.txt', 'Lists all Python package dependencies needed for the project to run (streamlit, pandas, scikit-learn, plotly, fpdf2, etc.).'),
]
for fname, desc in files:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(10, 50, 120)
    pdf.cell(0, 7, fname, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(pdf.epw, 6, '    ' + desc)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

# ========== SECTION 3: WORKFLOW ==========
pdf.add_page()
pdf.chapter_title('3. HOW THE SYSTEM WORKS - STEP BY STEP FLOW')
steps = [
    ('Step 1 - User Opens Website', 'The browser loads the Streamlit app. The app.py first checks if the user is logged in (st.session_state["logged_in"]). If not, it shows the login page from auth.py and stops.'),
    ('Step 2 - Login / Sign Up', 'User enters email and password. The password is hashed using SHA-256 (hashlib) and compared with the stored hash in data/users.json. On success, session_state["logged_in"] = True.'),
    ('Step 3 - Sidebar Loads', 'After login, the sidebar appears with: Logout button, Data Source upload (CSV/XLSX), and navigation links to all 8 pages.'),
    ('Step 4 - Data Loading', 'If user uploads a file, it is read by load_uploaded_data(). It validates that all required columns are present. If not uploaded, the default student_performance.csv is used.'),
    ('Step 5 - Data Preprocessing', 'preprocess_data() removes duplicate rows, fills missing values with column means, and assigns a performance_category (Low = score < 50, Average = 50-75, High > 75) to each student.'),
    ('Step 6 - Page Navigation', 'Using st.navigation(), the user can navigate to 7 dashboard pages. Each page independently loads data from st.session_state and renders charts.'),
    ('Step 7 - ML Prediction (Page 5)', 'The user inputs 7 feature values using sliders. These are scaled using StandardScaler and passed to the best-performing classifier (found by evaluating all 5 models on test data). The predicted category and confidence probabilities are shown.'),
    ('Step 8 - Report Generation (Page 7)', 'User selects a student. The system generates a PDF with student details, scores, and performance rating using fpdf2, or an Excel file with full dataset using openpyxl.'),
]
for title, desc in steps:
    pdf.section_title(title)
    pdf.body_text(desc)
    pdf.ln(1)

# ========== SECTION 4: ML MODELS EXPLAINED ==========
pdf.add_page()
pdf.chapter_title('4. MACHINE LEARNING MODELS EXPLAINED')
pdf.body_text(
    'The project uses supervised machine learning with labeled data. The target variable is '
    'performance_category (Low, Average, High) for classification, and final_score for regression. '
    'The data is split 80% training and 20% testing using train_test_split.'
)
pdf.section_title('4.1 Input Features (7 Features)')
for f in ['attendance_pct (Attendance %)', 'internal_marks (out of 50)', 'assignment_marks (out of 25)', 'practical_marks (out of 25)', 'previous_sem_result', 'study_hours_per_day', 'participation_score']:
    pdf.bullet(f)
pdf.ln(3)
pdf.section_title('4.2 Classification Models (predict category: Low/Average/High)')
models_info = [
    ('Logistic Regression', 'A linear model that learns a decision boundary between classes. Fast and interpretable. Uses sigmoid function to output class probabilities.'),
    ('Decision Tree', 'Splits data using feature thresholds (e.g., attendance > 75%). Creates a tree of if-else rules. Easy to understand but may overfit.'),
    ('Random Forest', 'Builds 100 decision trees on random subsets and takes majority vote. More accurate and robust than a single Decision Tree.'),
    ('KNN (K-Nearest Neighbors)', 'Classifies a new student by finding 5 most similar students in the training set and taking majority vote of their categories.'),
    ('SVM (Support Vector Machine)', 'Finds the best hyperplane that separates classes with maximum margin. Effective for high-dimensional data.'),
]
for name, desc in models_info:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(10, 50, 120)
    pdf.cell(0, 7, name, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(pdf.epw, 6, '    ' + desc)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)
pdf.section_title('4.3 Regression Model (predict score)')
pdf.body_text('Linear Regression: Fits a straight line through data points to predict the numerical final_score from the 7 input features. Evaluated using MAE (Mean Absolute Error), RMSE (Root Mean Squared Error), and R2 Score (coefficient of determination).')
pdf.section_title('4.4 How Best Model is Chosen')
pdf.body_text('After training all 5 classifiers, each is evaluated on the test set. The model with the highest Accuracy is automatically selected as the "Best Model". No model is assumed to be best in advance - it is determined purely by performance on this dataset.')

# ========== SECTION 5: DATASET ==========
pdf.add_page()
pdf.chapter_title('5. DATASET EXPLANATION')
pdf.body_text('The system uses a synthetically generated dataset of 515 student records (500 unique + 15 duplicates added for preprocessing demo). The dataset has 15 columns and intentionally includes ~4% missing values to demonstrate data cleaning.')
pdf.section_title('5.1 Column Details')
cols = [
    ('student_id', 'Unique identifier (STU001, STU002, ...)'),
    ('name', 'Student name'),
    ('gender', 'Male or Female'),
    ('attendance_pct', 'Attendance percentage (40% to 100%)'),
    ('internal_marks', 'Internal exam marks out of 50'),
    ('assignment_marks', 'Assignment marks out of 25'),
    ('practical_marks', 'Practical exam marks out of 25'),
    ('previous_sem_result', 'Previous semester score (30-100)'),
    ('study_hours_per_day', 'Average daily study hours (0.5-8)'),
    ('participation_score', 'Class participation score (1-10)'),
    ('math_score', 'Mathematics score (15-100)'),
    ('physics_score', 'Physics score (15-100)'),
    ('programming_score', 'Programming score (15-100)'),
    ('data_science_score', 'Data Science score (15-100)'),
    ('statistics_score', 'Statistics score (15-100)'),
    ('final_score', 'Average of all 5 subject scores (computed target variable)'),
]
for c, d in cols:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(10, 50, 120)
    pdf.cell(55, 6, c, new_x='RIGHT', new_y='LAST')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 6, d, new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
pdf.ln(3)
pdf.section_title('5.2 Performance Category Logic')
pdf.body_text('After computing final_score (average of 5 subject scores), each student is categorized as:\n- Low: final_score < 50\n- Average: 50 <= final_score <= 75\n- High: final_score > 75\nThis is done in preprocessing.py using the get_performance_category() function from utils.py.')

# ========== SECTION 6: VIVA QUESTIONS ==========
pdf.add_page()
pdf.chapter_title('6. VIVA QUESTIONS AND ANSWERS')
pdf.body_text('These are commonly asked questions in project viva/demonstration. Read these carefully to confidently explain your project to external examiners.')

viva = [
    ('What is the main objective of your project?',
     'The main objective is to build a web-based system that analyzes student academic performance, visualizes trends using interactive charts, predicts student performance categories using machine learning, and generates downloadable reports for educators.'),
    ('What programming language and framework did you use?',
     'We used Python as the main programming language. Streamlit was used as the web framework to build the interactive dashboard. Plotly was used for charts, scikit-learn for machine learning, and fpdf2 for PDF generation.'),
    ('What machine learning models did you implement?',
     'We implemented 5 classification models: Logistic Regression, Decision Tree, Random Forest, KNN, and SVM. We also implemented Linear Regression to predict the numerical final score. All models are trained and evaluated on the same test data.'),
    ('How do you select the best model?',
     'After training all 5 classifiers, we evaluate each one on the 20% test split using accuracy score. The model with the highest accuracy is automatically selected as the best model. This decision is not made manually - it is data-driven.'),
    ('What is the difference between classification and regression in your project?',
     'Classification predicts the category of a student: Low, Average, or High (discrete output). Regression predicts the actual numerical score (continuous output). We use classification for the Prediction page and Linear Regression to predict the final_score value.'),
    ('What features (inputs) does the ML model use?',
     'The model uses 7 input features: attendance_pct, internal_marks, assignment_marks, practical_marks, previous_sem_result, study_hours_per_day, and participation_score. These are the factors most relevant to predicting a student\'s final performance.'),
    ('How did you handle missing values in the dataset?',
     'In the preprocessing step (src/preprocessing.py), we fill missing numerical values with the mean of that column. We also remove duplicate rows. This ensures the model receives clean, consistent data.'),
    ('How is the password stored securely?',
     'We use SHA-256 hashing from Python\'s built-in hashlib library. When a user signs up, the password is hashed before storing in a JSON file. During login, the entered password is hashed and compared with the stored hash. The actual password is never stored.'),
    ('What is StandardScaler and why did you use it?',
     'StandardScaler from scikit-learn standardizes feature values so they all have mean=0 and standard deviation=1. This is important because models like KNN, SVM, and Logistic Regression are sensitive to the scale of input features. Without scaling, a feature like internal_marks (0-50) would dominate over participation_score (1-10).'),
    ('What is Streamlit and how does it work?',
     'Streamlit is a Python library that converts Python scripts into interactive web applications without needing HTML, CSS, or JavaScript knowledge. Every time a user interacts with a widget (button, slider, dropdown), Streamlit re-runs the entire script and updates the display accordingly.'),
    ('What is st.session_state and why did you use it?',
     'st.session_state is a dictionary provided by Streamlit to store variables that persist across page navigation and re-runs. We use it to store the logged_in status, loaded data (data, processed_data), and student selections so they do not reset every time a page changes.'),
    ('What charts are used in your project and why?',
     'We used: Pie/Donut chart for Performance Distribution, Bar charts for Average Score by Category and Top 10 Performers, Histogram for Attendance Distribution, Heatmap for Correlation Matrix, Scatter plots for Actual vs Predicted scores, Radar chart for individual student profiles, and Horizontal bar charts for Feature Importance.'),
    ('What is a confusion matrix?',
     'A confusion matrix shows how well a classification model performs. Rows represent actual categories, columns represent predicted categories. The diagonal cells show correct predictions, and off-diagonal cells show misclassifications. We display confusion matrices for all 5 models in the Model Comparison page.'),
    ('What is F1-Score?',
     'F1-Score is the harmonic mean of Precision and Recall. Precision measures how many of the predicted positive cases are actually positive. Recall measures how many actual positive cases were correctly predicted. F1-Score balances both, especially useful when class distribution is imbalanced.'),
    ('What is feature importance?',
     'Feature importance tells us which input features contribute most to the model\'s prediction. For Random Forest, it is computed using how much each feature reduces impurity across all trees. Features with higher importance have more influence on the final prediction.'),
    ('How did you deploy the project online?',
     'We used Streamlit Community Cloud (share.streamlit.io) for free hosting. The project code is stored on GitHub (sahilpowar2007/Student-Performance-Analysis). Streamlit Cloud is connected to this repository and automatically redeploys the app whenever new code is pushed to the main branch.'),
    ('What is the EDA (Exploratory Data Analysis) page?',
     'The EDA page allows users to explore the dataset visually before applying any models. It includes Distribution plots (histogram showing how values are spread), Correlation Heatmap (which subjects are related to each other), Scatter plots (relationship between two chosen columns), Boxplots (showing median, quartiles, and outliers), and Top/Bottom 10 student rankings.'),
    ('What is the What-If Analysis in the Prediction page?',
     'What-If Analysis shows the impact of improving one factor at a time. For example, if a student improves their attendance by 10%, how much would their predicted score increase? It runs the prediction for 4 hypothetical improvements (attendance +10%, study hours +1hr, participation +2, internal marks +5) and shows the score delta for each.'),
    ('What is the At-Risk student feature in the Reports page?',
     'At-Risk students are identified based on two criteria: attendance below a threshold (default 75%) and final_score below 50. The system displays these students with color-coded risk levels (High Risk = both criteria, Medium Risk = one criterion). A disclaimer is shown stating this is an analytical indicator, not a judgment of ability.'),
    ('Why did you choose Streamlit over Flask or Django?',
     'Streamlit is specifically designed for data science and ML applications. It allows rapid development of interactive dashboards with far less code than Flask or Django. It has built-in widgets like sliders, file uploaders, and charts. For a data-focused project like this, Streamlit was the most efficient and appropriate choice.'),
]

for q, a in viva:
    pdf.q_and_a(q, a)

# ========== SECTION 7: SUMMARY TABLE ==========
pdf.add_page()
pdf.chapter_title('7. QUICK REFERENCE SUMMARY')
summary = [
    ('Total Pages', '8 (Home, Overview, EDA, Student Analysis, Subject Analysis, Prediction, Model Comparison, Reports)'),
    ('Dataset Size', '515 rows x 15 columns (500 students + 15 duplicates, 4% missing values)'),
    ('ML Models', '5 Classifiers + 1 Regressor = 6 ML models total'),
    ('Best Classifier', 'Auto-selected based on highest accuracy on test split (typically SVM ~86%)'),
    ('Regressor R2', '~0.93 (excellent fit - Linear Regression explains 93% variance in scores)'),
    ('Authentication', 'SHA-256 hashed passwords stored in data/users.json'),
    ('CSS Theme', 'Dark navy (#0A1128), Cyan accent (#14B8C4), White text (#FFFFFF)'),
    ('Deployment URL', 'student-performance-analysis-system1.streamlit.app'),
    ('GitHub Repo', 'github.com/sahilpowar2007/Student-Performance-Analysis'),
    ('Report Formats', 'PDF (fpdf2), Excel/CSV (openpyxl, xlsxwriter, pandas)'),
]
for k, v in summary:
    pdf.set_fill_color(235, 245, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(10, 50, 120)
    pdf.cell(62, 8, k, fill=True, new_x='RIGHT', new_y='LAST', border=1)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(pdf.epw, 8, v, border=1, fill=False)
    pdf.set_text_color(0, 0, 0)

pdf.ln(8)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(20, 184, 196)
pdf.cell(0, 10, 'Best of Luck for your Viva! You have built a professional, industry-standard project.', align='C', new_x='LMARGIN', new_y='NEXT')

out_path = os.path.join(os.path.dirname(__file__), 'data', 'Project_Explanation_and_Viva.pdf')
pdf.output(out_path)
print(f'PDF saved at: {out_path}')
