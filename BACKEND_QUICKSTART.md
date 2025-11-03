# Backend Quick Start Guide

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your preferred settings
# For development, the defaults are fine
```

### 3. Start the Backend Server
```bash
# From the project root directory
uvicorn backend.main:app --reload --port 8000

# The server will be available at http://localhost:8000
```

## Testing the API

### Option 1: Use the Interactive Docs
Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: Use curl Commands

#### 1. Create a User Account
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
  }' \
  -c cookies.txt -v
```

#### 2. Login (if you already have an account)
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }' \
  -c cookies.txt -v
```

#### 3. Get Current User Info
```bash
curl http://localhost:8000/api/auth/me -b cookies.txt
```

#### 4. Create a Channel
```bash
curl -X POST http://localhost:8000/api/channels \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "general",
    "description": "General discussion channel",
    "is_private": false
  }'
```

#### 5. List Channels
```bash
curl http://localhost:8000/api/channels -b cookies.txt
```

#### 6. Send a Message to a Channel
```bash
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "channel_id": 1,
    "user_id": 1,
    "content": "Hello, everyone!"
  }'
```

#### 7. Get Messages from a Channel
```bash
curl http://localhost:8000/api/messages/channel/1 -b cookies.txt
```

#### 8. Send a Direct Message
```bash
curl -X POST http://localhost:8000/api/direct-messages \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "receiver_id": 2,
    "content": "Hey, how are you?"
  }'
```

#### 9. Get Conversation with a User
```bash
curl http://localhost:8000/api/direct-messages/conversation/2 -b cookies.txt
```

#### 10. List All Users
```bash
curl http://localhost:8000/api/users -b cookies.txt
```

#### 11. Search Users
```bash
curl "http://localhost:8000/api/users?search=john" -b cookies.txt
```

#### 12. Add a Reaction to a Message
```bash
curl -X POST http://localhost:8000/api/messages/1/reactions \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message_id": 1,
    "emoji": "👍"
  }'
```

#### 13. Create a Thread Reply
```bash
curl -X POST http://localhost:8000/api/messages/1/threads \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "parent_message_id": 1,
    "content": "Great point!"
  }'
```

#### 14. Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout -b cookies.txt -c cookies.txt
```

## Common Issues

### Issue: "Not authenticated" error
**Solution**: Make sure you're using the `-b cookies.txt` flag to send the session cookie with your requests.

### Issue: "Module not found" error
**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete the database file and restart the server to recreate it:
```bash
rm data/slack_rl.db
uvicorn backend.main:app --reload --port 8000
```

### Issue: Port 8000 already in use
**Solution**: Use a different port:
```bash
uvicorn backend.main:app --reload --port 8001
```

## API Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Auth      │  │   Users      │  │  Channels    │     │
│  │   Routes     │  │   Routes     │  │   Routes     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │   Messages   │  │    Direct    │                        │
│  │   Routes     │  │   Messages   │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│              Session Authentication Middleware               │
├─────────────────────────────────────────────────────────────┤
│                    SQLAlchemy ORM Layer                      │
├─────────────────────────────────────────────────────────────┤
│                    SQLite Database                           │
│    (Users, Channels, Messages, DMs, Threads, Reactions)    │
└─────────────────────────────────────────────────────────────┘
```

## Key Features Implemented

✅ User authentication with session cookies  
✅ Password hashing with bcrypt  
✅ Public and private channels  
✅ Channel membership management  
✅ Direct messaging between users  
✅ Threaded replies to messages  
✅ Message reactions (emojis)  
✅ User profile management  
✅ Contact list management  
✅ User directory with search  
✅ Comprehensive error handling  
✅ Automatic database initialization  
✅ CORS support for frontend  

## Next Steps

1. Test all endpoints using the Swagger UI at http://localhost:8000/docs
2. Create multiple user accounts to test messaging
3. Create channels and test public/private access
4. Test direct messaging between users
5. Try adding reactions and thread replies
6. Explore the user directory and contact features

## Support

For detailed API documentation, visit:
- http://localhost:8000/docs (Interactive Swagger UI)
- http://localhost:8000/redoc (ReDoc documentation)

For backend architecture and implementation details, see `backend/README.md`
