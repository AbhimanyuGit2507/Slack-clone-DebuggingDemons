# 📊 How to View Your SQLite Database

## Method 1: SQLite Viewer Extension (Already Installed! ✅)

1. **Locate** `slack.db` file in VS Code Explorer
2. **Right-click** on `slack.db`
3. Select **"Open with SQLite Viewer"**
4. Browse tables visually with a beautiful interface!

## Method 2: SQLite Extension (Already Installed! ✅)

1. Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
2. Type: **"SQLite: Open Database"**
3. Select `slack.db`
4. Click on "SQLite Explorer" in the sidebar
5. Expand tables and run queries!

## Method 3: Python Script to Display Data

Run this command:
```bash
python view_database.py
```

## Method 4: VS Code Built-in SQLite Browser

1. In Explorer, click on `slack.db` file
2. VS Code will automatically open it with SQLite Viewer

## 📋 Sample Queries

Once you open SQLite Explorer, try these queries:

### View all users:
```sql
SELECT id, username, email, full_name, job_title, presence, status 
FROM users;
```

### View all channels with member count:
```sql
SELECT c.id, c.name, c.section, c.is_private, COUNT(cm.user_id) as member_count
FROM channels c
LEFT JOIN channel_members cm ON c.id = cm.channel_id
GROUP BY c.id;
```

### View user groups with members:
```sql
SELECT ug.name, ug.handle, COUNT(ugm.user_id) as member_count
FROM user_groups ug
LEFT JOIN user_group_members ugm ON ug.id = ugm.group_id
GROUP BY ug.id;
```

### View messages with user info:
```sql
SELECT m.id, u.full_name, c.name as channel, m.content, m.timestamp
FROM messages m
JOIN users u ON m.user_id = u.id
JOIN channels c ON m.channel_id = c.id
ORDER BY m.timestamp DESC;
```

## 🔍 Explore Your Data

After seeding, you should see:
- ✅ 15 users in `users` table
- ✅ 10 channels in `channels` table
- ✅ 8 user groups in `user_groups` table
- ✅ 10 messages in `messages` table
- ✅ Relationships in `channel_members` and `user_group_members` tables
