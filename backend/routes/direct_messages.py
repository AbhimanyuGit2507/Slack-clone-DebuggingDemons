from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uuid
import bleach

from ..database import get_db
from ..models import DirectMessage, DirectMessageAttachment, User
from ..schemas import (
    DirectMessage as DirectMessageSchema,
    DirectMessageCreate,
    DirectMessageUpdate
)
from .auth import get_current_user

router = APIRouter(prefix="/api/direct-messages", tags=["direct messages"])

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

@router.post("", response_model=DirectMessageSchema, status_code=status.HTTP_201_CREATED)
async def send_direct_message(
    receiver_id: int = Form(...),
    content: str = Form(...),
    formatted_content: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a direct message to another user with optional formatting and file attachments"""
    import json
    
    # Verify receiver exists
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    # Don't allow sending DM to self
    if receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send direct message to yourself"
        )
    
    # Sanitize HTML content if provided
    sanitized_formatted_content = None
    if formatted_content:
        sanitized_formatted_content = sanitize_html(formatted_content)
        print(f"DM Original HTML: {formatted_content}")
        print(f"DM Sanitized HTML: {sanitized_formatted_content}")
    
    # Create direct message
    dm = DirectMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        formatted_content=sanitized_formatted_content
    )
    
    db.add(dm)
    db.flush()  # Get DM ID before processing attachments
    
    # Handle file uploads
    if files:
        upload_dir = Path("uploads/direct_messages")
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
            attachment = DirectMessageAttachment(
                direct_message_id=dm.id,
                filename=file.filename,
                file_path=str(file_path),
                file_type=file.content_type.split('/')[0] if file.content_type else 'file',
                file_size=os.path.getsize(file_path),
                mime_type=file.content_type
            )
            db.add(attachment)
    
    db.commit()
    db.refresh(dm)
    
    return DirectMessageSchema.model_validate(dm)

@router.get("/conversation/{user_id}", response_model=List[DirectMessageSchema])
def get_conversation(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all direct messages between current user and specified user"""
    # Verify other user exists
    other_user = db.query(User).filter(User.id == user_id).first()
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get all messages between the two users
    messages = db.query(DirectMessage).filter(
        or_(
            and_(
                DirectMessage.sender_id == current_user.id,
                DirectMessage.receiver_id == user_id
            ),
            and_(
                DirectMessage.sender_id == user_id,
                DirectMessage.receiver_id == current_user.id
            )
        )
    ).order_by(DirectMessage.timestamp).all()
    
    # Mark received messages as read
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.commit()
    
    return [DirectMessageSchema.model_validate(msg) for msg in messages]

@router.get("/conversations", response_model=List[dict])
def get_all_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of all users current user has DM conversations with"""
    # Get all unique users involved in DMs with current user
    sent_to = db.query(DirectMessage.receiver_id).filter(
        DirectMessage.sender_id == current_user.id
    ).distinct().all()
    
    received_from = db.query(DirectMessage.sender_id).filter(
        DirectMessage.receiver_id == current_user.id
    ).distinct().all()
    
    # Combine and get unique user IDs
    user_ids = set([u[0] for u in sent_to] + [u[0] for u in received_from])
    
    # Get user details and last message for each conversation
    conversations = []
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Get last message in conversation
            last_message = db.query(DirectMessage).filter(
                or_(
                    and_(
                        DirectMessage.sender_id == current_user.id,
                        DirectMessage.receiver_id == user_id
                    ),
                    and_(
                        DirectMessage.sender_id == user_id,
                        DirectMessage.receiver_id == current_user.id
                    )
                )
            ).order_by(DirectMessage.timestamp.desc()).first()
            
            # Count unread messages
            unread_count = db.query(DirectMessage).filter(
                DirectMessage.sender_id == user_id,
                DirectMessage.receiver_id == current_user.id,
                DirectMessage.is_read == False
            ).count()
            
            conversations.append({
                "user_id": user.id,
                "username": user.username,
                "profile_picture": user.profile_picture,
                "status": user.status,
                "last_message": DirectMessageSchema.model_validate(last_message) if last_message else None,
                "unread_count": unread_count
            })
    
    # Sort by last message timestamp
    conversations.sort(
        key=lambda x: x["last_message"].timestamp if x["last_message"] else "",
        reverse=True
    )
    
    return conversations

@router.put("/{message_id}", response_model=DirectMessageSchema)
def update_direct_message(
    message_id: int,
    update_data: DirectMessageUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a direct message (only sender can update)"""
    from datetime import datetime
    import json
    
    dm = db.query(DirectMessage).filter(DirectMessage.id == message_id).first()
    
    if not dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Direct message not found"
        )
    
    # Only sender can update
    if dm.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own messages"
        )
    
    dm.content = update_data.content
    dm.edited_at = datetime.utcnow()
    
    # Update formatting if provided
    if update_data.formatting is not None:
        dm.formatting = update_data.formatting
    
    # Update mentions if provided
    if update_data.mentions is not None:
        dm.mentions = json.dumps(update_data.mentions)
    
    db.commit()
    db.refresh(dm)
    
    return DirectMessageSchema.model_validate(dm)

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_direct_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a direct message (only sender can delete)"""
    dm = db.query(DirectMessage).filter(DirectMessage.id == message_id).first()
    
    if not dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Direct message not found"
        )
    
    # Only sender can delete
    if dm.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own messages"
        )
    
    db.delete(dm)
    db.commit()
    
    return None

@router.patch("/{message_id}/read", response_model=DirectMessageSchema)
def mark_as_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a direct message as read"""
    dm = db.query(DirectMessage).filter(DirectMessage.id == message_id).first()
    
    if not dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Direct message not found"
        )
    
    # Only receiver can mark as read
    if dm.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark messages sent to you as read"
        )
    
    dm.is_read = True
    db.commit()
    db.refresh(dm)
    
    return DirectMessageSchema.model_validate(dm)
