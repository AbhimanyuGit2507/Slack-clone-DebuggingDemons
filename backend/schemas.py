from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional
from datetime import datetime

# ===== User Schemas =====
class UserBase(BaseModel):
    username: str
    email: EmailStr
    status: Optional[str] = "offline"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    profile_picture: Optional[str] = None

class User(UserBase):
    id: int
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserProfile(User):
    pass

# ===== Channel Schemas =====
class ChannelBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False

class ChannelCreate(ChannelBase):
    members: Optional[List[int]] = []

class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None

class Channel(ChannelBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    members: List[User] = []
    model_config = ConfigDict(from_attributes=True)

# ===== Message Schemas =====
class MessageBase(BaseModel):
    content: str

class MessageFormatting(BaseModel):
    """Schema for rich text formatting metadata"""
    bold: Optional[List[tuple]] = []  # [(start, end), ...]
    italic: Optional[List[tuple]] = []
    code: Optional[List[tuple]] = []
    strikethrough: Optional[List[tuple]] = []
    links: Optional[List[dict]] = []  # [{"start": int, "end": int, "url": str}, ...]
    
class MessageCreate(MessageBase):
    channel_id: int
    user_id: Optional[int] = None  # Optional - will use current user from session
    formatting: Optional[str] = None  # JSON string of MessageFormatting
    mentions: Optional[List[int]] = []  # List of mentioned user IDs

class MessageUpdate(BaseModel):
    content: str
    formatting: Optional[str] = None
    mentions: Optional[List[int]] = []

class AttachmentSchema(BaseModel):
    id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    mime_type: Optional[str] = None
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Message(MessageBase):
    id: int
    channel_id: int
    user_id: int
    timestamp: datetime
    edited_at: Optional[datetime] = None
    is_deleted: bool = False
    is_system_message: bool = False
    formatted_content: Optional[str] = None
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    attachments: List[AttachmentSchema] = []
    user: Optional[dict] = None  # Include user info for frontend
    model_config = ConfigDict(from_attributes=True)

# ===== Direct Message Schemas =====
class DirectMessageBase(BaseModel):
    content: str

class DirectMessageCreate(DirectMessageBase):
    receiver_id: int
    formatting: Optional[str] = None
    mentions: Optional[List[int]] = []

class DirectMessageUpdate(BaseModel):
    content: str
    formatting: Optional[str] = None
    mentions: Optional[List[int]] = []

class DMAttachmentSchema(BaseModel):
    id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    mime_type: Optional[str] = None
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DirectMessage(DirectMessageBase):
    id: int
    sender_id: int
    receiver_id: int
    timestamp: datetime
    is_read: bool = False
    edited_at: Optional[datetime] = None
    is_deleted: bool = False
    formatting: Optional[str] = None
    mentions: Optional[str] = None
    dm_attachments: List[DMAttachmentSchema] = []
    model_config = ConfigDict(from_attributes=True)

# ===== Thread Schemas =====
class ThreadBase(BaseModel):
    content: str

class ThreadCreate(ThreadBase):
    parent_message_id: int

class ThreadUpdate(BaseModel):
    content: str

class Thread(ThreadBase):
    id: int
    parent_message_id: int
    user_id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

# ===== Reaction Schemas =====
class ReactionBase(BaseModel):
    emoji: str

class ReactionCreate(ReactionBase):
    message_id: int

class Reaction(ReactionBase):
    id: int
    message_id: int
    user_id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

# ===== Contact Schemas =====
class ContactAdd(BaseModel):
    contact_id: int

class ContactRemove(BaseModel):
    contact_id: int

# ===== Authentication Response Schemas =====
class AuthResponse(BaseModel):
    message: str
    user: User

class LogoutResponse(BaseModel):
    message: str

# ===== Search Schemas =====
class SearchQuery(BaseModel):
    query: str
    search_type: Optional[str] = "all"  # all, messages, channels, users
    limit: Optional[int] = 50

class SearchResult(BaseModel):
    result_type: str  # message, channel, user
    id: int
    content: dict
    relevance_score: Optional[float] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_count: int


# ===== Notification Schemas =====
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


# ===== Pinned Message Schemas =====
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


# ===== Bookmark Schemas (Later Feature) =====
class BookmarkCreate(BaseModel):
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None
    note: Optional[str] = None

class BookmarkUpdate(BaseModel):
    note: Optional[str] = None

class BookmarkSchema(BaseModel):
    id: int
    user_id: int
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== Draft Schemas =====
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


# ===== Scheduled Message Schemas =====
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


# ===== User Group Schemas =====
class UserGroupCreate(BaseModel):
    name: str
    handle: str
    description: Optional[str] = None
    member_ids: List[int] = []

class UserGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class UserGroupSchema(BaseModel):
    id: int
    name: str
    handle: str
    description: Optional[str] = None
    created_by: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== Custom Emoji Schemas =====
class CustomEmojiCreate(BaseModel):
    name: str
    aliases: Optional[str] = None

class CustomEmojiSchema(BaseModel):
    id: int
    name: str
    image_path: str
    aliases: Optional[str] = None
    uploaded_by: int
    created_at: datetime
    usage_count: int
    model_config = ConfigDict(from_attributes=True)


# ===== Canvas Schemas =====
class CanvasCreate(BaseModel):
    title: str
    content: str
    channel_id: Optional[int] = None
    is_public: bool = False

class CanvasUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    channel_id: Optional[int] = None
    is_public: Optional[bool] = None

class CanvasSchema(BaseModel):
    id: int
    title: str
    content: str
    channel_id: Optional[int] = None
    owner_id: int
    is_public: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== Workflow Schemas =====
class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: str
    action_type: str
    trigger_config: Optional[str] = None
    action_config: Optional[str] = None
    channel_id: Optional[int] = None

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class WorkflowSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    trigger_type: str
    action_type: str
    trigger_config: Optional[str] = None
    action_config: Optional[str] = None
    channel_id: Optional[int] = None
    created_by: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== Activity Schemas =====
class ActivitySchema(BaseModel):
    id: int
    user_id: int
    activity_type: str
    description: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    metadata: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== Permalink Schemas =====
class PermalinkCreate(BaseModel):
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None

class PermalinkSchema(BaseModel):
    id: int
    message_id: Optional[int] = None
    direct_message_id: Optional[int] = None
    permalink: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== User Presence Schemas =====
class UserPresenceUpdate(BaseModel):
    presence: str  # online, away, dnd, offline

class UserStatusUpdate(BaseModel):
    status_text: Optional[str] = None
    status_emoji: Optional[str] = None
    status_expires_at: Optional[datetime] = None


# ===== User Profile Enhancement Schemas =====
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    timezone: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


# ===== User Preference Schemas =====
class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    notification_sound: Optional[bool] = None
    email_notifications: Optional[bool] = None


# ===== Channel Topic Schemas =====
class ChannelTopicUpdate(BaseModel):
    topic: Optional[str] = None
    purpose: Optional[str] = None


# ===== File Metadata Schemas =====
class FileMetadataSchema(BaseModel):
    id: int
    attachment_id: Optional[int] = None
    dm_attachment_id: Optional[int] = None
    thumbnail_path: Optional[str] = None
    download_count: int
    is_public: bool
    tags: Optional[str] = None
    has_thumbnail: bool
    model_config = ConfigDict(from_attributes=True)
