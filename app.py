from flask import Flask, render_template, request, redirect, session, jsonify
import config
import pandas as pd

app = Flask(__name__)
app.secret_key = "student_performance_secret"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("homepage.html")


# ---------------- LOGIN ----------------
@app.route('/login')
def login_page():
    return render_template("login.html")


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
        role = user[0]
        session['role'] = role
        session['user_email'] = email   # ✅ IMPORTANT

        if role == "admin":
            return redirect("/admin")
        elif role == "faculty":
            return redirect("/faculty")
        else:
            return redirect("/student")

    return render_template("login.html", error="⚠ Invalid credentials")


# ---------------- DASHBOARDS ----------------
@app.route('/admin')
def admin():
    return render_template("admin/a_dashboard.html")


@app.route('/faculty')
def faculty():
    return render_template("faculty/f_dashboard.html")


@app.route('/student')
def student():
    return render_template("student/s_dashboard.html")


# ---------------- STUDENT PAGES ----------------
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


# ---------------- FACULTY PAGES ----------------
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


# ---------------- ADMIN ----------------
@app.route("/a_dashboard")
def a_dashboard():
    return render_template("admin/a_dashboard.html")


@app.route("/a_analytics")
def a_analytics():
    return render_template("admin/a_analytics.html")


@app.route("/a_users")
def a_users():
    return render_template("admin/a_users.html")


@app.route("/upload")
def upload_page():
    conn = config.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT year FROM academic_years ORDER BY year DESC")
    years = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template("admin/upload.html", years=years)


# ---------------- UPLOAD EXCEL ----------------
@app.route("/admin/upload_students_excel", methods=["POST"])
def upload_students_excel():

    print("API CALLED")

    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"message": "No file uploaded"}), 400

        dept_name = request.form.get("department")
        year_value = request.form.get("year")

        print("Dept:", dept_name, "Year:", year_value)

        df = pd.read_excel(file)
        df.columns = df.columns.str.strip().str.replace(" ", "")

        print("Columns:", df.columns)
        print("Total Rows:", len(df))

        conn = config.get_connection()
        cursor = conn.cursor()

        inserted = 0

        # Department
        cursor.execute(
            "SELECT dept_id FROM departments WHERE LOWER(dept_name)=LOWER(?)",
            dept_name
        )
        dept_row = cursor.fetchone()

        if not dept_row:
            cursor.execute("INSERT INTO departments (dept_name) VALUES (?)", dept_name)
            conn.commit()
            cursor.execute(
                "SELECT dept_id FROM departments WHERE LOWER(dept_name)=LOWER(?)",
                dept_name
            )
            dept_row = cursor.fetchone()

        dept_id = dept_row[0]

        # Year
        cursor.execute("SELECT year_id FROM academic_years WHERE year=?", year_value)
        year_row = cursor.fetchone()

        if not year_row:
            return jsonify({"message": "Invalid year"}), 400

        year_id = year_row[0]

        # Insert students
        for _, row in df.iterrows():
            try:
                student_id = str(row.get("CollegeID"))
                name = row.get("Name")
                dob = row.get("DOB")
                program = row.get("Program")
                admission_date = row.get("AdmissionDate")

                if not student_id or student_id == "nan":
                    continue

                email = student_id.lower() + "@charusat.edu.in"
                password = student_id

                cursor.execute("""
                INSERT INTO students
                (student_id, name, dob, dept_id, year_id, program, admission_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                student_id, name, dob, dept_id, year_id, program, admission_date)

                cursor.execute("""
                INSERT INTO users (id, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                student_id, email, password, "student")

                inserted += 1

            except Exception as e:
                print("Row Error:", e)
                continue

        conn.commit()
        conn.close()

        return jsonify({"message": f"{inserted} students uploaded successfully"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# ---------------- GET PROFILE ----------------
@app.route("/student/get_profile")
def get_profile():

    email = session.get("user_email")

    conn = config.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        s.student_id,
        s.name,
        s.dob,
        u.email,
        d.dept_name AS branch,
        a.year,
        s.program,
        s.admission_date,

        p.father_name,
        p.mother_name,
        p.parent_phone,
        p.student_phone,
        p.blood_group,
        p.admission_year,
        p.tenth_percent,
        p.twelfth_percent,
        p.acpc_rank,
        p.guardian_name,
        p.guardian_phone,
        p.guardian_occupation,
        p.guardian_qualification,
        p.guardian_relation,
        p.guardian_address

    FROM users u
    JOIN students s ON u.id = s.student_id
    LEFT JOIN student_profiles p ON s.student_id = p.student_id
    JOIN departments d ON s.dept_id = d.dept_id
    JOIN academic_years a ON s.year_id = a.year_id

    WHERE u.email = ?
    """, email)

    row = cursor.fetchone()

    if not row:
        return jsonify({})

    columns = [col[0] for col in cursor.description]
    data = dict(zip(columns, row))

    conn.close()

    return jsonify(data)


# ---------------- UPDATE PROFILE ----------------
@app.route("/student/update_profile", methods=["POST"])
def update_profile():

    data = request.json
    email = session.get("user_email")

    conn = config.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email=?", email)
    student_id = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM student_profiles WHERE student_id=?", student_id)
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
        UPDATE student_profiles SET
            father_name=?, mother_name=?, parent_phone=?, student_phone=?,
            blood_group=?, admission_year=?, tenth_percent=?, twelfth_percent=?,
            acpc_rank=?, guardian_name=?, guardian_phone=?,
            guardian_occupation=?, guardian_qualification=?,
            guardian_relation=?, guardian_address=?
        WHERE student_id=?
        """,
        data.get("father_name"),
        data.get("mother_name"),
        data.get("parent_phone"),
        data.get("student_phone"),
        data.get("blood_group"),
        data.get("admission_year"),
        data.get("tenth_percent"),
        data.get("twelfth_percent"),
        data.get("acpc_rank"),
        data.get("guardian_name"),
        data.get("guardian_phone"),
        data.get("guardian_occupation"),
        data.get("guardian_qualification"),
        data.get("guardian_relation"),
        data.get("guardian_address"),
        student_id)
    else:
        cursor.execute("""
        INSERT INTO student_profiles (
            student_id, father_name, mother_name, parent_phone,
            student_phone, blood_group, admission_year,
            tenth_percent, twelfth_percent, acpc_rank,
            guardian_name, guardian_phone, guardian_occupation,
            guardian_qualification, guardian_relation, guardian_address
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        student_id,
        data.get("father_name"),
        data.get("mother_name"),
        data.get("parent_phone"),
        data.get("student_phone"),
        data.get("blood_group"),
        data.get("admission_year"),
        data.get("tenth_percent"),
        data.get("twelfth_percent"),
        data.get("acpc_rank"),
        data.get("guardian_name"),
        data.get("guardian_phone"),
        data.get("guardian_occupation"),
        data.get("guardian_qualification"),
        data.get("guardian_relation"),
        data.get("guardian_address"))

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile updated successfully"})

@app.route("/student/change_password", methods=["POST"])
def change_password():

    data = request.json
    email = session.get("user_email")

    conn = config.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email=?",
        email
    )

    current = cursor.fetchone()[0]

    if current != data.get("old_password"):
        return jsonify({"message": "Old password incorrect ❌"})

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        data.get("new_password"), email
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Password changed successfully ✅"})

@app.route("/student/dashboard_data")
def dashboard_data():

    email = session.get("user_email")

    conn = config.get_connection()
    cursor = conn.cursor()

    # Get student_id
    cursor.execute("SELECT id FROM users WHERE email=?", email)
    student_id = cursor.fetchone()[0]

    # 🔹 Marks
    cursor.execute("""
    SELECT subject, marks FROM marks WHERE student_id=?
    """, student_id)

    marks_data = cursor.fetchall()

    subjects = [row[0] for row in marks_data]
    marks = [row[1] for row in marks_data]

    # 🔹 Attendance trend
    cursor.execute("""
    SELECT semester, attendance_percent 
    FROM attendance WHERE student_id=? ORDER BY semester
    """, student_id)

    att_data = cursor.fetchall()

    semesters = [f"Sem{row[0]}" for row in att_data]
    attendance = [row[1] for row in att_data]

    # 🔹 Avg attendance
    avg_att = sum(attendance)/len(attendance) if attendance else 0

    # 🔹 CGPA (simple logic)
    cgpa = round(sum(marks)/len(marks)/10,2) if marks else 0

    # 🔹 Performance label
    performance = "Excellent" if cgpa >= 8 else "Good" if cgpa >= 6 else "Average"

    conn.close()

    return jsonify({
        "subjects": subjects,
        "marks": marks,
        "semesters": semesters,
        "attendance": attendance,
        "avg_attendance": round(avg_att,2),
        "cgpa": cgpa,
        "performance": performance
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)