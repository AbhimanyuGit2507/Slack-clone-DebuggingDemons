from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from ..database import get_db
from ..models import User, CustomEmoji
from ..schemas import CustomEmojiSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/emojis", tags=["custom-emojis"])

EMOJI_DIR = "uploads/emojis"
os.makedirs(EMOJI_DIR, exist_ok=True)


@router.post("/", response_model=CustomEmojiSchema)
async def upload_custom_emoji(
    name: str,
    image: UploadFile = File(...),
    aliases: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a custom emoji"""
    # Check if name already exists
    existing = db.query(CustomEmoji).filter(CustomEmoji.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Emoji name already exists")
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_extension = image.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(EMOJI_DIR, unique_filename)
    
    # Save file
    with open(file_path, 'wb') as f:
        content = await image.read()
        f.write(content)
    
    # Create emoji record
    emoji = CustomEmoji(
        name=name,
        image_path=file_path,
        aliases=aliases,
        uploaded_by=current_user.id
    )
    db.add(emoji)
    db.commit()
    db.refresh(emoji)
    
    return emoji


@router.get("/", response_model=List[CustomEmojiSchema])
def list_custom_emojis(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all custom emojis"""
    emojis = db.query(CustomEmoji).offset(skip).limit(limit).all()
    return emojis


@router.get("/popular", response_model=List[CustomEmojiSchema])
def get_popular_emojis(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most popular custom emojis"""
    emojis = db.query(CustomEmoji).order_by(
        CustomEmoji.usage_count.desc()
    ).limit(limit).all()
    return emojis


@router.delete("/{emoji_id}")
def delete_custom_emoji(
    emoji_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a custom emoji"""
    emoji = db.query(CustomEmoji).filter(CustomEmoji.id == emoji_id).first()
    if not emoji:
        raise HTTPException(status_code=404, detail="Emoji not found")
    
    # Only uploader can delete
    if emoji.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only uploader can delete emoji")
    
    # Delete file
    if os.path.exists(emoji.image_path):
        os.remove(emoji.image_path)
    
    db.delete(emoji)
    db.commit()
    
    return {"message": "Emoji deleted successfully"}


@router.post("/{emoji_id}/use")
def increment_emoji_usage(
    emoji_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Increment emoji usage count"""
    emoji = db.query(CustomEmoji).filter(CustomEmoji.id == emoji_id).first()
    if not emoji:
        raise HTTPException(status_code=404, detail="Emoji not found")
    
    emoji.usage_count += 1
    db.commit()
    
    return {"message": "Usage count updated"}
