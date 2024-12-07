import sqlite3


def check_admin_user_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM admin_users WHERE is_admin = 1")
    count = cursor.fetchone()[0]
    return count > 0


def main():
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t.db")
    cursor = conn.cursor()

    if check_admin_user_exists(cursor):
        print("There is at least one admin user.")
    else:
        print("There are no admin users.")
    conn.close()


if __name__ == "__main__":
    main()
