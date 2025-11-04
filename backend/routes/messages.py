from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from .auth import get_current_user
import os
import shutil
from pathlib import Path
import uuid
import bleach

router = APIRouter(prefix="/api/messages", tags=["messages"])

# Allowed HTML tags and attributes for sanitization
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'strike', 
    'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'span'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'code': ['class'],
    'pre': ['class'],
    'span': ['class', 'data-user-id', 'data-username', 'style']
}

def sanitize_html(html: str) -> str:
    """Sanitize HTML content to prevent XSS attacks"""
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

@router.post("", status_code=status.HTTP_201_CREATED)
async def send_message(
    channel_id: int = Form(...),
    user_id: int = Form(...),
    content: str = Form(...),
    formatted_content: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a channel with optional formatting and file attachments"""
    import json
    
    # Verify channel exists
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Verify user is a member of the channel
    if current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a member of the channel to send messages"
        )
    
    # Sanitize HTML content if provided
    sanitized_formatted_content = None
    if formatted_content:
        sanitized_formatted_content = sanitize_html(formatted_content)
        print(f"Original HTML: {formatted_content}")
        print(f"Sanitized HTML: {sanitized_formatted_content}")
    
    # Create message (use current_user.id instead of payload.user_id for security)
    msg = models.Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=content,
        formatted_content=sanitized_formatted_content
    )
    db.add(msg)
    db.flush()  # Get message ID before processing attachments
    
    # Handle file uploads
    if files:
        upload_dir = Path("uploads/messages")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # Generate unique filename
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = upload_dir / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Create attachment record
            attachment = models.Attachment(
                message_id=msg.id,
                filename=file.filename,
                file_path=str(file_path),
                file_type=file.content_type.split('/')[0] if file.content_type else 'file',
                file_size=os.path.getsize(file_path),
                mime_type=file.content_type
            )
            db.add(attachment)
    
    # Extract mentions from formatted content and create activities
    if formatted_content:
        import re
        # Find all mentions in format <span class="mention" data-user-id="123">@username</span>
        mention_pattern = r'data-user-id="(\d+)"'
        mentioned_user_ids = re.findall(mention_pattern, formatted_content)
        
        for user_id_str in mentioned_user_ids:
            mentioned_user_id = int(user_id_str)
            # Don't create activity if user mentions themselves
            if mentioned_user_id != current_user.id:
                # Create activity for mentioned user
                activity = models.Activity(
                    user_id=mentioned_user_id,
                    activity_type='mention',
                    description=f'{current_user.username} mentioned you in #{channel.name}',
                    target_type='message',
                    target_id=msg.id,
                    activity_metadata=f'{{"channel_id": {channel_id}, "message_id": {msg.id}}}'
                )
                db.add(activity)
    
    db.commit()
    db.refresh(msg)
    
    # Return message with user info
    return {
        'id': msg.id,
        'channel_id': msg.channel_id,
        'user_id': msg.user_id,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
        'edited_at': msg.edited_at.isoformat() if msg.edited_at else None,
        'is_deleted': msg.is_deleted,
        'is_system_message': msg.is_system_message,
        'formatted_content': msg.formatted_content,
        'formatting': msg.formatting,
        'mentions': msg.mentions,
        'attachments': [],
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'full_name': current_user.full_name,
            'name': current_user.full_name or current_user.username,
            'profile_picture': current_user.profile_picture
        }
    }

@router.get("/channel/{channel_id}")
def get_messages(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a channel"""
    # Verify channel exists
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Verify user has access to channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    msgs = db.query(models.Message).filter(
        models.Message.channel_id == channel_id
    ).order_by(models.Message.timestamp.asc()).all()
    
    # Add user information to each message
    result = []
    for msg in msgs:
        # Fetch user details
        user = db.query(models.User).filter(models.User.id == msg.user_id).first()
        msg_dict = {
            'id': msg.id,
            'channel_id': msg.channel_id,
            'user_id': msg.user_id,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
            'edited_at': msg.edited_at.isoformat() if msg.edited_at else None,
            'is_deleted': msg.is_deleted,
            'is_system_message': msg.is_system_message,
            'formatted_content': msg.formatted_content,
            'formatting': msg.formatting,
            'mentions': msg.mentions,
            'attachments': [],
            'user': None
        }
        
        if user:
            msg_dict['user'] = {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'name': user.full_name or user.username,
                'profile_picture': user.profile_picture
            }
        result.append(msg_dict)
    
    return result

@router.put("/{message_id}", response_model=schemas.Message)
def update_message(
    message_id: int,
    update_data: schemas.MessageUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a message (author only)"""
    from datetime import datetime
    import json
    
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Only author can update
    if msg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own messages"
        )
    
    msg.content = update_data.content
    msg.edited_at = datetime.utcnow()
    
    # Update formatting if provided
    if update_data.formatting is not None:
        msg.formatting = update_data.formatting
    
    # Update mentions if provided
    if update_data.mentions is not None:
        msg.mentions = json.dumps(update_data.mentions)
    
    db.commit()
    db.refresh(msg)
    
    return msg

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a message (author only)"""
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Only author can delete
    if msg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own messages"
        )
    
    db.delete(msg)
    db.commit()
    
    return None

# ===== Thread Endpoints =====

@router.post("/{message_id}/threads", response_model=schemas.Thread, status_code=status.HTTP_201_CREATED)
def create_thread(
    message_id: int,
    thread_data: schemas.ThreadCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reply to a message (create a thread)"""
    # Verify parent message exists
    parent_msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not parent_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent message not found"
        )
    
    # Verify user has access to the channel
    channel = parent_msg.channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    # Create thread
    thread = models.Thread(
        parent_message_id=message_id,
        user_id=current_user.id,
        content=thread_data.content
    )
    
    db.add(thread)
    db.commit()
    db.refresh(thread)
    
    return thread

@router.get("/{message_id}/threads", response_model=List[schemas.Thread])
def get_threads(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all threads (replies) for a message"""
    # Verify parent message exists
    parent_msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not parent_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent message not found"
        )
    
    # Verify user has access to the channel
    channel = parent_msg.channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    threads = db.query(models.Thread).filter(
        models.Thread.parent_message_id == message_id
    ).order_by(models.Thread.timestamp.asc()).all()
    
    return threads

@router.put("/threads/{thread_id}", response_model=schemas.Thread)
def update_thread(
    thread_id: int,
    update_data: schemas.ThreadUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a thread reply (author only)"""
    thread = db.query(models.Thread).filter(models.Thread.id == thread_id).first()
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    # Only author can update
    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own threads"
        )
    
    thread.content = update_data.content
    db.commit()
    db.refresh(thread)
    
    return thread

@router.delete("/threads/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_thread(
    thread_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a thread reply (author only)"""
    thread = db.query(models.Thread).filter(models.Thread.id == thread_id).first()
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    # Only author can delete
    if thread.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own threads"
        )
    
    db.delete(thread)
    db.commit()
    
    return None

# ===== Reaction Endpoints =====

@router.post("/{message_id}/reactions", response_model=schemas.Reaction, status_code=status.HTTP_201_CREATED)
def add_reaction(
    message_id: int,
    reaction_data: schemas.ReactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a reaction to a message"""
    # Verify message exists
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Verify user has access to the channel
    channel = msg.channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    # Check if user already reacted with this emoji
    existing = db.query(models.Reaction).filter(
        models.Reaction.message_id == message_id,
        models.Reaction.user_id == current_user.id,
        models.Reaction.emoji == reaction_data.emoji
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already reacted with this emoji"
        )
    
    # Create reaction
    reaction = models.Reaction(
        message_id=message_id,
        user_id=current_user.id,
        emoji=reaction_data.emoji
    )
    
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    
    return reaction

@router.get("/{message_id}/reactions", response_model=List[schemas.Reaction])
def get_reactions(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reactions for a message or direct message"""
    # Check if the message is a channel message
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        # Verify user has access to the channel
        channel = msg.channel
        if channel.is_private and current_user not in channel.members:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this channel"
            )
        reactions = db.query(models.Reaction).filter(
            models.Reaction.message_id == message_id
        ).order_by(models.Reaction.timestamp.asc()).all()
        return reactions

    # Check if the message is a direct message
    dm = db.query(models.DirectMessage).filter(models.DirectMessage.id == message_id).first()
    if dm:
        # Verify user is either the sender or receiver
        if current_user.id not in [dm.sender_id, dm.receiver_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this direct message"
            )
        reactions = db.query(models.Reaction).filter(
            models.Reaction.message_id == message_id
        ).order_by(models.Reaction.timestamp.asc()).all()
        return reactions

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Message not found"
    )

@router.delete("/reactions/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_reaction(
    reaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a reaction (user who reacted only)"""
    reaction = db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()
    
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reaction not found"
        )
    
    # Only user who reacted can remove
    if reaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only remove your own reactions"
        )
    
    db.delete(reaction)
    db.commit()
    
    return None
