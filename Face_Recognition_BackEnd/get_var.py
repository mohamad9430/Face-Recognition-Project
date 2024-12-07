from flask import Flask
import sqlite3

app = Flask(__name__)

employee_id = "ahmad"


@app.route('/test', methods=['GET'])
def get_boolean_value2():
    # employee_id = "ahmad"
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT upload FROM users WHERE admin_username = ?", (employee_id,))
    row = cursor.fetchone()

    if row:
        boolean_value = bool(row[0])

        cursor.close()
        conn.close()

        print(str(boolean_value))
        return str(boolean_value)
    else:
        cursor.close()
        conn.close()

        return 'Employee not found', 404


@app.route('/testt', methods=['GET'])
def get_boolean_value():
    # employee_id = "ahmad"
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT detection FROM users WHERE admin_username = ?", (employee_id,))
    row = cursor.fetchone()

    if row:
        boolean_value = bool(row[0])

        cursor.close()
        conn.close()

        print(str(boolean_value))
        return str(boolean_value)
    else:
        cursor.close()
        conn.close()

        return 'Employee not found', 404


if __name__ == '__main__':
    app.run(debug=True)
