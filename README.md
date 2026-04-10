# 🎓 EduTrack Analytics: Student Performance & Career Trajectory System

A sophisticated, full-stack predictive academic tracking platform designed to bridge the gap between B.Tech academic performance and real-world career mapping. Built with a focus on high-agency "Bento 2.0" design aesthetics and data-dense interactions.

---

## ⚡ Features

### 🏢 System Administration
- **Batch Provisioning:** Admins can mass-upload students via CSV, instantly generating secured access credentials.
- **Rollout Engine:** Automated cohort progression systems to progress student semesters efficiently based on passing criteria.
- **Global Overview:** High-level Chart.js integration monitoring macro institutional performance and demographics.

### 👨‍🏫 Faculty Operations
- **Bulk Data Intake:** Clean interface for professors to upload semester grade markers via CSV directly to the Supabase database.
- **Roster Directories:** Effortlessly browse specific department rosters to evaluate granular, sub-level performance metrics isolated by major.

### 🧑‍🎓 Student Portal
- **Holistic Tracking:** Unifies Academic CGPA tracking with Co-Curricular & Extra-Curricular engagement mapping.
- **🧠 AI Career Trajectory Engine:** Leverages a `Scikit-Learn` Random Forest Machine Learning model to calculate probabilities and align a student's internal metrics against optimal future career funnels (e.g., Software Engineering, Data Science, Product Management).
- **Skill Assessment Grids:** Radar charts mapping quantifiable metrics across core competencies. 
- **Real-World Transcripts:** Official 1-click CSV Transcript generation available from the profile view.

---

## 🛠️ Technology Stack

**Backend Architecture:**
- **Python 3 / Flask:** Lightweight, robust routing framework.
- **Supabase (PostgreSQL):** Serverless Backend-as-a-Service handling relational databases safely via `supabase-py`.
- **Pandas:** Powerful dataframe manipulation for bulk CSV uploads and Transcript generation.
- **Scikit-Learn / Joblib:** Core Machine Learning infrastructure hosting the Career Prediction algorithms.

**Frontend Engineering:**
- **HTML5 / Vanilla CSS:** Strict reliance on native cascading styles avoiding heavy CSS frameworks to maintain complete control over the UI components.
- **Bento 2.0 Aesthetics:** Deep diffusion shadowing, massive `2.5rem` radiuses, high-contrast typography, and zero "AI Slop" layouts.
- **Phosphor Vector Icons:** Crisp, consistent iconography for professional visual density.
- **Outfit Font:** Utilizing optimized typographical scaling.

---

## 🚀 Setup & Installation Environment

### 1. Clone the Repository
```bash
git clone https://github.com/Manashvi04/Student-Performance-Career-Analysis.git
cd Student-Performance-Career-Analysis
```

### 2. Establish Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Core Dependencies
Ensure you have `pip` updated, then install the necessary libraries:
```bash
pip install flask supabase python-dotenv pandas numpy scikit-learn joblib
```

### 4. Configure Environment Variables
Create a `.env` file in the absolute root directory of the project. You will need a provisioned project over at [Supabase](https://supabase.com/).
```env
# Essential Database Keys
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-public-anon-key
FLASK_SECRET_KEY=your-secure-flask-key

# Optional: Email Setup for Auto-Credentials Generation
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

### 5. Launch the Web Server
Launch the development environment:
```bash
python app.py
```
The application will default to running on `http://127.0.0.1:5000/`.

---

## 🔐 System Architecture Notes

* **Dummy vs. Standard ML Model:** Initializing the system without `model.joblib` triggers `ml_model.py` to compile an artificially standardized logic tree dataset ensuring out-of-the-box readiness.
* **Database Schema Requirements:** The backend expects standard implementations for `users`, `student_profiles`, and `subject_marks`. Use Supabase SQL editor to scaffold standard matching columns or view the Python queries across `app.py`.

---

## 🤝 Contribution Guidelines
This project heavily prioritizes Frontend Engineering rules outlined internally. Please avoid injecting generic component libraries (Bootstrap/Tailwind defaults) and respect the native `css/style.css` architecture. Maintain strict variable consistency across the project. 

*Designed and engineered originally for internal academic tracking.*
