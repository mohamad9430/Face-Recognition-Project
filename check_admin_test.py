import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def check_admin_user_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM admin_users WHERE is_admin = 1")
    count = cursor.fetchone()[0]
    return count > 0


@app.route('/test', methods=['GET', 'POST'])
def test():
    data = request.json
    image_name2 = data.get('text3')
    image_name = data.get('text4')
    print(image_name2)
    print(image_name)
    return "test"


@app.route('/data', methods=['GET', 'POST'])
def main():


    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t.db")
    cursor = conn.cursor()

    if check_admin_user_exists(cursor):
        return "There is at least one admin user."
    else:
        print("There are no admin users.")
    conn.close()




if __name__ == '__main__':
    app.run(debug=True, port=6300)