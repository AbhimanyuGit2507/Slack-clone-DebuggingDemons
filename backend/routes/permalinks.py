from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..database import get_db
from ..models import User, Permalink, Message, DirectMessage
from ..schemas import PermalinkCreate, PermalinkSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/permalinks", tags=["permalinks"])


@router.post("/", response_model=PermalinkSchema)
def create_permalink(
    permalink_data: PermalinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a permalink for a message"""
    # Validate that either message_id or direct_message_id is provided
    if not permalink_data.message_id and not permalink_data.direct_message_id:
        raise HTTPException(status_code=400, detail="Must provide either message_id or direct_message_id")
    
    if permalink_data.message_id and permalink_data.direct_message_id:
        raise HTTPException(status_code=400, detail="Cannot create permalink for both message and DM")
    
    # Check if message exists
    if permalink_data.message_id:
        message = db.query(Message).filter(Message.id == permalink_data.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Check if permalink already exists
        existing = db.query(Permalink).filter(Permalink.message_id == permalink_data.message_id).first()
        if existing:
            return existing
    
    # Check if DM exists
    if permalink_data.direct_message_id:
        dm = db.query(DirectMessage).filter(DirectMessage.id == permalink_data.direct_message_id).first()
        if not dm:
            raise HTTPException(status_code=404, detail="Direct message not found")
        
        # Verify user is part of conversation
        if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if permalink already exists
        existing = db.query(Permalink).filter(Permalink.direct_message_id == permalink_data.direct_message_id).first()
        if existing:
            return existing
    
    # Generate unique permalink
    permalink_str = str(uuid.uuid4())[:8]
    
    # Create permalink
    permalink = Permalink(
        message_id=permalink_data.message_id,
        direct_message_id=permalink_data.direct_message_id,
        permalink=permalink_str
    )
    db.add(permalink)
    db.commit()
    db.refresh(permalink)
    
    return permalink


@router.get("/{permalink_str}")
def get_by_permalink(
    permalink_str: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get message by permalink"""
    permalink = db.query(Permalink).filter(Permalink.permalink == permalink_str).first()
    if not permalink:
        raise HTTPException(status_code=404, detail="Permalink not found")
    
    if permalink.message_id:
        message = db.query(Message).filter(Message.id == permalink.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Check if user has access to channel
        if current_user not in message.channel.members:
            raise HTTPException(status_code=403, detail="No access to this channel")
        
        return {
            "type": "message",
            "id": message.id,
            "channel_id": message.channel_id,
            "channel_name": message.channel.name,
            "user_id": message.user_id,
            "content": message.content,
            "timestamp": message.timestamp,
            "permalink": permalink_str
        }
    
    if permalink.direct_message_id:
        dm = db.query(DirectMessage).filter(DirectMessage.id == permalink.direct_message_id).first()
        if not dm:
            raise HTTPException(status_code=404, detail="Direct message not found")
        
        # Check if user is part of conversation
        if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
            raise HTTPException(status_code=403, detail="No access to this message")
        
        return {
            "type": "direct_message",
            "id": dm.id,
            "sender_id": dm.sender_id,
            "receiver_id": dm.receiver_id,
            "content": dm.content,
            "timestamp": dm.timestamp,
            "permalink": permalink_str
        }
    
    raise HTTPException(status_code=404, detail="Message not found")
