from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import joblib
import pyodbc
from config import supabase


app = Flask(__name__)

# Load the saved model and scaler
model = joblib.load('Classifier_model3.pkl')
scaler = joblib.load("scaler3.pkl")

# Career labels
career_labels = {
    0: "Software Engineer", 1: "Business Owner", 2: "Unknown", 3: "Banker",
    4: "Lawyer", 5: "Accountant", 6: "Doctor", 7: "Real Estate Developer",
    8: "Stock Investor", 9: "Construction Engineer", 10: "Artist",
    11: "Game Developer", 12: "Government Officer", 13: "Teacher",
    14: "Designer", 15: "Scientist", 16: "Writer"
}

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# ----------------- Prediction Page -------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Text-to-numeric mappings
        gender_map = {'Male': 0, 'Female': 1}
        job_map = {'No': 0, 'Yes': 1}
        extra_map = {'No': 0, 'Yes': 1}

        # Collect and convert basic inputs
        gender = gender_map[request.form['gender']]
        part_time_job = job_map[request.form['part_time_job']]
        absence_days = int(request.form['absence_days'])
        extracurricular_activities = extra_map[request.form['extracurricular_activities']]
        self_study_hours = int(request.form['weekly_self_study_hours'])

        # Initialize scores with default 0
        subjects = ['math_score', 'history_score', 'physics_score', 'chemistry_score',
                    'biology_score', 'english_score', 'geography_score']
        scores = {subject: 0.0 for subject in subjects}

        # Collect subject scores
        for key in request.form:
            if key.startswith("subject_") and key.endswith("_name"):
                idx = key.split("_")[1]
                subject_key = request.form[key]  # e.g., 'math_score'
                score_val = float(request.form.get(f"subject_{idx}_score", 0))
                scores[subject_key] = score_val

        # Calculate average score
        average_score = np.mean(list(scores.values()))

        # Prepare input
        input_data = [
            gender,
            part_time_job,
            absence_days,
            extracurricular_activities,
            self_study_hours,
            scores['math_score'],
            scores['history_score'],
            scores['physics_score'],
            scores['chemistry_score'],
            scores['biology_score'],
            scores['english_score'],
            scores['geography_score'],
            average_score  # 13th feature
        ]

        input_df = pd.DataFrame([input_data], columns=[
            'gender', 'part_time_job', 'absence_days',
            'extracurricular_activities', 'weekly_self_study_hours',
            'math_score', 'history_score', 'physics_score',
            'chemistry_score', 'biology_score', 'english_score',
            'geography_score', 'average_score'
        ])

        # Scale and predict
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]

        # Map prediction to career name
        career = career_labels.get(prediction, "Unknown Career")

        return render_template('index.html', prediction_text=f'Predicted Career: {career}')

    return render_template('index.html')


# ----------------- Student Data Management -------------------
@app.route('/student_data')
def student_data():
    response = supabase.table("student_data").select("*").limit(5000).order("student_id", desc=True).execute()
    students = response.data
    return render_template('student_data.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "gender": request.form['gender']
    }
    supabase.table("student_data").insert(data).execute()
    return redirect(url_for('student_data'))

@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    updated_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "gender": request.form['gender']
    }
    supabase.table("student_data").update(updated_data).eq("student_id", student_id).execute()
    return redirect(url_for('student_data'))

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    supabase.table("student_data").delete().eq("student_id", student_id).execute()
    return redirect(url_for('student_data'))

# ----------------- Academic Info Management -------------------
@app.route('/academic_info')
def academic_info():
    response = supabase.table("academic_info").select("*").limit(5000).order("record_id", desc=True).execute()
    academics = response.data
    return render_template('academic_info.html', academics=academics)

@app.route('/add_academic', methods=['POST'])
def add_academic():
    data = {
        "student_id": request.form['student_id'],
        "absence_days": request.form['absence_days'],
        "part_time_job": request.form['part_time_job'],
        "extracurricular_activities": request.form['extracurricular_activities'],
        "weekly_self_study_hours": request.form['weekly_self_study_hours'],
        "career_aspiration": request.form['career_aspiration']
    }
    supabase.table("academic_info").insert(data).execute()
    return redirect(url_for('academic_info'))

@app.route('/update_academic/<int:record_id>', methods=['POST'])
def update_academic(record_id):
    updated_data = {
        "absence_days": request.form['absence_days'],
        "part_time_job": request.form['part_time_job'],
        "extracurricular_activities": request.form['extracurricular_activities'],
        "weekly_self_study_hours": request.form['weekly_self_study_hours'],
        "career_aspiration": request.form['career_aspiration']
    }
    supabase.table("academic_info").update(updated_data).eq("record_id", record_id).execute()
    return redirect(url_for('academic_info'))

@app.route('/delete_academic/<int:record_id>')
def delete_academic(record_id):
    supabase.table("academic_info").delete().eq("record_id", record_id).execute()
    return redirect(url_for('academic_info'))

# ----------------- Subjects Management -------------------
@app.route('/subjects')
def subjects():
    response = supabase.table("subjects").select("*").limit(5000).order("id", desc=True).execute()
    subjects = response.data
    return render_template('subjects.html', subjects=subjects)

@app.route('/add_subject', methods=['POST'])
def add_subject():
    data = {
        "student_id": request.form['student_id'],
        "math_score": request.form['math_score'],
        "history_score": request.form['history_score'],
        "physics_score": request.form['physics_score'],
        "chemistry_score": request.form['chemistry_score'],
        "biology_score": request.form['biology_score'],
        "english_score": request.form['english_score'],
        "geography_score": request.form['geography_score']
    }
    supabase.table("subjects").insert(data).execute()
    return redirect(url_for('subjects'))

@app.route('/update_subject/<int:id>', methods=['POST'])
def update_subject(id):
    updated_data = {
        "math_score": request.form['math_score'],
        "history_score": request.form['history_score'],
        "physics_score": request.form['physics_score'],
        "chemistry_score": request.form['chemistry_score'],
        "biology_score": request.form['biology_score'],
        "english_score": request.form['english_score'],
        "geography_score": request.form['geography_score']
    }
    supabase.table("subjects").update(updated_data).eq("id", id).execute()
    return redirect(url_for('subjects'))

@app.route('/delete_subject/<int:id>')
def delete_subject(id):
    supabase.table("subjects").delete().eq("id", id).execute()
    return redirect(url_for('subjects'))

if __name__ == "__main__":
    app.run(debug=True)
