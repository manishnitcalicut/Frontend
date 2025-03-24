
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def connect_db():
    """Connects to the SQLite database."""
    return sqlite3.connect("results_final.db", check_same_thread=False)

def check_student(roll_number, dob):
    """Checks if the student exists in the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_data WHERE roll_number = ? AND dob = ?", (roll_number, dob))
        return cursor.fetchone()  # Returns student details if found

# 
def get_student_result(roll_number, exam_type):
    """Fetches student results and calculates total marks and percentage correctly."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Get exam_id
        cursor.execute("SELECT exam_id FROM exams WHERE exam_name = ?", (exam_type,))
        exam_data = cursor.fetchone()
        if not exam_data:
            return [], 0, 0  # No exam found

        exam_id = exam_data[0]

        # Get student result
        cursor.execute("SELECT subject, marks FROM student_results WHERE roll_number = ? AND exam_id = ?", (roll_number, exam_id))
        result = cursor.fetchall()

    # Handle empty results
    if not result:
        return [], 0, 0

    # Check marks for Hindi and Sanskrit
    subject_marks = {subject.lower(): marks for subject, marks in result}

    # Remove Hindi if Sanskrit has 0 marks
    if subject_marks.get("sanskrit") == 0:
        result = [(subject, marks) for subject, marks in result if subject.lower() != "sanskrit"]

    # Remove Sanskrit if Hindi has 0 marks
    if subject_marks.get("hindi") == 0:
        result = [(subject, marks) for subject, marks in result if subject.lower() != "hindi"]

    # Calculate total marks
    total_marks = sum(marks for _, marks in result)

    # Consider only subjects with marks > 0
    valid_subjects = [marks for _, marks in result if marks > 0]
    total_subjects = len(valid_subjects)

    # 🔹 Determine full marks per subject
    if "term" in exam_type.lower():  # Term 1 or Term 2
        full_marks_per_subject = 100
    else:  # PT1 or PT2
        full_marks_per_subject = 50

    # 🔹 Calculate percentage
    percentage = (sum(valid_subjects) / (total_subjects * full_marks_per_subject)) * 100 if total_subjects > 0 else 0
    percentage = round(percentage, 2)  # Limit to 2 decimal places

    return result, total_marks, percentage

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/<exam_type>", methods=["GET", "POST"])
def login(exam_type):
    if request.method == "POST":
        roll_no = request.form["roll_number"].strip()
        dob_input = request.form["dob"]

        # Convert input DOB from YYYY-MM-DD to DD-MM-YYYY
        dob = datetime.strptime(dob_input, "%Y-%m-%d").strftime("%d-%m-%Y")

        student = check_student(roll_no, dob)
        results, total_marks, percentage = get_student_result(roll_no, exam_type)

        if student and results:
            return render_template("Result.html", student=student, results=results, exam_type=exam_type,
                                   total_marks=total_marks, percentage=percentage)
        else:
            return render_template("login.html", exam_type=exam_type, error="❌ Invalid Roll Number or No Result Found!")

    return render_template("login.html", exam_type=exam_type)

if __name__ == "__main__":
    app.run(debug=True)
