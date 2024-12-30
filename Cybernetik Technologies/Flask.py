from flask import Flask, request, render_template, jsonify
import pyodbc
from urllib.parse import unquote
from Delete import delete_row  
from Search import search_data
from Create import create_row
# from Edit import edit_row

app = Flask(__name__)

# Database connection setup
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER={KSHITIJ-PC};'
    'DATABASE={UAPR007};'
    'Trusted_Connection=yes;'
)

#To fetch data from the database 
@app.route('/data', methods=['GET'])
def get_data():
    conn = None
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Fetch all data
        query = "SELECT * FROM UAPR007.dbo.Report"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        # Add serial numbers dynamically
        rows_with_serial = [(index + 1, *row) for index, row in enumerate(rows)]

        return render_template("table.html", columns=columns, rows=rows_with_serial)
    except pyodbc.Error as e:
        return f"<h1>Error: {str(e)}</h1>", 500
    finally:
        if conn:
            conn.close()

#To search and sort data from the database
@app.route('/search', methods=['GET'])
def search():
    # Get date range from the request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Call search_data function from Search.py
    columns, rows = search_data(start_date, end_date)

    if isinstance(columns, str):  # Handle error returned by search_data
        return f"<h1>Error: {columns}</h1>", 500
    if not rows:  # No rows found
        return "<h1>No data found for the given date range</h1>", 404
    
    # Add serial numbers dynamically
    rows_with_serial = [(index + 1, *row) for index, row in enumerate(rows)]
    return render_template("table.html", columns=columns, rows=rows_with_serial)

#To create new rows in the database
@app.route('/create', methods=['POST'])
def create_row_route():
    data = request.json.get("data")  # Get row data from the POST request
    result = create_row(data)

    if result["success"]:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": result["error"]}), 500

# To delete a row from the database
@app.route('/delete/<unique_identifier>', methods=['DELETE'])
def delete_route(unique_identifier):
    unique_identifier = unquote(unique_identifier)  # Decode the URL-encoded identifier
    result = delete_row(unique_identifier)

    if result["success"]:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": result["error"]}), 500
    

'''
# To edit a row in the database
@app.route('/edit/<unique_identifier>', methods=['POST'])
def edit_route(unique_identifier):
    # Extract data from the POST request
    data = request.json.get("data")
    
    if not data or len(data) != 5:
        return jsonify({"success": False, "error": "Incorrect number of values in the data."}), 400

    # Call the edit_row function to update the row in the database
    result = edit_row(unique_identifier, data)

    if result["success"]:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": result["error"]}), 500
'''

#To reset the table to show all rows from the database
@app.route('/reset', methods=['GET'])
def reset_table():
    # Resets the data table to show all rows from the database.
    conn = None
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Fetch all data
        query = "SELECT * FROM UAPR007.dbo.Report"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        # Add serial numbers dynamically
        rows_with_serial = [(index + 1, *row) for index, row in enumerate(rows)]

        return render_template("table.html", columns=columns, rows=rows_with_serial)
    except pyodbc.Error as e:
        return f"<h1>Error: {str(e)}</h1>", 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)