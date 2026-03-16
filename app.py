from flask import Flask, render_template, request, redirect, session
import config
import pandas as pd
from flask import request, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "student_performance_secret"

# Home page
@app.route('/')
def home():
    return render_template("homepage.html")


# Login page
@app.route('/login')
def login_page():
    return render_template("login.html")


# Login logic
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = config.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        session['id'] = user[0]   # store name
        role = user[0]

        if role == "admin":
            return redirect("/admin")
        elif role == "faculty":
            return redirect("/faculty")
        else:
            return redirect("/student")

    return "Invalid Login"


# Dashboards
@app.route('/admin')
def admin():
    return render_template("admin/a_dashboard.html")


@app.route('/faculty')
def faculty():
    return render_template("faculty/f_dashboard.html")


@app.route('/student')
def student():
    return render_template("student/s_dashboard.html")


# Student pages
@app.route('/performance_analysis')
def performance_analysis():
    return render_template("student/performance_analysis.html")

@app.route('/career_trajectory')
def career_trajectory():
    return render_template("student/career_trajectory.html")

@app.route("/s_profile")
def student_profile():
    return render_template("student/s_profile.html")

@app.route("/attendance_s")
def attendance_s():
    return render_template("student/attendance_s.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

#Faculty pages 
@app.route('/faculty_dashboard')
def faculty_dashboard():
    return render_template('faculty/f_dashboard.html')

@app.route('/students')
def students():
    return render_template('faculty/students.html')

@app.route('/upload_marks')
def upload_marks():
    return render_template('faculty/upload_marks.html')

@app.route('/analytics')
def analytics():
    return render_template('faculty/analytics.html')

@app.route('/attendance_f')
def attendance():
    return render_template('faculty/attendance_f.html')

@app.route('/f_profile')
def f_profile():
    return render_template('faculty/f_profile.html')

#Admin pages

@app.route("/a_dashboard")
def a_dashboard():
    return render_template("admin/a_dashboard.html")

@app.route("/upload")
def upload():
    return render_template("admin/upload.html")

@app.route("/a_analytics")
def a_analytics():
    return render_template("admin/a_analytics.html")

@app.route("/a_users")
def a_users():
    return render_template("admin/a_users.html")

#upload
@app.route("/admin/upload_students_excel", methods=["POST"])
def upload_students_excel():

    file = request.files["file"]
    dept_name = request.form["department"]
    year_value = request.form["year"]

    import pandas as pd
    df = pd.read_excel(file)

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    inserted = 0

    # Get dept_id
    cursor.execute("SELECT dept_id FROM departments WHERE dept_name = ?", dept_name)
    dept_row = cursor.fetchone()
    dept_id = dept_row[0]

    # Get year_id
    cursor.execute("SELECT year_id FROM academic_years WHERE year = ?", year_value)
    year_row = cursor.fetchone()
    year_id = year_row[0]

    for _, row in df.iterrows():

        student_id = str(row["CollegeID"])
        name = row["Name"]
        dob = row["DOB"]
        program = row["Program"]
        admission_date = row["AdmissionDate"]

        # Generate Email
        email = student_id.lower() + "@charusat.edu.in"

        # Password
        password = student_id

        # Insert student data
        cursor.execute("""
        INSERT INTO students
        (student_id, name, dob, dept_id, year_id, program, admission_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        student_id, name, dob, dept_id, year_id, program, admission_date)

        # Insert login credentials
        cursor.execute("""
        INSERT INTO users (id, email, password, role)
        VALUES (?, ?, ?, ?)
        """,
        student_id, email, password, "student")

        inserted += 1

    conn.commit()

    return jsonify({"message": f"{inserted} students uploaded successfully"})
if __name__ == "__main__":
    app.run(debug=True)