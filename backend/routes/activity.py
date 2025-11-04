from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta
import json

from ..database import get_db
from ..models import User, Activity
from ..schemas import ActivitySchema
from .auth import get_current_user

router = APIRouter(prefix="/api/activity", tags=["activity"])


@router.get("/", response_model=List[ActivitySchema])
def get_activities(
    skip: int = 0,
    limit: int = 50,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent activities for current user"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    activities = db.query(Activity).filter(
        Activity.user_id == current_user.id,
        Activity.created_at >= cutoff
    ).order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()
    
    return activities


@router.get("/all", response_model=List[ActivitySchema])
def get_all_activities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all activities across workspace (for Activity page)"""
    # Get activities from channels user is member of
    activities = db.query(Activity).options(joinedload(Activity.user)).order_by(
        Activity.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    # Format activities for frontend
    formatted_activities = []
    for activity in activities:
        # Parse metadata if exists
        metadata = {}
        if activity.activity_metadata:
            try:
                metadata = json.loads(activity.activity_metadata)
            except:
                pass

        formatted_activities.append({
            'id': activity.id,
            'user_id': activity.user_id,
            'description': activity.description,
            'metadata': json.dumps(metadata),  # Convert metadata to JSON string
            'created_at': activity.created_at.isoformat() if activity.created_at else None,
            'user_name': activity.user.username if activity.user else 'Unknown',
            'user': activity.user.username if activity.user else 'Unknown',
            'action': activity.description,
            'activity_type': activity.activity_type,
            'timestamp': activity.created_at.isoformat() if activity.created_at else None,
            'is_read': True,  # Default to read for now
            'contentType': 'dm' if activity.target_type == 'dm' else 'channel',
            'contentId': activity.target_id if activity.target_id else activity.user_id,
        })

    return formatted_activities


@router.get("/public")
def get_public_activities(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get public activities"""
    activities = db.query(Activity).filter(
        Activity.is_public == True
    ).order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()

    return activities


@router.get("/public", response_model=List[ActivitySchema])
def get_public_activities(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get public activities"""
    activities = db.query(Activity).filter(
        Activity.is_public == True
    ).order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()

    return activities


# Helper function to create activity logs
def create_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    description: str,
    target_type: str = None,
    target_id: int = None,
    metadata: dict = None
):
    """Helper function to create an activity log"""
    activity = Activity(
        user_id=user_id,
        activity_type=activity_type,
        description=description,
        target_type=target_type,
        target_id=target_id,
        metadata=json.dumps(metadata) if metadata else None
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
