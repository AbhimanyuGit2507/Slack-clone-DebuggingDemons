from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Notification Schemas
class NotificationBase(BaseModel):
    notification_type: str
    title: str
    message: str
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    data: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None

class NotificationSchema(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# Pinned Message Schemas
class PinnedMessageCreate(BaseModel):
    message_id: int
    channel_id: int

class PinnedMessageSchema(BaseModel):
    id: int
    message_id: int
    channel_id: int
    pinned_by: int
    pinned_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Bookmark Schemas
class BookmarkCreate(BaseModel):
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None
    note: Optional[str] = None

class BookmarkSchema(BaseModel):
    id: int
    user_id: int
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Draft Schemas
class DraftCreate(BaseModel):
    channel_id: Optional[int] = None
    receiver_id: Optional[int] = None
    content: str
    formatting: Optional[str] = None
    mentions: Optional[str] = None

class DraftUpdate(BaseModel):
    content: Optional[str] = None
    formatting: Optional[str] = None
    mentions: Optional[str] = None

class DraftSchema(BaseModel):
    id: int
    user_id: int
    channel_id: Optional[int] = None
    receiver_id: Optional[int] = None
    content: str
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Scheduled Message Schemas
class ScheduledMessageCreate(BaseModel):
    channel_id: Optional[int] = None
    receiver_id: Optional[int] = None
    content: str
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    scheduled_for: datetime

class ScheduledMessageUpdate(BaseModel):
    content: Optional[str] = None
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    scheduled_for: Optional[datetime] = None

class ScheduledMessageSchema(BaseModel):
    id: int
    user_id: int
    channel_id: Optional[int] = None
    receiver_id: Optional[int] = None
    content: str
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    scheduled_for: datetime
    status: str
    created_at: datetime
    sent_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# User Presence Schemas
class UserPresenceUpdate(BaseModel):
    presence: str  # online, away, dnd, offline

class UserStatusUpdate(BaseModel):
    status_text: Optional[str] = None
    status_emoji: Optional[str] = None
    status_expires_at: Optional[datetime] = None
