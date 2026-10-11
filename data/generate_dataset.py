import pandas as pd
import numpy as np
import random
import os

def generate_dataset():
    np.random.seed(42)
    random.seed(42)
    
    first_names = [
        'Aarav', 'Vihaan', 'Aditya', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya',
        'Atharva', 'Advik', 'Pranav', 'Kabir', 'Ritvik', 'Aryan', 'Dhruv', 'Darsh', 'Rohan', 'Abhinav',
        'Diya', 'Isha', 'Aanya', 'Priya', 'Ananya', 'Aaradhya', 'Kavya', 'Avni', 'Saanvi', 'Myra',
        'Prisha', 'Riya', 'Kiara', 'Navya', 'Mira', 'Snigdha', 'Sia', 'Nisha', 'Aisha', 'Aditi',
        'Roshni', 'Pooja', 'Shruti', 'Megha', 'Neha', 'Rohan', 'Amit', 'Anjali', 'Sneha', 'Rahul'
    ]
    last_names = [
        'Sharma', 'Patil', 'Deshmukh', 'Joshi', 'Kulkarni', 'Deshpande', 'Pawar', 'Jadhav', 'Gaikwad', 'Shinde',
        'Kadam', 'Kale', 'Mane', 'Bhosale', 'Yadav', 'Singh', 'Gupta', 'Kumar', 'Das', 'Roy',
        'Chowdhury', 'Mukherjee', 'Banerjee', 'Chatterjee', 'Bose', 'Ghosh', 'Sen', 'Dutta', 'Nair', 'Menon',
        'Pillai', 'Reddy', 'Rao', 'Iyer', 'Naidu', 'Gowda', 'Shetty', 'Hegde', 'Kamat', 'Prabhu',
        'Nayak', 'Shenoy', 'Baliga', 'Pai', 'Kini', 'Verma', 'Mishra', 'Tiwari', 'Pandey', 'Dubey'
    ]
    
    n_students = 500
    
    data = []
    for i in range(1, n_students + 1):
        student_id = f"STU{i:03d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        gender = random.choice(['Male', 'Female'])
        
        # Base factor for correlation
        student_aptitude = np.random.normal(0, 1)
        
        # Attendance (40 to 100)
        attendance_pct = np.clip(75 + student_aptitude * 15 + np.random.normal(0, 5), 40, 100)
        
        # Study hours (0.5 to 8)
        study_hours = np.clip(3 + student_aptitude * 2 + np.random.normal(0, 1), 0.5, 8.0)
        
        # Internal marks (10 to 50)
        internal = np.clip(30 + student_aptitude * 10 + np.random.normal(0, 5), 10, 50)
        
        # Assignment marks (5 to 25)
        assignment = np.clip(15 + student_aptitude * 5 + np.random.normal(0, 2.5), 5, 25)
        
        # Practical marks (5 to 25)
        practical = np.clip(15 + student_aptitude * 5 + np.random.normal(0, 2.5), 5, 25)
        
        # Previous sem (30 to 100)
        prev_sem = np.clip(65 + student_aptitude * 15 + np.random.normal(0, 10), 30, 100)
        
        # Participation (1 to 10)
        participation = np.clip(5 + student_aptitude * 2 + np.random.normal(0, 2), 1, 10)
        
        # Base subject score out of 100 based on components
        base_score = (internal + assignment + practical)
        
        # Subject scores (15 to 100) - correlated with base score and aptitude
        math_score = np.clip(base_score + np.random.normal(0, 10) + student_aptitude * 5, 15, 100)
        physics_score = np.clip(base_score + np.random.normal(0, 10) + student_aptitude * 4, 15, 100)
        programming_score = np.clip(base_score + np.random.normal(0, 8) + student_aptitude * 6 + study_hours * 2, 15, 100)
        data_science_score = np.clip(base_score + np.random.normal(0, 8) + student_aptitude * 7, 15, 100)
        statistics_score = np.clip(base_score + np.random.normal(0, 10) + student_aptitude * 5, 15, 100)
        
        final_score = np.mean([math_score, physics_score, programming_score, data_science_score, statistics_score])
        
        row = {
            'student_id': student_id,
            'name': name,
            'gender': gender,
            'attendance_pct': round(attendance_pct, 2),
            'internal_marks': round(internal, 2),
            'assignment_marks': round(assignment, 2),
            'practical_marks': round(practical, 2),
            'previous_sem_result': round(prev_sem, 2),
            'study_hours_per_day': round(study_hours, 2),
            'participation_score': round(participation, 2),
            'math_score': round(math_score, 2),
            'physics_score': round(physics_score, 2),
            'programming_score': round(programming_score, 2),
            'data_science_score': round(data_science_score, 2),
            'statistics_score': round(statistics_score, 2),
            'final_score': round(final_score, 2)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Add duplicate rows (~15)
    duplicates = df.sample(n=15, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Add missing values (3-5%)
    cols_to_corrupt = [col for col in df.columns if col not in ['student_id', 'name']]
    total_cells = df.shape[0] * len(cols_to_corrupt)
    num_missing = int(total_cells * 0.04)  # 4% missing
    
    for _ in range(num_missing):
        row_idx = np.random.randint(0, df.shape[0])
        col_name = np.random.choice(cols_to_corrupt)
        df.at[row_idx, col_name] = np.nan
        
    # Save dataset
    out_dir = os.path.dirname(__file__)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'student_performance.csv')
    df.to_csv(out_path, index=False)
    print(f"Dataset generated at {out_path} with {df.shape[0]} rows and {df.shape[1]} columns.")

if __name__ == "__main__":
    generate_dataset()
