CREATE DATABASE student_performance_system;

USE student_performance_system;

CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    id VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(20)
);

INSERT INTO users (id, email, password, role)
VALUES 
('Admin', 'admin@charusat.ac.in', 'admin@1234', 'admin'),
('Dr patel', 'patel.it@charusat.edu.in', 'patel@1234', 'faculty'),
('24DIT006', '24dit006@charusat.edu.in', 'princee@1234', 'student');
