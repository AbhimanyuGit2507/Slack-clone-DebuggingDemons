import sqlite3

def check_table_exists(db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()

        if result:
            print(f"Table '{table_name}' exists.")
        else:
            print(f"Table '{table_name}' does not exist.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = "data/slack_rl.db"
    table_name = "reactions"  # Replace with the table name you want to check
    check_table_exists(db_path, table_name)