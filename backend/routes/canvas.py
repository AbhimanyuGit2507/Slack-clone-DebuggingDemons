from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, Canvas, Channel
from ..schemas import CanvasCreate, CanvasUpdate, CanvasSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/canvas", tags=["canvas"])


@router.post("/", response_model=CanvasSchema)
def create_canvas(
    canvas_data: CanvasCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new canvas document"""
    # If channel_id provided and positive (not a DM), verify membership
    if canvas_data.channel_id and canvas_data.channel_id > 0:
        channel = db.query(Channel).filter(Channel.id == canvas_data.channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        if current_user not in channel.members:
            raise HTTPException(status_code=403, detail="Not a member of this channel")
    # Negative channel_ids represent DMs, no verification needed
    
    canvas = Canvas(
        title=canvas_data.title,
        content=canvas_data.content,
        channel_id=canvas_data.channel_id,
        owner_id=current_user.id,
        is_public=canvas_data.is_public
    )
    db.add(canvas)
    db.commit()
    db.refresh(canvas)
    
    return canvas


@router.get("/", response_model=List[CanvasSchema])
def list_canvases(
    skip: int = 0,
    limit: int = 50,
    channel_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all accessible canvases"""
    query = db.query(Canvas).filter(
        (Canvas.owner_id == current_user.id) | (Canvas.is_public == True)
    )
    
    if channel_id:
        query = query.filter(Canvas.channel_id == channel_id)
    
    canvases = query.order_by(Canvas.updated_at.desc()).offset(skip).limit(limit).all()
    return canvases


@router.get("/{canvas_id}", response_model=CanvasSchema)
def get_canvas(
    canvas_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific canvas"""
    canvas = db.query(Canvas).filter(Canvas.id == canvas_id).first()
    if not canvas:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    # Check access permissions
    if canvas.owner_id != current_user.id and not canvas.is_public:
        if canvas.channel_id:
            channel = db.query(Channel).filter(Channel.id == canvas.channel_id).first()
            if not channel or current_user not in channel.members:
                raise HTTPException(status_code=403, detail="Access denied")
        else:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return canvas


@router.put("/{canvas_id}", response_model=CanvasSchema)
def update_canvas(
    canvas_id: int,
    canvas_update: CanvasUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a canvas"""
    canvas = db.query(Canvas).filter(Canvas.id == canvas_id).first()
    if not canvas:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    # Only owner can update
    if canvas.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update canvas")
    
    if canvas_update.title is not None:
        canvas.title = canvas_update.title
    if canvas_update.content is not None:
        canvas.content = canvas_update.content
    if canvas_update.channel_id is not None:
        canvas.channel_id = canvas_update.channel_id
    if canvas_update.is_public is not None:
        canvas.is_public = canvas_update.is_public
    
    canvas.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(canvas)
    
    return canvas


@router.delete("/{canvas_id}")
def delete_canvas(
    canvas_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a canvas"""
    canvas = db.query(Canvas).filter(Canvas.id == canvas_id).first()
    if not canvas:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    # Only owner can delete
    if canvas.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete canvas")
    
    db.delete(canvas)
    db.commit()
    
    return {"message": "Canvas deleted successfully"}
