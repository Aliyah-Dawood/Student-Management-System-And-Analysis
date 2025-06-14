from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import joblib
import pyodbc
from config import supabase


app = Flask(__name__)

# Load the saved model and scaler
model = joblib.load('Classifier_model3 (2).pkl')
scaler = joblib.load("scaler3 (2).pkl")

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
        try:
            # Maps
            gender_map = {'Male': 0, 'Female': 1}
            job_map = {'No': 0, 'Yes': 1}
            extra_map = {'No': 0, 'Yes': 1}

            # Inputs
            gender = gender_map[request.form['gender']]
            absence_days = int(request.form['absence_days'])
            part_time_job = job_map[request.form['part_time_job']]
            extracurricular_activities = extra_map[request.form['extracurricular_activities']]
            self_study_hours = int(request.form['weekly_self_study_hours'])

            # Subject scores
            subjects = ['math_score', 'history_score', 'physics_score', 'chemistry_score',
                        'biology_score', 'english_score', 'geography_score']
            scores = {subject: 0.0 for subject in subjects}

            for key in request.form:
                if key.startswith("subject_") and key.endswith("_name"):
                    idx = key.split("_")[1]
                    subject_key = request.form[key]
                    score_val = float(request.form.get(f"subject_{idx}_score", 0))
                    scores[subject_key] = score_val

            average_score = sum(scores.values()) / len(scores)

            # Match trained model’s feature order exactly:
            expected_order = [
                'gender', 'math_score', 'history_score', 'physics_score', 'chemistry_score',
                'biology_score', 'english_score', 'geography_score', 'absence_days',
                'part_time_job', 'extracurricular_activities', 'weekly_self_study_hours',
                'average_score'
            ]

            input_data = [[
                gender,
                scores['math_score'], scores['history_score'], scores['physics_score'],
                scores['chemistry_score'], scores['biology_score'], scores['english_score'],
                scores['geography_score'], absence_days,
                part_time_job, extracurricular_activities, self_study_hours,
                average_score
            ]]

            input_df = pd.DataFrame(input_data, columns=expected_order)

            # Transform and predict
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
            career = career_labels.get(prediction, "Unknown Career")

            return render_template('index.html', prediction_text=f'Predicted Career: {career}')
        
        except Exception as e:
            return f"Error during prediction: {e}"

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
    job_map = {'No': 0, 'Yes': 1}
    extra_map = {'No': 0, 'Yes': 1}
    data = {
        "student_id": request.form['student_id'],
        "absence_days": request.form['absence_days'],
        "part_time_job": job_map[request.form['part_time_job']],
        "extracurricular_activities": extra_map[request.form['extracurricular_activities']],
        "weekly_self_study_hours": request.form['weekly_self_study_hours'],
        "career_aspiration": request.form['career_aspiration']
    }
    supabase.table("academic_info").insert(data).execute()
    return redirect(url_for('academic_info'))

@app.route('/update_academic/<int:record_id>', methods=['POST'])
def update_academic(record_id):
    job_map = {'No': 0, 'Yes': 1}
    extra_map = {'No': 0, 'Yes': 1}
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

# ----------------- Visualization Page -------------------
@app.route('/visualizations')
def visualizations():
    try:
        import matplotlib
        matplotlib.use('Agg')

        import matplotlib.pyplot as plt
        import seaborn as sns
        import io
        import base64
        import pandas as pd
        from config import supabase

        images = []

        # ---------- Plot 1: Top vs Bottom Performers ----------
        subjects_data = supabase.table("subjects").select("*").limit(100).execute().data
        students_data = supabase.table("student_data").select("student_id, first_name, last_name").execute().data

        df1 = pd.DataFrame(subjects_data)
        students_df = pd.DataFrame(students_data)

        df1 = df1.merge(students_df, on='student_id')
        df1['student_name'] = df1['first_name'] + ' ' + df1['last_name']
        df1['average_score'] = df1[["math_score", "geography_score", "english_score",
                                    "physics_score", "chemistry_score", "biology_score"]].mean(axis=1)

        top_10 = df1.nlargest(10, "average_score").copy().sort_values(by="average_score", ascending=False)
        bottom_10 = df1.nsmallest(10, "average_score").copy().sort_values(by="average_score", ascending=False)
        top_10["category"] = "Top 10"
        bottom_10["category"] = "Bottom 10"

        df_combined = pd.concat([top_10, bottom_10], ignore_index=True)
        df_combined["student_name"] = pd.Categorical(df_combined["student_name"],
                                                     categories=df_combined["student_name"],
                                                     ordered=True)

        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.barplot(x="average_score", y="student_name", hue="category", data=df_combined,
                    palette={"Top 10": "green", "Bottom 10": "red"}, ax=ax1)
        ax1.set_title("Top 10 vs. Bottom 10 Performers")
        ax1.set_xlabel("Average Score")
        ax1.set_ylabel("Student Name")
        ax1.legend(title="Category")
        ax1.grid(True, linestyle="--", alpha=0.6)

        buf1 = io.BytesIO()
        plt.tight_layout()
        fig1.savefig(buf1, format="png")
        buf1.seek(0)
        images.append(base64.b64encode(buf1.read()).decode("utf-8"))
        plt.close(fig1)

        # ---------- Plot 2: Absence vs Performance ----------
        academic_data = supabase.table("academic_info").select("absence_days, student_id").execute().data
        scores_data = supabase.table("subjects").select(
            "student_id, math_score, geography_score, english_score, physics_score, chemistry_score, biology_score"
        ).execute().data

        df_abs = pd.DataFrame(academic_data)
        df_scores = pd.DataFrame(scores_data)
        df2 = pd.merge(df_abs, df_scores, on="student_id")
        df2["avg_score"] = df2[["math_score", "geography_score", "english_score", "physics_score", "chemistry_score", "biology_score"]].mean(axis=1)

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.scatter(df2['absence_days'], df2['avg_score'], color='b', alpha=0.6)
        ax2.set_xlabel("Absence Days")
        ax2.set_ylabel("Average Academic Score")
        ax2.set_title("Absence Days vs. Academic Performance")
        ax2.grid(True)
        buf2 = io.BytesIO()
        plt.tight_layout()
        fig2.savefig(buf2, format="png")
        buf2.seek(0)
        images.append(base64.b64encode(buf2.read()).decode("utf-8"))
        plt.close(fig2)

        # ---------- Plot 3: Career Aspirations ----------
        df3 = pd.DataFrame(supabase.table("academic_info").select("career_aspiration").execute().data)
        career_counts = df3['career_aspiration'].value_counts()
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=career_counts.index, y=career_counts.values, palette="viridis", ax=ax3)
        ax3.set_xlabel("Career Aspiration")
        ax3.set_ylabel("Number of Students")
        ax3.set_title("Career Aspirations Breakdown")
        ax3.tick_params(axis='x', rotation=60)
        buf3 = io.BytesIO()
        plt.tight_layout()
        fig3.savefig(buf3, format="png")
        buf3.seek(0)
        images.append(base64.b64encode(buf3.read()).decode("utf-8"))
        plt.close(fig3)

        # ---------- Plot 4: Subject Score Distribution ----------
        df4 = pd.DataFrame(supabase.table("subjects").select(
            "math_score, geography_score, english_score, physics_score, chemistry_score, biology_score"
        ).execute().data)
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df4, ax=ax4)
        ax4.set_title("Subjects Score Distribution (Boxplot)")
        ax4.tick_params(axis='x', rotation=45)
        buf4 = io.BytesIO()
        plt.tight_layout()
        fig4.savefig(buf4, format="png")
        buf4.seek(0)
        images.append(base64.b64encode(buf4.read()).decode("utf-8"))
        plt.close(fig4)

        return render_template('visualizations.html', plots=images)

    except Exception as e:
        return f"<h2>Internal Server Error</h2><p>{str(e)}</p>"
if __name__ == "__main__":
    app.run(debug=True)
