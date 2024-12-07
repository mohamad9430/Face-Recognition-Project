import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    data = request.json
    upload = data.get('text3')

    detection = data.get('text4')

    user_name = data.get('text5')

    password2 = data.get('text6')

    admin_username = user_name

    password = password2

    is_admin_input = "false"

    is_admin = is_admin_input == 'true'

    cursor.execute('''INSERT INTO users3 (username, password, is_admin, upload, detection)
                              VALUES (?, ?, ?, ?, ?)''', (admin_username, password, is_admin, upload, detection))

    print("User inserted successfully.")

    conn.commit()
    conn.close()

    print(user_name)
    print(password2)
    print(upload)
    print(detection)
    return "User inserted successfully."

if __name__ == '__main__':
    app.run(debug=True, port=6300)