import pyodbc
# Database connection setup
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER={KSHITIJ-PC};'
    'DATABASE={UAPR007};'
    'Trusted_Connection=yes;'
)

def edit_row(Date_Time, data):
    conn = None
    try:
        # Ensure data is in the correct format
        # Convert values to the correct types if necessary, with validation
        try:    
            pallet_no = int(data[1])
            total_bag_count = float(data[2])
            total_time = str(data[3])  
            avg_bag_time = str(data[4])  
            bag_wait_time = str(data[5])
        except ValueError as e:
            return {"success": False, "error": f"Data conversion error: {e}"}

        # Log the converted data (for debugging)
        print(f"Data to be updated: Pallet_No={pallet_no}, Total_Bag_Count={total_bag_count}, "
              f"Total_time={total_time}, Avg_Bag_time={avg_bag_time}, Bag_Wait_time={bag_wait_time}")

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """
        UPDATE UAPR007.dbo.Report
        SET Pallet_No = ?, Total_Bag_Count = ?, Total_time = ?, Avg_Bag_time = ?, Bag_Wait_time = ?
        WHERE Date_Time = ?
        """
        
        # Execute the query with validated data
        cursor.execute(query, (pallet_no, total_bag_count, total_time, avg_bag_time, bag_wait_time, Date_Time))
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            return {"success": False, "error": "No matching row found to update."}

        return {"success": True}

    except pyodbc.Error as e:
        return {"success": False, "error": str(e)}

    finally:
        if conn:
            conn.close()
