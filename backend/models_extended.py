from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notification_type = Column(String, nullable=False)  # mention, reaction, dm, invite, thread_reply
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    
    # Reference to the source
    source_type = Column(String, nullable=True)  # message, channel, user, etc.
    source_id = Column(Integer, nullable=True)
    
    # Metadata
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Related data (JSON)
    data = Column(Text, nullable=True)  # Additional JSON data
    
    user = relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type}, read={self.is_read})>"


class PinnedMessage(Base):
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
        return f"<ScheduledMessage(id={self.id}, scheduled_for={self.scheduled_for}, status={self.status})>"
