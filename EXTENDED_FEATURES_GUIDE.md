# 🚀 Extended Slack Features - Implementation Guide

This document provides detailed information about additional Slack-like features that can be added to your backend. The features are prioritized and include implementation examples.

## 📊 Feature Priority Matrix

| Feature | Priority | Complexity | User Value | Implementation Time |
|---------|----------|------------|------------|-------------------|
| Activity Feed/Notifications | 🔴 HIGH | Medium | Very High | 4-6 hours |
| Pinned Messages | 🔴 HIGH | Low | High | 2-3 hours |
| Bookmarks/Saved Items | 🔴 HIGH | Low | High | 2-3 hours |
| Enhanced Presence | 🔴 HIGH | Low | Medium | 2-3 hours |
| File Management UI | 🟡 MEDIUM | Medium | High | 4-5 hours |
| Message Drafts | 🟡 MEDIUM | Low | Medium | 2-3 hours |
| User Groups | 🟡 MEDIUM | Medium | Medium | 5-6 hours |
| Message Scheduling | 🟡 MEDIUM | Medium | Medium | 4-5 hours |
| Reminders | 🟢 LOW | Medium | Medium | 4-5 hours |
| Custom Emojis | 🟢 LOW | Medium | Low | 3-4 hours |
| Polls | 🟢 LOW | Medium | Low | 3-4 hours |
| Analytics | 🟢 LOW | High | Low | 8-10 hours |

---

## 🎯 Feature 1: Activity Feed & Notifications (HIGH PRIORITY)

### What It Does
- Real-time notifications for user activities
- Mentions tracking
- Reaction notifications
- DM alerts
- Channel invitations
- Thread replies

### Database Schema
```python
# Already implemented in models_extended.py
class Notification:
    - user_id: Who receives the notification
    - notification_type: mention, reaction, dm, invite, thread_reply
    - title: Short notification title
    - message: Notification content
    - source_type: message, channel, user
    - source_id: ID of the source entity
    - is_read: Read status
    - data: JSON metadata
```

### API Endpoints (Already Implemented)
```
GET    /api/notifications                 - Get all notifications
GET    /api/notifications/unread-count    - Get unread count
POST   /api/notifications/{id}/read       - Mark as read
POST   /api/notifications/mark-all-read   - Mark all read
DELETE /api/notifications/{id}            - Delete notification
DELETE /api/notifications                 - Clear all
```

### Integration Points

#### 1. Create Notification When User is Mentioned
Add to `backend/routes/messages.py` after sending message:

```python
# In send_message() function
if mentions:
    from .notifications import create_notification
    mention_list = json.loads(mentions) if isinstance(mentions, str) else mentions
    for user_id in mention_list:
        create_notification(
            db=db,
            user_id=user_id,
            notification_type="mention",
            title=f"{current_user.username} mentioned you",
            message=f"in #{channel.name}: {content[:50]}...",
            source_type="message",
            source_id=new_message.id,
            data={"channel_id": channel_id, "channel_name": channel.name}
        )
```

#### 2. Create Notification When Message is Reacted
Add to `backend/routes/messages.py` in `add_reaction()`:

```python
# After creating reaction
from .notifications import create_notification
message_owner = message.user
if message_owner.id != current_user.id:
    create_notification(
        db=db,
        user_id=message_owner.id,
        notification_type="reaction",
        title=f"{current_user.username} reacted to your message",
        message=f"with {emoji}",
        source_type="message",
        source_id=message_id,
        data={"emoji": emoji, "channel_id": message.channel_id}
    )
```

#### 3. Create Notification for New DM
Add to `backend/routes/direct_messages.py` in `send_direct_message()`:

```python
# After creating DM
from .notifications import create_notification
create_notification(
    db=db,
    user_id=receiver_id,
    notification_type="dm",
    title=f"New message from {current_user.username}",
    message=content[:100],
    source_type="direct_message",
    source_id=new_dm.id
)
```

### Frontend Integration
```javascript
// Poll for new notifications every 30 seconds
setInterval(async () => {
  const response = await axios.get('/api/notifications/unread-count');
  updateNotificationBadge(response.data.unread_count);
}, 30000);

// Fetch notifications
const notifications = await axios.get('/api/notifications?unread_only=true');
```

---

## 📌 Feature 2: Pinned Messages (HIGH PRIORITY)

### What It Does
- Pin important messages to channel top
- Quick access to pinned items
- Only members can view pins
- Creators and pinners can unpin

### Database Schema
```python
# Already implemented in models_extended.py
class PinnedMessage:
    - message_id: The message being pinned
    - channel_id: Channel containing the message
    - pinned_by: User who pinned it
    - pinned_at: Timestamp
```

### API Endpoints (Already Implemented)
```
POST   /api/pins/channels/{channel_id}/messages/{message_id}  - Pin message
GET    /api/pins/channels/{channel_id}                        - Get all pins
DELETE /api/pins/channels/{channel_id}/messages/{message_id}  - Unpin message
```

### Usage Example
```python
# Pin a message
response = requests.post(
    "http://localhost:8000/api/pins/channels/1/messages/42",
    cookies={"session_id": session_cookie}
)

# Get pinned messages
response = requests.get(
    "http://localhost:8000/api/pins/channels/1",
    cookies={"session_id": session_cookie}
)
```

### Frontend Integration
```javascript
// Pin message
await axios.post(`/api/pins/channels/${channelId}/messages/${messageId}`);

// Show pins in channel header
const pins = await axios.get(`/api/pins/channels/${channelId}`);
displayPinnedMessages(pins.data);
```

---

## 🔖 Feature 3: Bookmarks (HIGH PRIORITY)

### What It Does
- Save messages for later reference
- Personal bookmark collection
- Add notes to bookmarks
- Bookmark both channel messages and DMs

### Database Schema
```python
# Already implemented in models_extended.py
class Bookmark:
    - user_id: Owner of bookmark
    - message_id: Bookmarked channel message (nullable)
    - direct_message_id: Bookmarked DM (nullable)
    - note: Optional personal note
    - created_at: When bookmarked
```

### API Endpoints (Already Implemented)
```
POST   /api/bookmarks              - Create bookmark
GET    /api/bookmarks              - Get all bookmarks
DELETE /api/bookmarks/{id}         - Delete bookmark
PUT    /api/bookmarks/{id}/note    - Update note
```

### Usage Example
```python
# Bookmark a message
response = requests.post(
    "http://localhost:8000/api/bookmarks",
    json={
        "message_id": 42,
        "note": "Important information about project"
    },
    cookies={"session_id": session_cookie}
)

# Get all bookmarks
response = requests.get(
    "http://localhost:8000/api/bookmarks",
    cookies={"session_id": session_cookie}
)
```

### Frontend Integration
```javascript
// Add bookmark button to each message
<button onClick={() => bookmarkMessage(messageId)}>
  <BookmarkIcon />
</button>

// Bookmark function
const bookmarkMessage = async (messageId) => {
  await axios.post('/api/bookmarks', { message_id: messageId });
  showToast('Message bookmarked!');
};

// Show bookmarks page
const bookmarks = await axios.get('/api/bookmarks');
```

---

## 🟢 Feature 4: Enhanced User Presence

### What You Need to Add
Update `backend/models.py` User model:

```python
# Add these columns to User model
presence = Column(String, default="offline")  # online, away, dnd, offline
status_text = Column(String, nullable=True)
status_emoji = Column(String, nullable=True)
status_expires_at = Column(DateTime, nullable=True)
last_activity_at = Column(DateTime, default=datetime.utcnow)
```

### New Endpoints to Create
```python
# backend/routes/users.py

@router.put("/me/presence")
def update_presence(
    presence_data: UserPresenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user presence status"""
    if presence_data.presence not in ["online", "away", "dnd", "offline"]:
        raise HTTPException(status_code=400, detail="Invalid presence status")
    
    current_user.presence = presence_data.presence
    current_user.last_activity_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Presence updated", "presence": presence_data.presence}


@router.put("/me/status")
def update_status(
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user status message"""
    current_user.status_text = status_data.status_text
    current_user.status_emoji = status_data.status_emoji
    current_user.status_expires_at = status_data.status_expires_at
    db.commit()
    
    return {"message": "Status updated"}
```

---

## 📁 Feature 5: Enhanced File Management

### What to Add
Create new endpoints in `backend/routes/attachments.py`:

```python
@router.get("/files/all")
def browse_all_files(
    skip: int = 0,
    limit: int = 50,
    file_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Browse all files accessible to user"""
    # Query attachments from channels user is member of
    query = db.query(Attachment).join(Message).join(Channel).filter(
        Channel.members.contains(current_user)
    )
    
    if file_type:
        query = query.filter(Attachment.file_type == file_type)
    
    files = query.order_by(Attachment.uploaded_at.desc()).offset(skip).limit(limit).all()
    return files


@router.get("/files/recent")
def get_recent_files(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recently uploaded files"""
    # Get files from last 7 days
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=7)
    
    files = db.query(Attachment).join(Message).join(Channel).filter(
        Channel.members.contains(current_user),
        Attachment.uploaded_at >= cutoff
    ).order_by(Attachment.uploaded_at.desc()).limit(limit).all()
    
    return files


@router.get("/files/stats")
def get_storage_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get storage statistics for user's files"""
    # Count files by type
    stats = db.query(
        Attachment.file_type,
        func.count(Attachment.id).label('count'),
        func.sum(Attachment.file_size).label('total_size')
    ).join(Message).filter(
        Message.user_id == current_user.id
    ).group_by(Attachment.file_type).all()
    
    return {
        "stats": [
            {"type": s.file_type, "count": s.count, "size": s.total_size}
            for s in stats
        ]
    }
```

---

## 💾 Feature 6: Message Drafts

### Implementation Steps

1. **Models already created** in `models_extended.py`

2. **Create router** `backend/routes/drafts.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, Draft, Channel
from ..schemas import DraftCreate, DraftUpdate, DraftSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/drafts", tags=["drafts"])


@router.post("/", response_model=DraftSchema)
def save_draft(
    draft_data: DraftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save or update a draft"""
    # Check if draft already exists for this channel/receiver
    existing_draft = db.query(Draft).filter(
        Draft.user_id == current_user.id,
        Draft.channel_id == draft_data.channel_id,
        Draft.receiver_id == draft_data.receiver_id
    ).first()
    
    if existing_draft:
        # Update existing draft
        existing_draft.content = draft_data.content
        existing_draft.formatting = draft_data.formatting
        existing_draft.mentions = draft_data.mentions
        existing_draft.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_draft)
        return existing_draft
    
    # Create new draft
    draft = Draft(
        user_id=current_user.id,
        channel_id=draft_data.channel_id,
        receiver_id=draft_data.receiver_id,
        content=draft_data.content,
        formatting=draft_data.formatting,
        mentions=draft_data.mentions
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


@router.get("/", response_model=List[DraftSchema])
def get_drafts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all drafts for current user"""
    drafts = db.query(Draft).filter(
        Draft.user_id == current_user.id
    ).order_by(Draft.updated_at.desc()).all()
    return drafts


@router.get("/channel/{channel_id}", response_model=DraftSchema)
def get_channel_draft(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get draft for specific channel"""
    draft = db.query(Draft).filter(
        Draft.user_id == current_user.id,
        Draft.channel_id == channel_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")
    
    return draft


@router.delete("/{draft_id}")
def delete_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a draft"""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == current_user.id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    db.delete(draft)
    db.commit()
    return {"message": "Draft deleted"}
```

3. **Add to main.py**:
```python
from backend.routes import drafts
app.include_router(drafts.router)
```

4. **Frontend integration**:
```javascript
// Auto-save draft every 2 seconds
let draftTimeout;
messageInput.addEventListener('input', (e) => {
  clearTimeout(draftTimeout);
  draftTimeout = setTimeout(async () => {
    await axios.post('/api/drafts', {
      channel_id: currentChannelId,
      content: e.target.value
    });
  }, 2000);
});

// Load draft when opening channel
const draft = await axios.get(`/api/drafts/channel/${channelId}`);
if (draft.data) {
  messageInput.value = draft.data.content;
}
```

---

## 📋 Implementation Checklist

### ✅ Already Completed
- [x] Models created in `models_extended.py`
- [x] Schemas created in `schemas_extended.py`
- [x] Notifications router implemented
- [x] Pins router implemented
- [x] Bookmarks router implemented

### 🔨 To Integrate
- [ ] Add notification imports to existing routes
- [ ] Call `create_notification()` on mentions
- [ ] Call `create_notification()` on reactions
- [ ] Call `create_notification()` on new DMs
- [ ] Add presence fields to User model
- [ ] Create drafts router
- [ ] Create scheduled messages router
- [ ] Add all new routers to main.py
- [ ] Update database migration/init

### 📝 To Update main.py

Add these lines to `backend/main.py`:

```python
from backend.routes import notifications, pins, bookmarks, drafts

# Include new routers
app.include_router(notifications.router)
app.include_router(pins.router)
app.include_router(bookmarks.router)
app.include_router(drafts.router)
```

---

## 🧪 Testing the New Features

### Test Notifications
```python
# 1. Send a message with mention
response = requests.post(
    "http://localhost:8000/api/messages/1",
    json={
        "content": "Hey @john check this out",
        "mentions": "[2]"  # User ID 2
    },
    cookies={"session_id": user1_session}
)

# 2. Check notifications as user 2
response = requests.get(
    "http://localhost:8000/api/notifications",
    cookies={"session_id": user2_session}
)
print(response.json())  # Should show mention notification
```

### Test Pins
```python
# Pin a message
response = requests.post(
    "http://localhost:8000/api/pins/channels/1/messages/5",
    cookies={"session_id": session_cookie}
)

# Get pins
response = requests.get(
    "http://localhost:8000/api/pins/channels/1",
    cookies={"session_id": session_cookie}
)
```

### Test Bookmarks
```python
# Bookmark a message
response = requests.post(
    "http://localhost:8000/api/bookmarks",
    json={
        "message_id": 10,
        "note": "Important deadline info"
    },
    cookies={"session_id": session_cookie}
)

# Get all bookmarks
response = requests.get(
    "http://localhost:8000/api/bookmarks",
    cookies={"session_id": session_cookie}
)
```

---

## 🎨 Frontend UI Suggestions

### Notifications Bell Icon
```jsx
<div className="notification-bell">
  <BellIcon />
  {unreadCount > 0 && (
    <span className="badge">{unreadCount}</span>
  )}
</div>
```

### Pinned Messages Banner
```jsx
<div className="pinned-messages-banner">
  <PinIcon /> {pins.length} pinned messages
  <button onClick={showPins}>View</button>
</div>
```

### Bookmark Button on Messages
```jsx
<div className="message-actions">
  <button onClick={() => bookmarkMessage(msg.id)}>
    <BookmarkIcon />
  </button>
</div>
```

---

## 📚 Additional Resources

### Recommended Reading
- [Slack API Documentation](https://api.slack.com/methods)
- [WebSocket for Real-time](https://fastapi.tiangolo.com/advanced/websockets/)
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

### Performance Tips
1. **Index frequently queried fields**
2. **Use pagination for large lists**
3. **Cache notification counts**
4. **Consider WebSocket for real-time notifications**
5. **Implement background jobs for scheduled messages**

---

## 🚀 Next Steps

1. **Immediate**: Integrate notification calls into existing message routes
2. **Short-term**: Add presence tracking and drafts
3. **Long-term**: Implement analytics and advanced features

Would you like me to help integrate any of these features into your existing backend?
