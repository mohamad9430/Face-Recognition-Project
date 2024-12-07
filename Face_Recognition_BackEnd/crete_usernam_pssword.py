import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/data', methods=['POST'])
def process_image():
    data = request.form
    user_name = data['text5']
    password = data['text6']
    sign_up(user_name, password)
    print(f"Received image path in Python: {user_name}")
    print(password)
    return "Test Succeeded"

def sign_up(user_name, password):
    with sqlite3.connect(r"C:\Users\admin\Desktop\t.db") as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user_name, password))


if __name__ == '__main__':
    app.run(debug=True, port=6000)
