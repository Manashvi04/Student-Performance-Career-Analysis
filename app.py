import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-12345")

# Supabase configuration (To be filled in .env)
# SUPABASE_URL=your_url
# SUPABASE_KEY=your_key
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# Initialize supabase if keys are provided
supabase: Client = None
if url and key:
    supabase = create_client(url, key)

@app.route('/')
def index():
    if 'user_role' in session:
        if session['user_role'] == 'student':
            return redirect(url_for('student_dashboard'))
        elif session['user_role'] == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        elif session['user_role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        role = request.form.get('role') # admin, faculty, student
        
        # NOTE: This is a mocked login block! 
        # In a real application with Supabase you would do something like:
        # if supabase:
        #     response = supabase.table('users').select('*').eq('id', user_id).eq('role', role).execute()
        #     user = response.data[0] if response.data else None
        #     if user and user['password'] == password: # (use hashed passwords!)
        #         session['user_id'] = user_id
        #         session['user_role'] = role
        #         return redirect(url_for('index'))
        
        # MOCK LOGIC for frontend preview purposes:
        if user_id and password:
            session['user_id'] = user_id
            session['user_role'] = role
            flash(f'Logged in successfully as {role}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    if session.get('user_role') != 'student':
        return redirect(url_for('login'))
    return render_template('student_dashboard.html', user_id=session.get('user_id'))

@app.route('/faculty')
def faculty_dashboard():
    if session.get('user_role') != 'faculty':
        return redirect(url_for('login'))
    return render_template('faculty_dashboard.html', user_id=session.get('user_id'))

@app.route('/admin')
def admin_dashboard():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', user_id=session.get('user_id'))

if __name__ == '__main__':
    app.run(debug=True)
