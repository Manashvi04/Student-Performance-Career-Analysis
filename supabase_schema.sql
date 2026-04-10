-- INSTRUCTIONS: Open your Supabase project, go to the "SQL Editor" tab on the left, and paste this entire file to run it.

-- 1. Users Table (Handles login for students, faculty, and admins)
CREATE TABLE users (
    id TEXT PRIMARY KEY, -- e.g., 'STU001', 'FAC001'
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('student', 'faculty', 'admin')) NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Student Profiles Table (Stores academic mapping)
CREATE TABLE student_profiles (
    student_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    department TEXT NOT NULL,
    college TEXT,
    semester INTEGER DEFAULT 1,
    year INTEGER DEFAULT 1,
    cgpa NUMERIC(4,2) DEFAULT 0.0,
    co_curricular_score NUMERIC(4,2) DEFAULT 0.0,
    extra_curricular_score NUMERIC(4,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Subject Marks Table (For the faculty to upload subject-wise performance)
CREATE TABLE subject_marks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    student_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    subject_name TEXT NOT NULL,
    marks NUMERIC(5,2) NOT NULL,
    semester INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Activities Table (For students uploading their certificates)
CREATE TABLE activities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    student_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    activity_type TEXT CHECK(activity_type IN ('co_curricular', 'extra_curricular')) NOT NULL,
    description TEXT,
    proof_url TEXT, -- Path to the file in Supabase Storage
    points_awarded NUMERIC(4,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- INSERT MOCK ADMIN USER FOR TESTING
INSERT INTO users (id, password, role, name, email) 
VALUES ('admin123', 'admin', 'admin', 'System Administrator', 'admin@college.edu');

-- INSERT MOCK FACULTY USER FOR TESTING
INSERT INTO users (id, password, role, name, email) 
VALUES ('fac123', 'faculty', 'faculty', 'Prof. Smith', 'smith@college.edu');

-- INSERT MOCK STUDENT USER FOR TESTING
INSERT INTO users (id, password, role, name, email) 
VALUES ('stu123', 'student', 'student', 'John Doe', 'john@college.edu');

INSERT INTO student_profiles (student_id, department, college, semester, year, cgpa, co_curricular_score, extra_curricular_score)
VALUES ('stu123', 'Computer Science', 'Main Campus', 6, 3, 8.2, 7.5, 8.0);
