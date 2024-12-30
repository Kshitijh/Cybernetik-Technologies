import pyodbc

# Database connection setup
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER={KSHITIJ-PC};'
    'DATABASE={UAPR007};'
    'Trusted_Connection=yes;'
)

def delete_row(Date_Time):
    """
    Deletes a row from the database based on the Date_Time column.

    Args:
        Date_Time (str): The value of the Date_Time column for the row to delete.

    Returns:
        dict: A dictionary with a success key indicating the operation status and an error key if applicable.
    """
    conn = None
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Delete query based on the Date_Time column
        query = """
        DELETE FROM UAPR007.dbo.Report
        WHERE Date_Time = ?
        """
        cursor.execute(query, (Date_Time,))
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            return {"success": False, "error": "No matching row found to delete."}

        return {"success": True}

    except pyodbc.Error as e:
        return {"success": False, "error": str(e)}

    finally:
        if conn:
            conn.close()
