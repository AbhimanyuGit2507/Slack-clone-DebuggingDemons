from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from pathlib import Path

from ..database import get_db
from ..models import User, Message, DirectMessage, Attachment, DirectMessageAttachment
from ..schemas import AttachmentSchema, DMAttachmentSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/attachments", tags=["attachments"])

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md', '.csv', '.xlsx', '.xls'],
    'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

def get_file_type(filename: str) -> str:
    """Determine file type based on extension"""
    ext = Path(filename).suffix.lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    
    return 'other'

def save_upload_file(upload_file: UploadFile) -> tuple:
    """Save uploaded file and return path and file info"""
    # Generate unique filename
    file_ext = Path(upload_file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        content = upload_file.file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        f.write(content)
    
    file_type = get_file_type(upload_file.filename)
    file_size = len(content)
    
    return str(file_path), file_type, file_size

@router.get("/", response_model=List[AttachmentSchema])
def list_all_attachments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments accessible to the current user"""
    # Get all attachments from regular messages
    attachments = db.query(Attachment).order_by(
        Attachment.uploaded_at.desc()
    ).offset(skip).limit(limit).all()
    
    return attachments

@router.post("/message/{message_id}", response_model=AttachmentSchema, status_code=status.HTTP_201_CREATED)
async def upload_message_attachment(
    message_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an attachment to a channel message"""
    # Verify message exists and user has access
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Verify user is member of channel
    channel = message.channel
    if current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    # Save file
    try:
        file_path, file_type, file_size = save_upload_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
    
    # Create attachment record
    attachment = Attachment(
        message_id=message_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        mime_type=file.content_type
    )
    
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return AttachmentSchema.model_validate(attachment)

@router.post("/direct-message/{dm_id}", response_model=DMAttachmentSchema, status_code=status.HTTP_201_CREATED)
async def upload_dm_attachment(
    dm_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an attachment to a direct message"""
    # Verify DM exists and user has access
    dm = db.query(DirectMessage).filter(DirectMessage.id == dm_id).first()
    if not dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Direct message not found"
        )
    
    # Verify user is sender or receiver
    if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this conversation"
        )
    
    # Save file
    try:
        file_path, file_type, file_size = save_upload_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
    
    # Create attachment record
    attachment = DirectMessageAttachment(
        direct_message_id=dm_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        mime_type=file.content_type
    )
    
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return DMAttachmentSchema.model_validate(attachment)

@router.get("/message/{message_id}", response_model=List[AttachmentSchema])
def get_message_attachments(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for a message"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Verify access
    channel = message.channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    return [AttachmentSchema.model_validate(att) for att in message.attachments]

@router.get("/direct-message/{dm_id}", response_model=List[DMAttachmentSchema])
def get_dm_attachments(
    dm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all attachments for a direct message"""
    dm = db.query(DirectMessage).filter(DirectMessage.id == dm_id).first()
    if not dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Direct message not found"
        )
    
    # Verify access
    if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this conversation"
        )
    
    return [DMAttachmentSchema.model_validate(att) for att in dm.dm_attachments]

@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attachment(
    attachment_id: int,
    attachment_type: str = "message",  # message or dm
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an attachment"""
    if attachment_type == "message":
        attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found"
            )
        
        # Only message author can delete
        if attachment.message.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own attachments"
            )
    else:
        attachment = db.query(DirectMessageAttachment).filter(
            DirectMessageAttachment.id == attachment_id
        ).first()
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found"
            )
        
        # Only sender can delete
        if attachment.direct_message.sender_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own attachments"
            )
    
    # Delete file from filesystem
    try:
        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)
    except Exception:
        pass  # Continue even if file deletion fails
    
    # Delete database record
    db.delete(attachment)
    db.commit()
    
    return None

@router.get("/download/{attachment_id}")
async def download_attachment(
    attachment_id: int,
    attachment_type: str = "message",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download an attachment"""
    from fastapi.responses import FileResponse
    
    if attachment_type == "message":
        attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found"
            )
        
        # Verify access
        channel = attachment.message.channel
        if channel.is_private and current_user not in channel.members:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this file"
            )
    else:
        attachment = db.query(DirectMessageAttachment).filter(
            DirectMessageAttachment.id == attachment_id
        ).first()
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found"
            )
        
        # Verify access
        dm = attachment.direct_message
        if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this file"
            )
    
    if not os.path.exists(attachment.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return FileResponse(
        path=attachment.file_path,
        filename=attachment.filename,
        media_type=attachment.mime_type
    )
