"""
View SQLite Database Contents - Pretty formatted output
"""
import sqlite3
import os
from tabulate import tabulate

db_path = os.path.join(os.path.dirname(__file__), 'data', 'slack_rl.db')

if not os.path.exists(db_path):
    print("❌ Database not found. Please run test_seed.py first or start the backend server.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("📊 SLACK DATABASE VIEWER")
print("="*80)

# Users
print("\n👥 USERS TABLE")
print("-"*80)
cursor.execute("""
    SELECT id, username, email, full_name, job_title, presence, status_text
    FROM users
    ORDER BY id
""")
users = cursor.fetchall()
print(tabulate(users, headers=['ID', 'Username', 'Email', 'Full Name', 'Job Title', 'Presence', 'Status'], tablefmt='grid'))
print(f"Total Users: {len(users)}")

# Channels
print("\n📺 CHANNELS TABLE")
print("-"*80)
cursor.execute("""
    SELECT c.id, c.name, c.section, 
           CASE WHEN c.is_private = 1 THEN '🔒 Private' ELSE '🌐 Public' END as privacy,
           COUNT(cm.user_id) as members,
           c.topic
    FROM channels c
    LEFT JOIN channel_members cm ON c.id = cm.channel_id
    GROUP BY c.id
    ORDER BY c.id
""")
channels = cursor.fetchall()
print(tabulate(channels, headers=['ID', 'Name', 'Section', 'Privacy', 'Members', 'Topic'], tablefmt='grid'))
print(f"Total Channels: {len(channels)}")

# User Groups
print("\n👨‍👩‍👧‍👦 USER GROUPS TABLE")
print("-"*80)
cursor.execute("""
    SELECT ug.id, ug.name, ug.handle, 
           COUNT(ugm.user_id) as members,
           ug.description
    FROM user_groups ug
    LEFT JOIN user_group_members ugm ON ug.id = ugm.group_id
    GROUP BY ug.id
    ORDER BY ug.id
""")
groups = cursor.fetchall()
print(tabulate(groups, headers=['ID', 'Name', 'Handle', 'Members', 'Description'], tablefmt='grid'))
print(f"Total User Groups: {len(groups)}")

# Messages
print("\n💬 RECENT MESSAGES")
print("-"*80)
cursor.execute("""
    SELECT m.id, u.full_name as user, c.name as channel, 
           substr(m.content, 1, 50) as content_preview
    FROM messages m
    JOIN users u ON m.user_id = u.id
    JOIN channels c ON m.channel_id = c.id
    ORDER BY m.timestamp DESC
    LIMIT 10
""")
messages = cursor.fetchall()
print(tabulate(messages, headers=['ID', 'User', 'Channel', 'Content Preview'], tablefmt='grid'))
cursor.execute("SELECT COUNT(*) FROM messages")
total_messages = cursor.fetchone()[0]
print(f"Total Messages: {total_messages}")

# Channel Members Detail
print("\n👥 CHANNEL MEMBERSHIP SUMMARY")
print("-"*80)
cursor.execute("""
    SELECT c.name as channel, 
           GROUP_CONCAT(u.full_name, ', ') as members
    FROM channels c
    JOIN channel_members cm ON c.id = cm.channel_id
    JOIN users u ON cm.user_id = u.id
    GROUP BY c.id
    ORDER BY c.name
""")
memberships = cursor.fetchall()
for channel, members in memberships:
    print(f"\n#{channel}:")
    member_list = members.split(', ')
    for i, member in enumerate(member_list, 1):
        print(f"  {i}. {member}")

# User Group Members Detail
print("\n\n👨‍👩‍👧‍👦 USER GROUP MEMBERSHIP DETAIL")
print("-"*80)
cursor.execute("""
    SELECT ug.handle as group_handle,
           GROUP_CONCAT(u.full_name, ', ') as members
    FROM user_groups ug
    JOIN user_group_members ugm ON ug.id = ugm.group_id
    JOIN users u ON ugm.user_id = u.id
    GROUP BY ug.id
    ORDER BY ug.name
""")
group_memberships = cursor.fetchall()
for group, members in group_memberships:
    print(f"\n{group}:")
    member_list = members.split(', ')
    for i, member in enumerate(member_list, 1):
        print(f"  {i}. {member}")

print("\n" + "="*80)
print("✅ Database view complete!")
print("="*80)

conn.close()
