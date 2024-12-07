import sqlite3

def get_boolean_value(employee_id):
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t.db")
    cursor = conn.cursor()

    # Execute a query to retrieve the boolean value for the specified employee ID
    cursor.execute("SELECT is_hr FROM employees WHERE employee_id = ?", (employee_id,))
    row = cursor.fetchone()

    # Check if a row was found
    if row:
        # Convert the retrieved value to a boolean value
        boolean_value = bool(row[0])

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the boolean value
        return boolean_value
    else:
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return None if the employee ID was not found
        return None

if __name__ == '__main__':
    employee_id = 1  # Specify the employee ID here
    boolean_value = get_boolean_value(employee_id)
    if boolean_value is not None:
        print(f"The boolean value for employee {employee_id} is: {boolean_value}")
    else:
        print(f"Employee with ID {employee_id} not found.")
