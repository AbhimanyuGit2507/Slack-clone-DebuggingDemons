import sqlite3

conn = sqlite3.connect(r'data\slack_rl.db')
cursor = conn.cursor()

# Check direct messages count
cursor.execute('SELECT COUNT(*) FROM direct_messages')
count = cursor.fetchone()[0]
print(f'✅ Direct messages count: {count}')

if count > 0:
    # Show first 5
    cursor.execute('SELECT id, sender_id, receiver_id, content FROM direct_messages LIMIT 5')
    print('\nFirst 5 DMs:')
    for row in cursor.fetchall():
        content_preview = row[3][:60] + '...' if len(row[3]) > 60 else row[3]
        print(f'  ID:{row[0]} From:User{row[1]} To:User{row[2]}')
        print(f'    "{content_preview}"')
else:
    print('❌ No direct messages found in database!')
    print('   The database needs to be reseeded.')

conn.close()
