import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

global_username_input = None


def authenticate_user(username, password):
    conn = sqlite3.connect("C:\\Users\\admin\\Desktop\\t3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users3 WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data:
        if password == user_data[2]:
            print("Authentication successful!")
            conn.close()
            return "Authentication successful"
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")

    conn.close()
    return "Authentication failed"


@app.route('/login', methods=['POST'])
def login():
    global global_username_input
    data = request.json
    username = data.get('text3')
    password = data.get('text4')
    if authenticate_user(username, password) == "Authentication successful":
        global_username_input = username
        print("Stored username:", global_username_input)
        return "Authentication successful"
    else:
        return "Authentication failed"


@app.route('/test', methods=['GET', 'POST'])
def get_boolean_values():
    global global_username_input
    print("Stored username:2", global_username_input)
    if global_username_input:
        conn = sqlite3.connect("C:\\Users\\admin\\Desktop\\t3.db")
        cursor = conn.cursor()

        cursor.execute("SELECT upload, detection FROM users3 WHERE username = ?", (global_username_input,))
        row = cursor.fetchone()

        if row:
            upload_value = bool(row[0])
            detection_value = bool(row[1])
            is_admin = bool(row[1])
            cursor.close()
            conn.close()
            print("Upload Value:", upload_value)
            print("Detection Value:", detection_value)
            print("IsAdmin Value:", is_admin)
            return jsonify({'upload': upload_value, 'detection': detection_value, 'is_admin': is_admin})
        else:
            cursor.close()
            conn.close()
            return 'Boolean values not found', 404
    else:
        return 'User not logged in', 401

if __name__ == '__main__':
    app.run(debug=True, port=6800)
