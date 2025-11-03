# Quick Start Guide - Slack Clone

## 🚀 Getting Started in 3 Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/slack-rl-clone.git
cd slack-rl-clone
```

### Step 2: Start with Docker

```bash
docker-compose up --build
```

**Wait for the services to start** (this may take 2-3 minutes on first run)

You'll see:
```
slack-backend   | Starting Slack Clone Backend...
slack-backend   | Database initialized successfully!
slack-backend   | Starting Uvicorn server...
slack-backend   | INFO:     Application startup complete.
slack-frontend  | VITE ready in 1234 ms
slack-frontend  | ➜  Local:   http://localhost:5173/
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:5173**

You're ready to go! 🎉

---

## 📱 What You Can Do

### 1. Send Messages
- Click on **#general** channel in the sidebar
- Type a message in the input box at the bottom
- Press Enter or click Send

### 2. Create a Channel
- Click the **+** button next to "Channels" in sidebar
- Enter channel name (e.g., "team-updates")
- Add a description
- Click Create

### 3. Direct Message Someone
- Click **"Direct messages"** in left sidebar
- Click on a user (Alice, Bob, Charlie, Diana, or Eve)
- Start chatting!

### 4. Create a Canvas
- Go to any channel
- Click the **"Canvas"** tab (next to Messages)
- Click on the canvas and start typing
- Your content auto-saves every 2 seconds

### 5. Upload Files
- Click the **📎** (paperclip) icon in message composer
- Select a file
- Add an optional message
- Click Send

### 6. Star Important Items
- Hover over any channel or DM
- Click the **★** (star) icon
- Access starred items from the sidebar

### 7. Search and Browse
- Click **"Files"** in left navigation to see all shared files
- Click **"Activity"** to see recent mentions and updates
- Click **"People & user groups"** to browse team members

---

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal where docker-compose is running, then:

```bash
docker-compose down
```

To completely reset and remove all data:

```bash
docker-compose down -v
```

---

## 🔧 Troubleshooting

### Port Already in Use

If you see `port is already allocated`:

**Solution 1:** Stop other services using ports 8000 or 5173

**Solution 2:** Change ports in `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change 8000 to 8001
  frontend:
    ports:
      - "5174:5173"  # Change 5173 to 5174
```

### Docker Not Running

**Windows/Mac:** Start Docker Desktop

**Linux:**
```bash
sudo systemctl start docker
```

### Build Errors

Clear Docker cache and rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### Backend Not Starting

Check logs:
```bash
docker-compose logs backend
```

Restart just the backend:
```bash
docker-compose restart backend
```

---

## 📊 Sample Data

The application comes with pre-loaded data:

### Users (email / password - if auth was enabled)
- alice@example.com
- bob@example.com
- charlie@example.com  
- diana@example.com
- eve@example.com

### Channels
- **#general** - Main discussion (5 members, 10+ messages)
- **#random** - Off-topic chat (3 members, 5+ messages)
- **#development** - Technical discussions (4 members, 8+ messages)

### Direct Messages
- Multiple conversation threads between users
- Various message types and timestamps

### Files
- Sample documents and images
- Organized by channel

---

## 🔍 Exploring the API

Visit **http://localhost:8000/docs** for interactive API documentation

Try these endpoints:
- `GET /api/channels/` - List all channels
- `GET /api/users` - List all users
- `GET /api/messages/channel/1` - Get messages from #general
- `POST /api/messages/` - Send a new message

---

## 💡 Pro Tips

1. **Keyboard Shortcuts:**
   - `Ctrl+K` - Quick search (coming soon)
   - `@username` - Mention someone
   - `:emoji:` - Add emojis

2. **Rich Text Formatting:**
   - `**bold**` - Bold text
   - `*italic*` - Italic text
   - `` `code` `` - Inline code
   - `> quote` - Block quote

3. **Canvas Features:**
   - Auto-saves every 2 seconds
   - Click "+" to add new elements
   - Drag to reorder items
   - Multiple users can edit (in real implementation)

4. **File Management:**
   - Drag & drop files to upload
   - Star important files for quick access
   - Filter by file type in Files page

---

## 📖 Next Steps

1. Read the [README.md](README.md) for full feature list
2. Check [API.md](API.md) for API documentation
3. Review [SETUP.md](SETUP.md) for detailed setup options
4. Explore the codebase in `frontend/src/` and `backend/`

---

## 🤝 Need Help?

- Check the [SETUP.md](SETUP.md) troubleshooting section
- Review backend logs: `docker-compose logs backend`
- Review frontend logs: `docker-compose logs frontend`
- Open an issue on GitHub

---

**Enjoy exploring the Slack Clone! 🚀**
