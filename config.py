import pyodbc

SERVER = "PRINCEE"
DATABASE = "student_performance_system"

CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(CONNECTION_STRING)