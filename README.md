STUDENT MANAGEMENT SYSTEM
=========================

A web-based student management application built with Flask. It allows administrators to manage student records, course enrollments, and predict students' career aspirations using a machine learning classifier.

Live Demo:
https://student-management-system-lyc7.onrender.com


REPOSITORY STRUCTURE
---------------------
Student-Management-System/
│
├── src/                        → Source code and assets
│   ├── static/                 → CSS, JavaScript, etc.
│   ├── templates/              → HTML templates
│   ├── Classifier_model3.pkl   → Trained ML classifier and scaler
|   ├── scaler3.pkl             → Trained ML classifier and scaler
│   ├── app.py                  → Main Flask application
│   ├── config.py               → App configuration
├── requirements.txt            → Python dependencies
├── README.txt                  → Project overview and instructions


PREREQUISITES
-------------
- Python 3.6 or later
- pip
- Git
- (Optional) virtualenv for isolated environments


GETTING STARTED (SOURCE CODE SETUP)
-----------------------------------

1. Clone the repository:
   git clone https://github.com/Aliyah-Dawood/Student-Management-System.git
   cd Student-Management-System

2. Create a virtual environment:

   On Windows:
   python -m venv venv
   venv\Scripts\activate

   On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Install required packages:
   pip install -r requirements.txt

4. Ensure ML model files are present in src:
   - Classifier_model3.pkl
   - scaler3.pkl

5. Run the Flask app:
   cd src
   python app.py

6. Open your browser and go to:
   http://127.0.0.1:5000/

CONFIGURATION
-------------
Edit the file at src/config.py to update:
- Secret key
- Debug mode
- Database URI (SQLite by default)


TROUBLESHOOTING
---------------
- If you get ModuleNotFoundError: run 'pip install -r requirements.txt' again
- If the port is already in use: run 'python app.py --port 5001'
- If app isn't loading: make sure you're running from inside the src/ directory
- Make Sure to enter the Gender field in Student Data page with Capital letter :"Male / Female"


