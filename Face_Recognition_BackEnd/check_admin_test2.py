import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def check_admin_user_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM users3 WHERE is_admin = 1")
    count = cursor.fetchone()[0]
    return count > 0


@app.route('/test', methods=['POST'])
def check_admin():
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    data = request.json
    ad_user_name = data.get('text3')
    password2 = data.get('text4')
    print(ad_user_name)
    print(password2)

    admin_username = ad_user_name
    password = password2
    is_admin_input = "true"
    is_admin = is_admin_input == 'true'
    upload = True
    detection = True

    cursor.execute('''INSERT INTO users3 (username, password, is_admin, upload, detection)
                          VALUES (?, ?, ?, ?, ?)''', (admin_username, password, is_admin, upload, detection))

    print("Admin user inserted successfully.")

    conn.commit()
    conn.close()

    return "Admin user inserted successfully."


@app.route('/data', methods=['GET'])
def check_admin():
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    if check_admin_user_exists(cursor):
        conn.close()
        return "There is at least one admin user."
    else:
        conn.close()
        return "There are no admin users."


if __name__ == '__main__':
    app.run(debug=True, port=6300)
