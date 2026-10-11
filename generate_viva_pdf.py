"""
Generate dedicated 'Most Asked Viva Questions & Answers' PDF for External Examination.
Run: python generate_viva_pdf.py
"""

from fpdf import FPDF
import os

class VivaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(16, 18, 16)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(10, 17, 40)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(20, 184, 196)
        self.cell(self.epw, 10, 'Student Performance Analysis System - External Viva Guide', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(self.epw, 8, f'External Viva Preparation Guide | Page {self.page_no()}', align='C')

    def chapter_header(self, number, title):
        self.ln(2)
        self.set_fill_color(10, 25, 55)
        self.set_text_color(20, 184, 196)
        self.set_font('Helvetica', 'B', 12)
        self.cell(self.epw, 9, f'  {number}. {title}', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def question_box(self, q_num, question, answer, examiner_tip=None):
        # Question Bar
        self.set_fill_color(230, 243, 250)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(10, 45, 110)
        q_text = f'Q{q_num}: {question}'
        self.multi_cell(self.epw, 6, q_text, fill=True)
        self.ln(1)

        # Answer Text
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(self.epw, 5.5, f'Answer:\n{answer}')
        
        # Examiner Tip (if provided)
        if examiner_tip:
            self.ln(1)
            self.set_fill_color(245, 247, 250)
            self.set_font('Helvetica', 'I', 8.5)
            self.set_text_color(100, 110, 125)
            self.multi_cell(self.epw, 5, f'Examiner Tip: {examiner_tip}', fill=True)

        self.ln(3)


pdf = VivaPDF()
pdf.add_page()

# ══════════════════════════ COVER PAGE ══════════════════════════
pdf.set_fill_color(10, 17, 40)
pdf.rect(0, 0, 210, 48, 'F')

pdf.set_y(12)
pdf.set_font('Helvetica', 'B', 20)
pdf.set_text_color(255, 255, 255)
pdf.cell(pdf.epw, 10, 'External Viva Voce Preparation Guide', align='C', new_x='LMARGIN', new_y='NEXT')

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(20, 184, 196)
pdf.cell(pdf.epw, 8, 'Student Performance Analysis & Prediction System', align='C', new_x='LMARGIN', new_y='NEXT')

pdf.set_y(54)
pdf.set_font('Helvetica', 'I', 9.5)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(pdf.epw, 5, 
    'This handbook contains the top 30 most-frequently asked questions by External Examiners '
    'during project viva examinations, written in simple, clear, professional English. '
    'Every question includes the direct answer and examiner perspective tips.')
pdf.ln(2)

# Quick Project Snapshot Card
pdf.set_fill_color(240, 247, 255)
pdf.rect(16, pdf.get_y(), pdf.epw, 24, 'F')
pdf.set_draw_color(20, 184, 196)
pdf.rect(16, pdf.get_y(), pdf.epw, 24, 'D')

curr_y = pdf.get_y() + 2
pdf.set_xy(20, curr_y)
pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(10, 45, 110)
pdf.cell(85, 5, 'Project: Student Performance Analysis System', new_x='RIGHT', new_y='LAST')
pdf.cell(85, 5, 'ML Models: 5 Classifiers + 1 Regressor', new_x='LMARGIN', new_y='NEXT')

pdf.set_x(20)
pdf.cell(85, 5, 'Framework: Streamlit 1.30+ (Python)', new_x='RIGHT', new_y='LAST')
pdf.cell(85, 5, 'Target: Performance Band (Low, Avg, High) & Score', new_x='LMARGIN', new_y='NEXT')

pdf.set_x(20)
pdf.cell(85, 5, 'Hosting: Streamlit Cloud + GitHub CI/CD', new_x='RIGHT', new_y='LAST')
pdf.cell(85, 5, 'Security: SHA-256 Hashed Password Gate', new_x='LMARGIN', new_y='NEXT')

pdf.set_y(curr_y + 26)

# ══════════════════════════ SECTION 1: PROJECT INTRODUCTION ══════════════════════════
pdf.chapter_header('1', 'Project Overview & General Introduction')

pdf.question_box(
    1,
    'Please introduce your project in 1 minute.',
    'Our project is the "Student Performance Analysis System". It is a machine learning web application built using Python and Streamlit. '
    'It helps teachers and administrators evaluate student marks across 5 subjects, analyze attendance and study patterns, '
    'predict whether a student will fall in Low, Average, or High performance bands, and identify At-Risk students before final exams. '
    'It also includes interactive data visualization, dynamic PDF reports, and What-If analysis.',
    'Keep your answer under 60 seconds. Mention the domain (Educational Analytics), technology (Python & ML), and benefit (early warning for students).'
)

pdf.question_box(
    2,
    'What problem does your project solve?',
    'Traditional academic monitoring relies on end-of-semester results when it is too late to help failing students. '
    'Our system solves this by analyzing multiple continuous parameters (attendance, internals, assignment, practicals, study hours) '
    'to provide early predictions and actionable recommendations so teachers can intervene before exams.',
    'Focus on "proactive intervention" rather than just showing charts.'
)

pdf.question_box(
    3,
    'Who are the end users of this system?',
    'The primary end users are: '
    '(1) College faculties and academic mentors to track at-risk students, '
    '(2) Heads of Department (HODs) for subject-level passing rate comparisons, and '
    '(3) Students themselves to test "What-If" scenarios to see how study hours or attendance can boost their score.',
    'Demonstrates you thought about multiple real-world user personas.'
)

# ══════════════════════════ SECTION 2: WEB ARCHITECTURE & STREAMLIT ══════════════════════════
pdf.chapter_header('2', 'Architecture, Streamlit & Front-End Design')

pdf.question_box(
    4,
    'Why did you choose Streamlit instead of React with Django or Flask?',
    'Streamlit is purpose-built for Data Science and Machine Learning. '
    'It integrates natively with Pandas DataFrames and Plotly charts without requiring custom REST APIs or JavaScript frontend code. '
    'This allowed us to focus on data engineering, machine learning pipelines, and predictive algorithms rather than boilerplate web plumbing.',
    'Examiners love this answer because it proves you chose the right tool for an ML project rather than overcomplicating it.'
)

pdf.question_box(
    5,
    'How does Streamlit work behind the scenes?',
    'Streamlit uses a reactive Python execution model. Whenever a user interacts with a widget (e.g. moves a slider or selects a dropdown), '
    'Streamlit re-executes the Python script from top to bottom. To prevent slow operations like model training or data loading from '
    'running repeatedly, we use caching decorators (@st.cache_data and @st.cache_resource).',
    'Mentioning @st.cache_data proves you understand performance optimization.'
)

pdf.question_box(
    6,
    'How did you maintain state (e.g. login status, loaded data) across different pages?',
    'We used Streamlit\'s built-in session state dictionary: st.session_state. '
    'When a user logs in, we set st.session_state["logged_in"] = True. '
    'Similarly, processed student data is saved in st.session_state["processed_data"], ensuring it persists seamlessly across all 8 navigation pages.',
    'st.session_state is the standard answer for state management in Streamlit.'
)

pdf.question_box(
    7,
    'How does your authentication system work?',
    'We implemented a secure user gate in src/auth.py: '
    '1. User credentials (email and password) are submitted via Sign Up / Sign In forms. '
    '2. Passwords are never stored in plain text; we use hashlib.sha256() to create a one-way cryptographic hash. '
    '3. Hashes are stored in data/users.json. On login, the entered password is hashed and verified against the stored hash.',
    'Highlighting SHA-256 one-way hashing proves you followed security best practices.'
)

# ══════════════════════════ SECTION 3: DATA PREPROCESSING & DATASET ══════════════════════════
pdf.chapter_header('3', 'Dataset & Data Preprocessing Pipeline')

pdf.question_box(
    8,
    'Describe your dataset. What are the features and target variable?',
    'The dataset contains 515 student records. '
    'Features include: attendance_pct, internal_marks (50), assignment_marks (25), practical_marks (25), previous_sem_result (100), '
    'study_hours_per_day (0.5-8), and participation_score (1-10). '
    'Subject scores include: math, physics, programming, data_science, and statistics. '
    'The target variable is final_score (continuous for regression) and performance_category (Low, Average, High for classification).',
    'Distinguish clearly between input features and target labels.'
)

pdf.question_box(
    9,
    'How is the performance category defined?',
    'We categorized students based on their final score: '
    '- Low: final_score < 50 '
    '- Average: 50 <= final_score <= 75 '
    '- High: final_score > 75 '
    'This logic is implemented in get_performance_category() inside src/utils.py.',
    'Mention the exact thresholds (50 and 75).'
)

pdf.question_box(
    10,
    'What data preprocessing steps did you perform?',
    'In src/preprocessing.py: '
    '1. Duplicate Removal: Identified and dropped duplicate rows using df.drop_duplicates(). '
    '2. Missing Value Imputation: Handled null values using column-wise mean imputation for numerical values. '
    '3. Feature Normalization: Used StandardScaler to standardize numerical inputs. '
    '4. Categorical Encoding: Used LabelEncoder from scikit-learn to map Low, Average, and High to numeric labels (0, 1, 2).',
    'Standard ML pipeline: Cleaning -> Imputation -> Encoding -> Scaling.'
)

pdf.question_box(
    11,
    'Why is Feature Scaling (StandardScaler) necessary?',
    'Different features have different ranges; for example, attendance is 0 to 100, while study hours is 0.5 to 8. '
    'Distance-based algorithms like KNN and margin-based algorithms like SVM or Logistic Regression are sensitive to magnitude. '
    'Without scaling, a feature with large numbers would dominate the distance calculation. '
    'StandardScaler transforms each feature to have mean = 0 and standard deviation = 1 (z-score normalization).',
    'Explain the formula: z = (x - mean) / std. Tree models do not strictly need scaling, but KNN/SVM do.'
)

pdf.question_box(
    12,
    'How did you split the data for training and testing?',
    'We used train_test_split from scikit-learn with an 80:20 ratio (80% training, 20% testing). '
    'We also fixed random_state = 42 to ensure deterministic, reproducible results during evaluation.',
    'Examiners frequently ask "Why random_state=42?" Answer: to ensure reproducibility.'
)

# ══════════════════════════ SECTION 4: MACHINE LEARNING MODELS ══════════════════════════
pdf.chapter_header('4', 'Machine Learning Models & Algorithms')

pdf.question_box(
    13,
    'Which machine learning algorithms did you train and compare?',
    'We trained 5 classification models: '
    '(1) Logistic Regression, (2) Decision Tree, (3) Random Forest, (4) K-Nearest Neighbors (KNN), and (5) Support Vector Machine (SVM). '
    'For score prediction, we trained a Linear Regression model.',
    'Speak clearly and name all 5 classifiers + 1 regressor.'
)

pdf.question_box(
    14,
    'How does your system select the "Best Model"?',
    'No model is assumed to be the best in advance. '
    'Our system trains all 5 classifiers on the training set, evaluates each one independently on the 20% unseen test set, '
    'and automatically selects the classifier with the highest Test Accuracy score as the best model for live predictions.',
    'Examiners appreciate objective, data-driven model selection rather than hardcoding a favourite model.'
)

pdf.question_box(
    15,
    'Explain how Random Forest works and why it often beats a Decision Tree.',
    'A Decision Tree creates hierarchical if-else decision rules. While easy to interpret, it often overfits training data. '
    'Random Forest is an ensemble learning method (Bagging). It builds 100 different decision trees, each trained on random bootstrap samples '
    'and random feature subsets. The final prediction is determined by majority voting. This reduces variance and prevents overfitting.',
    'Keyword to use: Ensemble technique, Bagging, Majority Voting, Overfitting reduction.'
)

pdf.question_box(
    16,
    'How does Support Vector Machine (SVM) classify students?',
    'SVM finds the optimal hyperplane that separates the classes with the maximum margin (distance between the hyperplane and closest support vectors). '
    'For non-linearly separable student data, we use the Radial Basis Function (RBF) kernel to project features into a higher-dimensional space.',
    'Mention RBF kernel and maximum margin hyperplane.'
)

pdf.question_box(
    17,
    'How does K-Nearest Neighbors (KNN) make predictions?',
    'KNN is an instance-based, non-parametric algorithm. To classify a student, it calculates the Euclidean distance between their 7 normalized features '
    'and all students in the training dataset. It picks the k=5 closest neighbours and assigns the category with the majority vote.',
    'Mention: k=5, Euclidean distance, instance-based learning.'
)

pdf.question_box(
    18,
    'What is Feature Importance and how is it calculated?',
    'Feature importance measures how much each input feature contributes to predicting student performance. '
    'In Random Forest, it is calculated based on Mean Decrease in Impurity (Gini importance) across all 100 trees. '
    'In our system, attendance_pct and internal_marks consistently emerge as the most critical predictors of student success.',
    'Refer to the horizontal bar chart on Page 6 of your dashboard.'
)

# ══════════════════════════ SECTION 5: MODEL EVALUATION & METRICS ══════════════════════════
pdf.chapter_header('5', 'Model Evaluation & Performance Metrics')

pdf.question_box(
    19,
    'What metrics did you use to evaluate your classification models?',
    'We evaluated models using 4 key metrics: '
    '1. Accuracy: Overall percentage of correct predictions. '
    '2. Precision: Out of all students predicted as High, how many were actually High? (Minimizes false alarms). '
    '3. Recall (Sensitivity): Out of all truly High students, how many did the model detect? '
    '4. F1-Score: Harmonic mean of Precision and Recall: 2 * (Precision * Recall) / (Precision + Recall).',
    'Write down the F1 formula on paper if the examiner asks.'
)

pdf.question_box(
    20,
    'Why can Accuracy alone be misleading in real-world problems?',
    'If a dataset has severe class imbalance (e.g. 90% Average students and only 10% Low students), '
    'a dumb model that predicts "Average" for every student would achieve 90% accuracy, while failing completely at identifying struggling students. '
    'Therefore, Precision, Recall, and F1-Score are vital to ensure struggling (Low/At-Risk) students are accurately detected.',
    'Class imbalance is one of the most popular viva topics in machine learning.'
)

pdf.question_box(
    21,
    'What is a Confusion Matrix?',
    'A confusion matrix is an N x N table (here 3x3 for Low, Average, High) that summarizes model performance by comparing Actual vs Predicted classes. '
    'The diagonal elements represent correct predictions (True Positives), while off-diagonal elements show misclassifications. '
    'We plot an interactive heatmap of the confusion matrix for every model on the Model Comparison page.',
    'Mention that diagonals = correct classifications.'
)

pdf.question_box(
    22,
    'How did you evaluate the Linear Regression model?',
    'We used 3 regression metrics: '
    '1. MAE (Mean Absolute Error): Average absolute difference between predicted and actual final score (~4.6 marks). '
    '2. RMSE (Root Mean Squared Error): Penalizes larger errors more heavily (~5.9 marks). '
    '3. R-squared (R2) Score: Proportion of variance explained by the model (~0.93 or 93%), indicating an excellent fit.',
    'State your project\'s actual values: MAE ~4.6, RMSE ~5.9, R2 ~0.93.'
)

# ══════════════════════════ SECTION 6: APPLICATION FEATURES & ANALYSIS ══════════════════════════
pdf.chapter_header('6', 'Key Application Features & Implementation')

pdf.question_box(
    23,
    'What is the "What-If Analysis" on the Prediction page?',
    'What-If analysis allows students and mentors to simulate positive interventions. '
    'After the baseline prediction is shown, the system tests 4 hypothetical improvements: '
    '(1) Attendance +10%, (2) Study hours +1 hour, (3) Participation +2 points, and (4) Internal marks +5. '
    'It re-runs the model and displays immediate score deltas (e.g. +3.4 marks) as dynamic KPI cards.',
    'Explain how this provides prescriptive guidance, not just predictive numbers.'
)

pdf.question_box(
    24,
    'How do you identify and handle "At-Risk" students?',
    'On the Reports page, students are filtered by two risk conditions: '
    '- High Risk: Attendance < 75% AND Final Score < 50 '
    '- Medium Risk: Either Attendance < 75% OR Final Score < 50 '
    'The system displays an At-Risk table with color-coded warnings and includes a mandatory ethical disclaimer stating that '
    'this is an analytical indicator meant for supportive mentoring, not a permanent judgment of student ability.',
    'Highlighting ethical AI and disclaimers creates an impressive academic impression.'
)

pdf.question_box(
    25,
    'What is Inter-Subject Correlation and what did your analysis reveal?',
    'Using Pearson correlation matrix (displayed as a Plotly heatmap on the Subject Analysis page), we measured how scores in one subject relate to others. '
    'We observed strong positive correlations between Mathematics, Statistics, and Data Science, indicating that strong quantitative foundational skills '
    'directly improve computer science performance.',
    'Proves you actually analyzed the data findings.'
)

pdf.question_box(
    26,
    'How did you generate dynamic PDF reports?',
    'We used the fpdf2 Python library in views/7_Reports.py. '
    'When an administrator selects a student, the system extracts their marks, builds a styled PDF with header banners, '
    'profile details, component breakdown, subject score table, and mentor recommendations, and provides a direct download button.',
    'fpdf2 is clean and lightweight, requiring no external printer drivers.'
)

# ══════════════════════════ SECTION 7: DEPLOYMENT, LIMITATIONS & FUTURE SCOPE ══════════════════════════
pdf.chapter_header('7', 'Deployment, Limitations & Future Scope')

pdf.question_box(
    27,
    'How did you deploy this application to production?',
    'We used Streamlit Community Cloud integrated with GitHub: '
    '1. Code and dependencies (requirements.txt) are version-controlled in our GitHub repository (sahilpowar2007/Student-Performance-Analysis). '
    '2. Streamlit Cloud connects directly to the main branch. '
    '3. Whenever a new commit is pushed, GitHub Webhooks automatically trigger a CI/CD build and redeploy the live application.',
    'Mentioning Git CI/CD and automated webhooks shows modern DevOps knowledge.'
)

pdf.question_box(
    28,
    'What are the limitations of your current system?',
    'Current limitations include: '
    '1. Static Model: Models are trained in-memory during session startup rather than updated via a continuous real-time data stream. '
    '2. Synthetic Data: The dataset is simulated (515 records); real-world data would exhibit more noise and sociodemographic variables. '
    '3. Single Semester View: It currently predicts semester performance rather than multi-year cumulative CGPA progression.',
    'Acknowledging real limitations shows intellectual maturity and honesty.'
)

pdf.question_box(
    29,
    'What are your future enhancements for this project?',
    'Future scope includes: '
    '1. Integration with College ERP / LMS (e.g. Moodle, Canvas) via REST APIs for automatic daily attendance syncing. '
    '2. Multi-Semester Deep Learning (LSTM / RNNs) to model student learning trajectories across 4 years. '
    '3. Automated SMS/Email alerts sent directly to mentors and parents when a student enters the High Risk band.',
    'Shows visionary engineering thinking.'
)

pdf.question_box(
    30,
    'If the examiner asks you to show the live working demo, what will you demonstrate?',
    'We will walk through 4 key steps: '
    '1. Sign In at the authentication page. '
    '2. Show the Overview dashboard with KPI cards and Performance Distribution donut chart. '
    '3. Navigate to Page 5 (Prediction), move the attendance and study hour sliders, and click "Predict Performance" to show live ML inference and What-If analysis. '
    '4. Navigate to Page 7 (Reports) and download a real-time generated student PDF report.',
    'Having a 4-step demo route planned prevents hesitation in front of the examiner!'
)

# Output PDF
output_path = os.path.join(os.path.dirname(__file__), 'data', 'Most_Asked_Viva_Questions_and_Answers.pdf')
pdf.output(output_path)
print(f'Viva Guide PDF generated successfully at: {output_path}')
