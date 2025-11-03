"""
Database migration script to add formatted_content support for rich text editing
Run this script to add the formatted_content column to messages and direct_messages tables
"""

import sqlite3
import os

def migrate_database():
    # Path to database - check both possible locations
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'slack_rl.db')
    
    if not os.path.exists(db_path):
        # Try alternative path
        db_path = os.path.join(os.path.dirname(__file__), 'slack_clone.db')
        
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("Skipping migration - database will be created with new schema")
        return
    
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if formatted_content already exists in messages table
        cursor.execute("PRAGMA table_info(messages)")
        messages_columns = [col[1] for col in cursor.fetchall()]
        
        if 'formatted_content' not in messages_columns:
            print("Adding formatted_content column to messages table...")
            cursor.execute("""
                ALTER TABLE messages 
                ADD COLUMN formatted_content TEXT
            """)
            print("✓ Added formatted_content to messages table")
        else:
            print("✓ formatted_content already exists in messages table")
        
        # Check if formatted_content already exists in direct_messages table
        cursor.execute("PRAGMA table_info(direct_messages)")
        dm_columns = [col[1] for col in cursor.fetchall()]
        
        if 'formatted_content' not in dm_columns:
            print("Adding formatted_content column to direct_messages table...")
            cursor.execute("""
                ALTER TABLE direct_messages 
                ADD COLUMN formatted_content TEXT
            """)
            print("✓ Added formatted_content to direct_messages table")
        else:
            print("✓ formatted_content already exists in direct_messages table")
        
        # Backfill existing messages with plain text as formatted content
        print("\nBackfilling existing messages...")
        cursor.execute("""
            UPDATE messages 
            SET formatted_content = content 
            WHERE formatted_content IS NULL
        """)
        messages_updated = cursor.rowcount
        print(f"✓ Updated {messages_updated} messages")
        
        cursor.execute("""
            UPDATE direct_messages 
            SET formatted_content = content 
            WHERE formatted_content IS NULL
        """)
        dms_updated = cursor.rowcount
        print(f"✓ Updated {dms_updated} direct messages")
        
        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
