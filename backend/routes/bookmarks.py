from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, Bookmark, Message, DirectMessage
from ..schemas import BookmarkCreate, BookmarkSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])


@router.post("/", response_model=BookmarkSchema)
def create_bookmark(
    bookmark_data: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a bookmark for a message or DM"""
    # Validate that either message_id or direct_message_id is provided
    if not bookmark_data.message_id and not bookmark_data.direct_message_id:
        raise HTTPException(status_code=400, detail="Must provide either message_id or direct_message_id")
    
    if bookmark_data.message_id and bookmark_data.direct_message_id:
        raise HTTPException(status_code=400, detail="Cannot bookmark both message and DM at once")
    
    # Check if message exists (if provided)
    if bookmark_data.message_id:
        message = db.query(Message).filter(Message.id == bookmark_data.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Check if user has access to the channel
        if current_user not in message.channel.members:
            raise HTTPException(status_code=403, detail="No access to this message")
    
    # Check if DM exists (if provided)
    if bookmark_data.direct_message_id:
        dm = db.query(DirectMessage).filter(
            DirectMessage.id == bookmark_data.direct_message_id
        ).first()
        if not dm:
            raise HTTPException(status_code=404, detail="Direct message not found")
        
        # Check if user is part of the conversation
        if dm.sender_id != current_user.id and dm.receiver_id != current_user.id:
            raise HTTPException(status_code=403, detail="No access to this message")
    
    # Check if already bookmarked
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.message_id == bookmark_data.message_id,
        Bookmark.direct_message_id == bookmark_data.direct_message_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    
    # Create bookmark
    bookmark = Bookmark(
        user_id=current_user.id,
        message_id=bookmark_data.message_id,
        direct_message_id=bookmark_data.direct_message_id,
        note=bookmark_data.note
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    
    return bookmark


@router.get("/", response_model=List[BookmarkSchema])
def get_bookmarks(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all bookmarks for current user"""
    bookmarks = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id
    ).order_by(Bookmark.created_at.desc()).offset(skip).limit(limit).all()
    
    return bookmarks


@router.delete("/{bookmark_id}")
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a bookmark"""
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark deleted successfully"}


@router.put("/{bookmark_id}/note")
def update_bookmark_note(
    bookmark_id: int,
    note: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update bookmark note"""
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    bookmark.note = note
    db.commit()
    
    return {"message": "Note updated successfully"}
