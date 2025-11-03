from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

channel_members = Table(
    'channel_members', Base.metadata,
    Column('channel_id', Integer, ForeignKey('channels.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)

contacts = Table(
    'contacts', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('contact_id', Integer, ForeignKey('users.id'), primary_key=True),
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    status = Column(String, default='offline')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Enhanced presence and status
    presence = Column(String, default="offline")  # online, away, dnd, offline
    status_text = Column(String, nullable=True)
    status_emoji = Column(String, nullable=True)
    status_expires_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, default=datetime.utcnow)
    
    # Profile enhancements
    full_name = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # User preferences
    theme = Column(String, default='light')  # light, dark
    notification_sound = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    
    # For backward compatibility with existing seed data
    name = Column(String, nullable=True)

    channels = relationship('Channel', secondary=channel_members, back_populates='members')
    contacts_list = relationship(
        'User',
        secondary=contacts,
        primaryjoin=id == contacts.c.user_id,
        secondaryjoin=id == contacts.c.contact_id,
        backref='contacted_by'
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, status={self.status})>"

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Enhanced channel features
    topic = Column(String, nullable=True)
    purpose = Column(Text, nullable=True)
    topic_set_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    topic_set_at = Column(DateTime, nullable=True)
    
    # Channel sections support
    section = Column(String, nullable=True)  # For organizing channels into sections

    members = relationship('User', secondary=channel_members, back_populates='channels')
    messages = relationship('Message', back_populates='channel', cascade='all, delete-orphan')
    creator = relationship('User', foreign_keys=[created_by])
    topic_setter = relationship('User', foreign_keys=[topic_set_by])

    def __repr__(self):
        return f"<Channel(id={self.id}, name={self.name}, is_private={self.is_private})>"

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    edited_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    is_system_message = Column(Boolean, default=False)  # For system notifications
    
    # Rich text formatting support
    formatted_content = Column(Text, nullable=True)  # HTML content with formatting
    formatting = Column(Text, nullable=True)  # JSON string with formatting metadata
    mentions = Column(Text, nullable=True)  # JSON array of mentioned user IDs

    channel = relationship('Channel', back_populates='messages')
    user = relationship('User')
    threads = relationship('Thread', back_populates='parent_message', cascade='all, delete-orphan')
    reactions = relationship('Reaction', back_populates='message', cascade='all, delete-orphan')
    attachments = relationship('Attachment', back_populates='message', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Message(id={self.id}, channel_id={self.channel_id}, user_id={self.user_id})>"

class DirectMessage(Base):
    __tablename__ = 'direct_messages'
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    
    # Rich text formatting support
    formatted_content = Column(Text, nullable=True)  # HTML content with formatting
    formatting = Column(Text, nullable=True)  # JSON string with formatting metadata
    mentions = Column(Text, nullable=True)  # JSON array of mentioned user IDs

    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    dm_attachments = relationship('DirectMessageAttachment', back_populates='direct_message', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<DirectMessage(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id})>"

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True, index=True)
    parent_message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    parent_message = relationship('Message', back_populates='threads')
    user = relationship('User')

    def __repr__(self):
        return f"<Thread(id={self.id}, parent_message_id={self.parent_message_id}, user_id={self.user_id})>"

class Reaction(Base):
    __tablename__ = 'reactions'
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    emoji = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    message = relationship('Message', back_populates='reactions')
    user = relationship('User')

    def __repr__(self):
        return f"<Reaction(id={self.id}, message_id={self.message_id}, user_id={self.user_id}, emoji={self.emoji})>"

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # image, document, video, audio, etc.
    file_size = Column(Integer, nullable=False)  # in bytes
    mime_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    message = relationship('Message', back_populates='attachments')

    def __repr__(self):
        return f"<Attachment(id={self.id}, message_id={self.message_id}, filename={self.filename})>"

class DirectMessageAttachment(Base):
    __tablename__ = 'dm_attachments'
    id = Column(Integer, primary_key=True, index=True)
    direct_message_id = Column(Integer, ForeignKey('direct_messages.id'), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    direct_message = relationship('DirectMessage', back_populates='dm_attachments')

    def __repr__(self):
        return f"<DirectMessageAttachment(id={self.id}, dm_id={self.direct_message_id}, filename={self.filename})>"

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship('User')

    def __repr__(self):
        return f"<Session(id={self.id}, session_id={self.session_id}, user_id={self.user_id})>"


# ============= NEW FEATURES =============

class Notification(Base):
    """Activity feed and notifications"""
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notification_type = Column(String, nullable=False)  # mention, reaction, dm, invite, thread_reply, pin
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    
    # Reference to the source
    source_type = Column(String, nullable=True)  # message, channel, user, thread
    source_id = Column(Integer, nullable=True)
    
    # Metadata
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Related data (JSON)
    data = Column(Text, nullable=True)  # Additional JSON data
    
    user = relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type})>"


class PinnedMessage(Base):
    """Pinned messages in channels"""
    __tablename__ = 'pinned_messages'
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    pinned_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    pinned_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship('Message')
    channel = relationship('Channel')
    user = relationship('User', foreign_keys=[pinned_by])
    
    def __repr__(self):
        return f"<PinnedMessage(id={self.id}, message_id={self.message_id}, channel_id={self.channel_id})>"


class Bookmark(Base):
    """Saved messages for later (Later feature)"""
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Can bookmark either a message or DM
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=True)
    direct_message_id = Column(Integer, ForeignKey('direct_messages.id'), nullable=True)
    
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', foreign_keys=[user_id])
    message = relationship('Message', foreign_keys=[message_id])
    direct_message = relationship('DirectMessage', foreign_keys=[direct_message_id])
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id})>"


class Draft(Base):
    """Message drafts"""
    __tablename__ = 'drafts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Draft for either channel or DM
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    content = Column(Text, nullable=False)
    formatting = Column(Text, nullable=True)
    mentions = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', foreign_keys=[user_id])
    channel = relationship('Channel', foreign_keys=[channel_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    
    def __repr__(self):
        return f"<Draft(id={self.id}, user_id={self.user_id})>"


class ScheduledMessage(Base):
    """Scheduled messages"""
    __tablename__ = 'scheduled_messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Schedule for either channel or DM
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    content = Column(Text, nullable=False)
    formatting = Column(Text, nullable=True)
    mentions = Column(Text, nullable=True)
    
    scheduled_for = Column(DateTime, nullable=False)
    status = Column(String, default='pending')  # pending, sent, cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    
    user = relationship('User', foreign_keys=[user_id])
    channel = relationship('Channel', foreign_keys=[channel_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    
    def __repr__(self):
        return f"<ScheduledMessage(id={self.id}, scheduled_for={self.scheduled_for})>"


# Many-to-many for user group members
user_group_members = Table(
    'user_group_members', Base.metadata,
    Column('group_id', Integer, ForeignKey('user_groups.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)

class UserGroup(Base):
    """User groups for @mentions"""
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    handle = Column(String, unique=True, nullable=False)  # e.g., @developers
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    creator = relationship('User', foreign_keys=[created_by])
    members = relationship('User', secondary=user_group_members, backref='user_groups')
    
    def __repr__(self):
        return f"<UserGroup(id={self.id}, name={self.name}, handle={self.handle})>"


class CustomEmoji(Base):
    """Custom emojis"""
    __tablename__ = 'custom_emojis'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    image_path = Column(String, nullable=False)
    aliases = Column(Text, nullable=True)  # JSON array
    uploaded_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    usage_count = Column(Integer, default=0)
    
    uploader = relationship('User', foreign_keys=[uploaded_by])
    
    def __repr__(self):
        return f"<CustomEmoji(id={self.id}, name={self.name})>"


class Canvas(Base):
    """Canvas documents for collaboration"""
    __tablename__ = 'canvases'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Rich text content
    
    # Can be in channel or personal
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Access control
    is_public = Column(Boolean, default=False)
    
    channel = relationship('Channel', foreign_keys=[channel_id])
    owner = relationship('User', foreign_keys=[owner_id])
    
    def __repr__(self):
        return f"<Canvas(id={self.id}, title={self.title})>"


class Workflow(Base):
    """Workflow automations"""
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    trigger_type = Column(String, nullable=False)  # message, reaction, join, schedule
    action_type = Column(String, nullable=False)  # send_message, notify, webhook
    
    # Configuration (JSON)
    trigger_config = Column(Text, nullable=True)
    action_config = Column(Text, nullable=True)
    
    # Scope
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    channel = relationship('Channel', foreign_keys=[channel_id])
    creator = relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name={self.name})>"


class Activity(Base):
    """Activity tracking for Activity page"""
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String, nullable=False)  # message_sent, file_uploaded, channel_joined, etc.
    description = Column(Text, nullable=False)
    
    # Reference to related entity
    target_type = Column(String, nullable=True)  # message, channel, file
    target_id = Column(Integer, nullable=True)
    
    activity_metadata = Column(Text, nullable=True)  # JSON metadata (renamed from 'metadata' to avoid SQLAlchemy conflict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Activity(id={self.id}, user_id={self.user_id}, type={self.activity_type})>"


class Permalink(Base):
    """Permanent links to messages"""
    __tablename__ = 'permalinks'
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=True)
    direct_message_id = Column(Integer, ForeignKey('direct_messages.id'), nullable=True)
    
    permalink = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship('Message', foreign_keys=[message_id])
    direct_message = relationship('DirectMessage', foreign_keys=[direct_message_id])
    
    def __repr__(self):
        return f"<Permalink(id={self.id}, permalink={self.permalink})>"


class FileMetadata(Base):
    """Enhanced file metadata for file management"""
    __tablename__ = 'file_metadata'
    id = Column(Integer, primary_key=True, index=True)
    attachment_id = Column(Integer, ForeignKey('attachments.id'), nullable=True)
    dm_attachment_id = Column(Integer, ForeignKey('dm_attachments.id'), nullable=True)
    
    # Enhanced metadata
    thumbnail_path = Column(String, nullable=True)
    download_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=False)
    tags = Column(Text, nullable=True)  # JSON array
    
    # File preview/thumbnail
    has_thumbnail = Column(Boolean, default=False)
    
    attachment = relationship('Attachment', foreign_keys=[attachment_id])
    dm_attachment = relationship('DirectMessageAttachment', foreign_keys=[dm_attachment_id])
    
    def __repr__(self):
        return f"<FileMetadata(id={self.id})>"
