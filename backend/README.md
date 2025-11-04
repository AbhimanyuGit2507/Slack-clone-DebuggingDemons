# Slack Clone Backend API

A comprehensive FastAPI backend for a Slack-like messaging application with SQLite database.

## Features

- 🔐 **Authentication System** - Session-based authentication with cookies
- 💬 **Channel Messaging** - Public and private channels with threaded conversations
- 📧 **Direct Messages** - 1-on-1 messaging between users
- 👥 **User Management** - User profiles, contacts, and directory
- 🧵 **Threaded Replies** - Reply to messages in threads
- 😀 **Message Reactions** - React to messages with emojis
- 🔒 **Authorization** - Role-based access control for channels and messages

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL ORM for database operations
- **SQLite** - Lightweight local database
- **Pydantic** - Data validation using Python type annotations
- **Passlib** - Secure password hashing with bcrypt
- **Python-dotenv** - Environment variable management

## Project Structure

```
backend/
├── config.py           # Configuration and environment settings
├── database.py         # Database connection and session management
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic schemas for request/response
├── middleware.py      # Session authentication middleware
├── main.py           # FastAPI application entry point
└── routes/
    ├── auth.py            # Authentication endpoints
    ├── users.py           # User management endpoints
    ├── channels.py        # Channel management endpoints
    ├── messages.py        # Message, thread, and reaction endpoints
    └── direct_messages.py # Direct message endpoints
```

## Database Models

### User
- `id`, `username`, `email`, `password_hash`
- `profile_picture`, `status`, `created_at`, `updated_at`
- Relationships: channels, contacts

### Channel
- `id`, `name`, `description`, `is_private`
- `created_by`, `created_at`
- Relationships: members, messages, creator

### Message
- `id`, `channel_id`, `user_id`, `content`, `timestamp`
- Relationships: channel, user, threads, reactions

### DirectMessage
- `id`, `sender_id`, `receiver_id`, `content`
- `timestamp`, `is_read`
- Relationships: sender, receiver

### Thread
- `id`, `parent_message_id`, `user_id`, `content`, `timestamp`
- Relationships: parent_message, user

### Reaction
- `id`, `message_id`, `user_id`, `emoji`, `timestamp`
- Relationships: message, user

### Session
- `id`, `session_id`, `user_id`, `created_at`, `expires_at`
- Relationships: user

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
DEBUG=False
DATABASE_URL=sqlite:///./data/slack_rl.db
SECRET_KEY=your-secret-key-change-this-in-production
SESSION_EXPIRY_HOURS=24
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8000
```

### 3. Run the Server

```bash
# From the project root directory
uvicorn backend.main:app --reload --port 8000

# Or using the batch file (Windows)
start-backend.bat
```

The API will be available at: `http://localhost:8000`

### 4. API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication (`/api/auth`)

- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user
- `GET /api/auth/check` - Check authentication status

### Users (`/api/users`)

- `GET /api/users` - List all users (with search and filters)
- `GET /api/users/{user_id}` - Get user profile
- `GET /api/users/me/profile` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/directory` - Get user directory
- `POST /api/users/contacts` - Add contact
- `GET /api/users/contacts` - Get contacts list
- `DELETE /api/users/contacts/{contact_id}` - Remove contact

### Channels (`/api/channels`)

- `POST /api/channels` - Create a channel
- `GET /api/channels` - List channels
- `GET /api/channels/my-channels` - Get user's channels
- `GET /api/channels/{channel_id}` - Get channel details
- `PUT /api/channels/{channel_id}` - Update channel
- `DELETE /api/channels/{channel_id}` - Delete channel
- `POST /api/channels/{channel_id}/join` - Join channel
- `POST /api/channels/{channel_id}/leave` - Leave channel
- `POST /api/channels/{channel_id}/invite/{user_id}` - Invite user

### Messages (`/api/messages`)

- `POST /api/messages` - Send message
- `GET /api/messages/channel/{channel_id}` - Get channel messages
- `PUT /api/messages/{message_id}` - Update message
- `DELETE /api/messages/{message_id}` - Delete message

#### Threads
- `POST /api/messages/{message_id}/threads` - Create thread reply
- `GET /api/messages/{message_id}/threads` - Get message threads
- `PUT /api/messages/threads/{thread_id}` - Update thread
- `DELETE /api/messages/threads/{thread_id}` - Delete thread

#### Reactions
- `POST /api/messages/{message_id}/reactions` - Add reaction
- `GET /api/messages/{message_id}/reactions` - Get reactions
- `DELETE /api/messages/reactions/{reaction_id}` - Remove reaction

### Direct Messages (`/api/direct-messages`)

- `POST /api/direct-messages` - Send direct message
- `GET /api/direct-messages/conversation/{user_id}` - Get conversation
- `GET /api/direct-messages/conversations` - Get all conversations
- `PUT /api/direct-messages/{message_id}` - Update direct message
- `DELETE /api/direct-messages/{message_id}` - Delete direct message
- `PATCH /api/direct-messages/{message_id}/read` - Mark as read

## Authentication Flow

1. **Signup**: User registers with username, email, and password
2. **Login**: User logs in, receives session cookie
3. **Protected Routes**: Session cookie is validated on each request
4. **Logout**: Session is deleted from database and cookie is cleared

### Session Cookie Details

- Cookie name: `session_id` (configurable)
- HttpOnly: Yes (prevents XSS attacks)
- SameSite: Lax
- Expiry: 24 hours (configurable)

## Security Features

- 🔒 Password hashing with bcrypt
- 🍪 HttpOnly cookies for session management
- 🔐 Session expiration and validation
- 🛡️ Authorization checks for all protected routes
- 🚫 CORS configuration for frontend access

## Database Initialization

The database is automatically initialized on startup:
- Creates all tables if they don't exist
- Seeds initial data from `data/seed.json` if database is empty
- Located at `data/slack_rl.db`

## Error Handling

All endpoints include proper error handling:
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Development

### Running in Development Mode

```bash
uvicorn backend.main:app --reload --port 8000
```

### Testing with curl

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  -c cookies.txt

# Get current user (with session cookie)
curl http://localhost:8000/api/auth/me -b cookies.txt
```

## Notes

- This backend is designed to work independently of the frontend
- All routes use `/api/` prefix for clear API organization
- Session-based authentication is used (no JWT tokens)
- Database migrations are automatic via SQLAlchemy
- Backward compatibility maintained for existing seed data

## Future Enhancements

- WebSocket support for real-time messaging
- File upload for attachments
- Email notifications
- Advanced search functionality
- Message editing history
- Typing indicators
- Read receipts
- User presence updates

## License

MIT License
