from flask import request, jsonify
import pyodbc

# Database connection setup
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER={KSHITIJ-PC};'
    'DATABASE={UAPR007};'
    'Trusted_Connection=yes;'
)

def search_data(start_date, end_date):
    conn = None
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
     
        # Prepare the query to filter data by date range
        query = """
        SELECT * FROM UAPR007.dbo.Report
        WHERE Date_Time BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))

        # Fetch filtered rows
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        return columns, rows
    except pyodbc.Error as e:
        return str(e), [] # Return error message and an empty list in case of failure
    finally:
        if conn:
            conn.close()
