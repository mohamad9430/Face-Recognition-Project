import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

global_username_input = None

def authenticate_user(username, password):
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data:
        if password == user_data[2]:
            print("Authentication successful!")
            return "Authentication successful"
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")

    conn.close()
    return False


@app.route('/login', methods=['POST'])
def login():
    global global_username_input
    data = request.json
    username = data.get('text3')
    password = data.get('text4')
    if authenticate_user(username, password):
        global_username_input = username
        print("Stored username:", global_username_input)
        return "Authentication successful"
    else:
        return "Authentication failed"


if __name__ == '__main__':
    app.run(debug=True, port=6800)
