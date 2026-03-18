CREATE DATABASE student_performance_system;

USE student_performance_system;

CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    id VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(20)
);
/*academic year */
CREATE TABLE academic_years (
    year_id INT IDENTITY(1,1) PRIMARY KEY,
    year VARCHAR(10)
);
/* */

DECLARE @year INT = 1990

WHILE @year <= 2500
BEGIN
    INSERT INTO academic_years (year)
    VALUES (CAST(@year AS VARCHAR(10)))

    SET @year = @year + 1
END

/* */

SELECT * FROM academic_years
/* */


CREATE TABLE departments (
    dept_id INT IDENTITY(1,1) PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    dept_id INT,
    year_id INT,
    program VARCHAR(50),
    admission_date DATE,

    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (year_id) REFERENCES academic_years(year_id)
);

SELECT TOP (1000) *
FROM [student_performance_system].[dbo].[academic_years]

INSERT INTO users (id, email, password, role)
VALUES 
('Admin', 'admin@charusat.ac.in', 'admin@1234', 'admin'),
('Dr patel', 'patel.it@charusat.edu.in', 'patel@1234', 'faculty'),
('24DIT006', '24dit006@charusat.edu.in', 'princee@1234', 'student');
