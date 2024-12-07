import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def check_admin_user_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    count = cursor.fetchone()[0]
    return count > 0


@app.route('/test', methods=['POST'])
def test():
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t3.db")
    cursor = conn.cursor()

    data = request.json
    ad_user_name = data.get('text5')
    password2 = data.get('text6')
    print(ad_user_name)
    print(password2)

    admin_username = ad_user_name
    password = password2
    is_admin = False
    upload = data.get('text3')
    detection = data.get('text4')
    print(upload)
    print(detection)

    cursor.execute('''INSERT INTO users (admin_username, password, is_admin, upload, detection)
                          VALUES (?, ?,  ?, ?, ?)''', (admin_username, password, is_admin, upload, detection))

    print("Admin user inserted successfully.")

    conn.commit()
    conn.close()

    return "Admin user inserted successfully."


if __name__ == '__main__':
    app.run(debug=True, port=6300)
