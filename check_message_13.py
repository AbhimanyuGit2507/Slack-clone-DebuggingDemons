import sqlite3

def check_message_exists(db_path, message_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM messages WHERE id = ?;"
        cursor.execute(query, (message_id,))
        result = cursor.fetchone()

        if result:
            print(f"Message with ID {message_id} exists: {result}")
        else:
            print(f"Message with ID {message_id} does not exist.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = "data/slack_rl.db"
    message_id = 13  # Replace with the ID you want to check
    check_message_exists(db_path, message_id)