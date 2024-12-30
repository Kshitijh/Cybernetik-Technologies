from flask import request, jsonify
import pyodbc

# Database connection setup
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER={KSHITIJ-PC};'
    'DATABASE={UAPR007};'
    'Trusted_Connection=yes;'
)

def create_row(data):
    conn = None
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Build the query dynamically
        query = """
            INSERT INTO UAPR007.dbo.Report 
            (Date_Time, Pallet_No, Total_Bag_Count, Total_time, Avg_Bag_time, Bag_Wait_time) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        # Execute the query with the provided data
        cursor.execute(query, data[0], data[1], data[2], data[3], data[4], data[5])  # Adjust this based on your column order
        conn.commit()
        
        return {"success": True}
    except pyodbc.Error as e:
        return {"success": False, "error": str(e)}
    finally:
        if conn:
            conn.close()



