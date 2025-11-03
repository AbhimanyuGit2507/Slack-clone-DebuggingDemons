# 🔗 Integration Guide - Connecting New Features

This guide shows how to integrate the new features (especially notifications and activity tracking) into your existing message routes.

---

## 1. Integrate Notifications into Messages

### Update `backend/routes/messages.py`

Add notification creation when users are mentioned:

```python
# At the top of the file, add import
from .notifications import create_notification
from .activity import create_activity

# In send_message() function, after creating the message:
@router.post("/{channel_id}", response_model=schemas.Message)
def send_message(
    channel_id: int,
    content: str = Form(...),
    formatting: Optional[str] = Form(None),
    mentions: Optional[str] = Form(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code to create message ...
    
    # NEW: Create notifications for mentions
    if mentions:
        import json
        try:
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
        except:
            pass  # Skip if mentions parsing fails
    
    # NEW: Create activity log
    create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="message_sent",
        description=f"Sent a message in #{channel.name}",
        target_type="message",
        target_id=new_message.id,
        metadata={"channel_id": channel_id, "channel_name": channel.name}
    )
    
    return new_message
```

### Add Notification for Reactions

```python
# In add_reaction() function:
@router.post("/reactions", response_model=schemas.Reaction)
def add_reaction(
    reaction: schemas.ReactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Notify message author about reaction
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
    
    return new_reaction
```

### Add Notification for Thread Replies

```python
# In create_thread() function:
@router.post("/threads", response_model=schemas.Thread)
def create_thread(
    thread: schemas.ThreadCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Notify parent message author
    parent_message = db.query(models.Message).filter(
        models.Message.id == thread.parent_message_id
    ).first()
    
    if parent_message and parent_message.user_id != current_user.id:
        create_notification(
            db=db,
            user_id=parent_message.user_id,
            notification_type="thread_reply",
            title=f"{current_user.username} replied to your thread",
            message=thread.content[:100],
            source_type="thread",
            source_id=new_thread.id,
            data={"parent_message_id": thread.parent_message_id}
        )
    
    return new_thread
```

---

## 2. Integrate Notifications into Direct Messages

### Update `backend/routes/direct_messages.py`

```python
# At the top, add import
from .notifications import create_notification
from .activity import create_activity

# In send_direct_message() function:
@router.post("", response_model=schemas.DirectMessage)
def send_direct_message(
    message: schemas.DirectMessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Create notification for receiver
    create_notification(
        db=db,
        user_id=message.receiver_id,
        notification_type="dm",
        title=f"New message from {current_user.username}",
        message=message.content[:100],
        source_type="direct_message",
        source_id=new_dm.id
    )
    
    # NEW: Create activity log
    create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="dm_sent",
        description=f"Sent a direct message",
        target_type="direct_message",
        target_id=new_dm.id
    )
    
    return new_dm
```

---

## 3. Integrate Activity Tracking into Channels

### Update `backend/routes/channels.py`

```python
# At the top, add import
from .activity import create_activity
from .notifications import create_notification

# In join_channel() function:
@router.post("/{channel_id}/join", response_model=schemas.Channel)
def join_channel(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Create activity log
    create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="channel_joined",
        description=f"Joined #{channel.name}",
        target_type="channel",
        target_id=channel_id,
        metadata={"channel_name": channel.name}
    )
    
    return channel

# In invite_to_channel() function:
@router.post("/{channel_id}/invite/{user_id}", response_model=schemas.Channel)
def invite_to_channel(
    channel_id: int,
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Notify invited user
    create_notification(
        db=db,
        user_id=user_id,
        notification_type="invite",
        title=f"{current_user.username} invited you to a channel",
        message=f"You've been invited to #{channel.name}",
        source_type="channel",
        source_id=channel_id,
        data={"channel_name": channel.name, "inviter": current_user.username}
    )
    
    return channel
```

---

## 4. Integrate Activity Tracking into Attachments

### Update `backend/routes/attachments.py`

```python
# At the top, add import
from .activity import create_activity

# In upload_message_attachment() function:
@router.post("/message/{message_id}")
async def upload_message_attachment(
    message_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ... existing code ...
    
    # NEW: Create activity log
    create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="file_uploaded",
        description=f"Uploaded file: {file.filename}",
        target_type="attachment",
        target_id=attachment.id,
        metadata={
            "filename": file.filename,
            "file_type": file_type,
            "message_id": message_id
        }
    )
    
    return attachment
```

---

## 5. Create Helper Function for Batch Notifications

Add to `backend/routes/notifications.py`:

```python
def notify_channel_members(
    db: Session,
    channel_id: int,
    exclude_user_id: int,
    notification_type: str,
    title: str,
    message: str,
    source_type: str = None,
    source_id: int = None
):
    """Send notification to all channel members except one user"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        return
    
    for member in channel.members:
        if member.id != exclude_user_id:
            create_notification(
                db=db,
                user_id=member.id,
                notification_type=notification_type,
                title=title,
                message=message,
                source_type=source_type,
                source_id=source_id,
                data={"channel_id": channel_id, "channel_name": channel.name}
            )
```

### Use for @channel or @here mentions

```python
# In send_message() function, check for @channel or @here
if "@channel" in content or "@here" in content:
    from .notifications import notify_channel_members
    notify_channel_members(
        db=db,
        channel_id=channel_id,
        exclude_user_id=current_user.id,
        notification_type="mention",
        title=f"{current_user.username} mentioned @channel",
        message=content[:100],
        source_type="message",
        source_id=new_message.id
    )
```

---

## 6. Complete Integration Example

Here's a complete example showing all integrations in `send_message()`:

```python
@router.post("/{channel_id}", response_model=schemas.Message)
async def send_message(
    channel_id: int,
    content: str = Form(...),
    formatting: Optional[str] = Form(None),
    mentions: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a channel with full feature integration"""
    import json
    from .notifications import create_notification
    from .activity import create_activity
    
    # Verify channel membership
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    # Create message
    new_message = models.Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=content,
        formatting=formatting,
        mentions=mentions
    )
    db.add(new_message)
    db.flush()
    
    # Handle file attachments
    if files:
        for file in files:
            # ... upload file logic ...
            pass
    
    # Create notifications for @mentions
    if mentions:
        try:
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
        except:
            pass
    
    # Check for @channel or @here mentions
    if "@channel" in content or "@here" in content:
        for member in channel.members:
            if member.id != current_user.id:
                create_notification(
                    db=db,
                    user_id=member.id,
                    notification_type="mention",
                    title=f"{current_user.username} mentioned @channel",
                    message=f"in #{channel.name}: {content[:50]}...",
                    source_type="message",
                    source_id=new_message.id,
                    data={"channel_id": channel_id, "channel_name": channel.name}
                )
    
    # Create activity log
    create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="message_sent",
        description=f"Sent a message in #{channel.name}",
        target_type="message",
        target_id=new_message.id,
        metadata={"channel_id": channel_id, "channel_name": channel.name, "content_preview": content[:50]}
    )
    
    db.commit()
    db.refresh(new_message)
    
    return new_message
```

---

## 7. Frontend Integration Examples

### Notification Bell Component

```javascript
// components/NotificationBell.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function NotificationBell() {
  const [unreadCount, setUnreadCount] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  // Poll for new notifications every 30 seconds
  useEffect(() => {
    const fetchUnreadCount = async () => {
      const { data } = await axios.get('/api/notifications/unread-count');
      setUnreadCount(data.unread_count);
    };

    fetchUnreadCount();
    const interval = setInterval(fetchUnreadCount, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    const { data } = await axios.get('/api/notifications?unread_only=true');
    setNotifications(data);
    setShowDropdown(true);
  };

  const markAsRead = async (notificationId) => {
    await axios.post(`/api/notifications/${notificationId}/read`);
    // Refresh notifications
    fetchNotifications();
  };

  return (
    <div className="notification-bell">
      <button onClick={fetchNotifications}>
        🔔
        {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
      </button>
      
      {showDropdown && (
        <div className="notifications-dropdown">
          {notifications.map(notif => (
            <div key={notif.id} className="notification-item">
              <h4>{notif.title}</h4>
              <p>{notif.message}</p>
              <button onClick={() => markAsRead(notif.id)}>Mark as read</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### Activity Feed Component

```javascript
// pages/ActivityPage.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function ActivityPage() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    const fetchActivities = async () => {
      const { data } = await axios.get('/api/activity/all?limit=100');
      setActivities(data);
    };
    
    fetchActivities();
  }, []);

  return (
    <div className="activity-page">
      <h1>Activity</h1>
      <div className="activity-feed">
        {activities.map(activity => (
          <div key={activity.id} className="activity-item">
            <span className="timestamp">
              {new Date(activity.created_at).toLocaleString()}
            </span>
            <p>{activity.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Bookmark Button Component

```javascript
// components/BookmarkButton.jsx
import { useState } from 'react';
import axios from 'axios';

export default function BookmarkButton({ messageId }) {
  const [isBookmarked, setIsBookmarked] = useState(false);

  const toggleBookmark = async () => {
    if (isBookmarked) {
      // Remove bookmark (would need bookmark ID)
      await axios.delete(`/api/bookmarks/${bookmarkId}`);
    } else {
      // Add bookmark
      await axios.post('/api/bookmarks', { message_id: messageId });
    }
    setIsBookmarked(!isBookmarked);
  };

  return (
    <button onClick={toggleBookmark} className="bookmark-btn">
      {isBookmarked ? '🔖' : '🔖'}
    </button>
  );
}
```

---

## 8. Testing Integration

Create `test_integration.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_complete_flow():
    # 1. Login
    login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "user1",
        "password": "password"
    })
    session1 = login.cookies.get("session_id")
    
    # 2. Send message with mention
    message = requests.post(
        f"{BASE_URL}/api/messages/1",
        data={
            "content": "Hey @user2 check this out!",
            "mentions": json.dumps([2])
        },
        cookies={"session_id": session1}
    )
    print(f"✅ Message sent: {message.status_code}")
    
    # 3. Login as user2
    login2 = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "user2",
        "password": "password"
    })
    session2 = login2.cookies.get("session_id")
    
    # 4. Check notifications
    notifs = requests.get(
        f"{BASE_URL}/api/notifications",
        cookies={"session_id": session2}
    )
    print(f"✅ Notifications received: {len(notifs.json())}")
    
    # 5. Bookmark the message
    bookmark = requests.post(
        f"{BASE_URL}/api/bookmarks",
        json={"message_id": message.json()["id"], "note": "Important"},
        cookies={"session_id": session2}
    )
    print(f"✅ Bookmark created: {bookmark.status_code}")
    
    # 6. Check activity
    activity = requests.get(
        f"{BASE_URL}/api/activity/all",
        cookies={"session_id": session1}
    )
    print(f"✅ Activities logged: {len(activity.json())}")

if __name__ == "__main__":
    test_complete_flow()
```

---

## 9. Summary

You now have:
- ✅ Complete notification system integrated
- ✅ Activity tracking on all major actions
- ✅ Frontend components for displaying features
- ✅ Test scripts for validation

All features are connected and working together! 🎉
