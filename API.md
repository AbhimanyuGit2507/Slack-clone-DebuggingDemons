# API Documentation - Slack Clone

Complete API reference for the Slack Clone backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently disabled for demo purposes. All endpoints are accessible without authentication.

For production, endpoints would require JWT token in header:
```
Authorization: Bearer <token>
```

---

## Users API

### Get All Users
```http
GET /api/users
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "full_name": "Alice Johnson",
    "profile_pic": "https://example.com/pic.jpg",
    "is_online": true,
    "status": "Active",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get User by ID
```http
GET /api/users/{user_id}
```

### Update User Profile
```http
PUT /api/users/{user_id}
```

**Request Body:**
```json
{
  "full_name": "Alice Johnson",
  "profile_pic": "https://example.com/new-pic.jpg",
  "status": "Away"
}
```

---

## Channels API

### List All Channels
```http
GET /api/channels/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "general",
    "description": "General discussion",
    "is_private": false,
    "created_at": "2024-01-01T00:00:00",
    "member_count": 5
  }
]
```

### Create Channel
```http
POST /api/channels/
```

**Request Body:**
```json
{
  "name": "new-channel",
  "description": "Channel description",
  "is_private": false
}
```

### Get Channel by Name
```http
GET /api/channels/{channel_name}
```

### Update Channel
```http
PUT /api/channels/{channel_id}
```

**Request Body:**
```json
{
  "name": "updated-name",
  "description": "Updated description",
  "is_private": true
}
```

### Delete Channel
```http
DELETE /api/channels/{channel_id}
```

### Join Channel
```http
POST /api/channels/{channel_id}/join
```

### Leave Channel
```http
DELETE /api/channels/{channel_id}/leave
```

### Get Channel Members
```http
GET /api/channels/{channel_id}/members
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "alice",
    "full_name": "Alice Johnson",
    "profile_pic": "https://example.com/pic.jpg"
  }
]
```

---

## Messages API

### Get Channel Messages
```http
GET /api/messages/channel/{channel_id}
```

**Query Parameters:**
- `skip` (int): Number of messages to skip (default: 0)
- `limit` (int): Maximum messages to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "content": "Hello everyone!",
    "sender_id": 1,
    "sender": {
      "username": "alice",
      "full_name": "Alice Johnson",
      "profile_pic": "https://example.com/pic.jpg"
    },
    "channel_id": 1,
    "created_at": "2024-01-01T10:30:00",
    "updated_at": null,
    "is_edited": false
  }
]
```

### Send Message
```http
POST /api/messages/
```

**Request Body:**
```json
{
  "content": "Hello everyone!",
  "channel_id": 1
}
```

### Update Message
```http
PUT /api/messages/{message_id}
```

**Request Body:**
```json
{
  "content": "Updated message content"
}
```

### Delete Message
```http
DELETE /api/messages/{message_id}
```

---

## Direct Messages API

### List All DM Conversations
```http
GET /api/direct-messages/
```

**Response:**
```json
[
  {
    "user_id": 2,
    "username": "bob",
    "full_name": "Bob Smith",
    "profile_pic": "https://example.com/bob.jpg",
    "last_message": "See you tomorrow!",
    "last_message_time": "2024-01-01T15:30:00",
    "unread_count": 2
  }
]
```

### Get DM Conversation
```http
GET /api/direct-messages/conversation/{user_id}
```

**Query Parameters:**
- `skip` (int): Number of messages to skip (default: 0)
- `limit` (int): Maximum messages to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "content": "Hi Bob!",
    "sender_id": 1,
    "sender": {
      "username": "alice",
      "full_name": "Alice Johnson"
    },
    "receiver_id": 2,
    "created_at": "2024-01-01T14:00:00"
  }
]
```

### Send Direct Message
```http
POST /api/direct-messages/
```

**Request Body:**
```json
{
  "content": "Hi there!",
  "receiver_id": 2
}
```

### Update DM
```http
PUT /api/direct-messages/{dm_id}
```

**Request Body:**
```json
{
  "content": "Updated message"
}
```

### Delete DM
```http
DELETE /api/direct-messages/{dm_id}
```

---

## Canvas API

### List All Canvases
```http
GET /api/canvas/
```

**Query Parameters:**
- `skip` (int): Number to skip (default: 0)
- `limit` (int): Maximum to return (default: 50)
- `channel_id` (int): Filter by channel

**Response:**
```json
[
  {
    "id": 1,
    "title": "Project Planning",
    "content": "[{\"id\":1,\"text\":\"Task 1\",\"type\":\"text\"}]",
    "channel_id": 1,
    "owner_id": 1,
    "owner": {
      "username": "alice",
      "full_name": "Alice Johnson"
    },
    "is_public": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
]
```

### Create Canvas
```http
POST /api/canvas/
```

**Request Body:**
```json
{
  "title": "New Canvas",
  "content": "[{\"id\":1,\"text\":\"Start here\",\"type\":\"text\"}]",
  "channel_id": 1,
  "is_public": true
}
```

### Get Canvas by ID
```http
GET /api/canvas/{canvas_id}
```

### Update Canvas
```http
PUT /api/canvas/{canvas_id}
```

**Request Body:**
```json
{
  "title": "Updated Canvas",
  "content": "[{\"id\":1,\"text\":\"Updated content\"}]",
  "is_public": false
}
```

### Delete Canvas
```http
DELETE /api/canvas/{canvas_id}
```

---

## Attachments API

### List All Attachments
```http
GET /api/attachments/
```

**Query Parameters:**
- `skip` (int): Number to skip (default: 0)
- `limit` (int): Maximum to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "file_name": "document.pdf",
    "file_path": "/uploads/abc123.pdf",
    "file_size": 1024000,
    "file_type": "application/pdf",
    "uploaded_at": "2024-01-01T10:00:00",
    "uploader_id": 1,
    "uploader_name": "alice",
    "channel_id": 1,
    "message_id": 10
  }
]
```

### Upload Attachment
```http
POST /api/attachments/
```

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file`: File to upload
- `channel_id` (optional): Channel ID
- `message_id` (optional): Message ID

**Response:**
```json
{
  "id": 1,
  "file_name": "document.pdf",
  "file_path": "/uploads/abc123.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "uploaded_at": "2024-01-01T10:00:00"
}
```

### Get Attachment Metadata
```http
GET /api/attachments/{attachment_id}
```

### Download Attachment
```http
GET /api/attachments/{attachment_id}/download
```

### Delete Attachment
```http
DELETE /api/attachments/{attachment_id}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Data Models

### User
```typescript
{
  id: number
  username: string
  email: string
  full_name: string
  profile_pic: string | null
  is_online: boolean
  status: string
  created_at: datetime
}
```

### Channel
```typescript
{
  id: number
  name: string
  description: string | null
  is_private: boolean
  created_at: datetime
  member_count: number
}
```

### Message
```typescript
{
  id: number
  content: string
  sender_id: number
  sender: User
  channel_id: number
  created_at: datetime
  updated_at: datetime | null
  is_edited: boolean
}
```

### DirectMessage
```typescript
{
  id: number
  content: string
  sender_id: number
  sender: User
  receiver_id: number
  created_at: datetime
  updated_at: datetime | null
}
```

### Canvas
```typescript
{
  id: number
  title: string
  content: string  // JSON string
  channel_id: number | null
  owner_id: number
  owner: User
  is_public: boolean
  created_at: datetime
  updated_at: datetime
}
```

### Attachment
```typescript
{
  id: number
  file_name: string
  file_path: string
  file_size: number
  file_type: string
  uploaded_at: datetime
  uploader_id: number
  uploader_name: string
  channel_id: number | null
  message_id: number | null
}
```

---

## Rate Limiting

Currently not implemented. For production, consider:
- 100 requests per minute per IP
- 1000 requests per hour per user

## CORS

Configured to allow requests from:
- http://localhost:5173
- http://localhost:3000

For production, update `ALLOWED_ORIGINS` in environment variables.

---

## Interactive Documentation

For interactive API testing, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
