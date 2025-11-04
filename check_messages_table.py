import sqlite3

def check_messages_table(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM messages;"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print("Messages table contains the following data:")
            for row in results:
                print(row)
        else:
            print("Messages table is empty.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = "data/slack_rl.db"
    check_messages_table(db_path)