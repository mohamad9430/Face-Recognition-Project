import sqlite3

def insert_admin_user(cursor):
    # Get user input for each column
    admin_username = input("Enter admin username: ")
    password = input("Enter password: ")
    is_admin_input = input("Is the user an admin? (True/False): ").lower()
    is_admin = is_admin_input == 'true'

    # Insert values into the table
    cursor.execute('''INSERT INTO admin_users (admin_username, password, is_admin) 
                      VALUES (?, ?, ?)''', (admin_username, password, is_admin))

    print("Admin user inserted successfully.")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(r"C:\Users\admin\Desktop\t.db")
    cursor = conn.cursor()

    # Insert values into the table
    insert_admin_user(cursor)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
