"""Migration script to add is_system_message column to messages table"""
from sqlalchemy import text
from backend.database import engine

def add_system_message_column():
    with engine.connect() as conn:
        try:
            # Check if column exists (SQLite)
            result = conn.execute(text("PRAGMA table_info(messages)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'is_system_message' not in columns:
                # Add the column if it doesn't exist
                conn.execute(text("""
                    ALTER TABLE messages 
                    ADD COLUMN is_system_message BOOLEAN DEFAULT 0
                """))
                conn.commit()
                print("✅ Successfully added is_system_message column to messages table")
            else:
                print("ℹ️ Column is_system_message already exists in messages table")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_system_message_column()
