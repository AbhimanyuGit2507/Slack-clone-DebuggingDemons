from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[schemas.User])
def list_users(
    search: Optional[str] = Query(None, description="Search by username or email"),
    status_filter: Optional[str] = Query(None, description="Filter by status (online, offline, away)"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all users with optional search and filtering"""
    query = db.query(models.User)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.User.username.ilike(search_term),
                models.User.email.ilike(search_term)
            )
        )
    
    # Apply status filter
    if status_filter:
        query = query.filter(models.User.status == status_filter)
    
    users = query.all()
    return users

@router.get("/{user_id}", response_model=schemas.UserProfile)
def get_user_profile(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/me", response_model=schemas.User)
def update_my_profile(
    update_data: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    # Update username if provided
    if update_data.username is not None:
        # Check if username already exists
        existing = db.query(models.User).filter(
            models.User.username == update_data.username,
            models.User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = update_data.username
    
    # Update email if provided
    if update_data.email is not None:
        # Check if email already exists
        existing = db.query(models.User).filter(
            models.User.email == update_data.email,
            models.User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        current_user.email = update_data.email
    
    # Update status if provided
    if update_data.status is not None:
        current_user.status = update_data.status
    
    # Update profile picture if provided
    if update_data.profile_picture is not None:
        current_user.profile_picture = update_data.profile_picture
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/me/profile", response_model=schemas.UserProfile)
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

# ===== Contacts Management =====

@router.post("/contacts", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_contact(
    contact_data: schemas.ContactAdd,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a user to contacts list"""
    # Verify contact user exists
    contact = db.query(models.User).filter(models.User.id == contact_data.contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Can't add self as contact
    if contact_data.contact_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add yourself as a contact"
        )
    
    # Check if already in contacts
    if contact in current_user.contacts_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already in your contacts"
        )
    
    # Add to contacts
    current_user.contacts_list.append(contact)
    db.commit()
    
    return {"message": "Contact added successfully", "contact_id": contact_data.contact_id}

@router.get("/contacts", response_model=List[schemas.User])
def get_contacts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's contacts list"""
    return current_user.contacts_list

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_contact(
    contact_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a user from contacts list"""
    # Verify contact user exists
    contact = db.query(models.User).filter(models.User.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if in contacts
    if contact not in current_user.contacts_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in your contacts"
        )
    
    # Remove from contacts
    current_user.contacts_list.remove(contact)
    db.commit()
    
    return None

@router.get("/directory", response_model=List[schemas.User])
def get_user_directory(
    search: Optional[str] = Query(None, description="Search by username or email"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user directory (all users except current user)"""
    query = db.query(models.User).filter(models.User.id != current_user.id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.User.username.ilike(search_term),
                models.User.email.ilike(search_term)
            )
        )
    
    users = query.all()
    return users


# ===== NEW ENHANCED PROFILE ENDPOINTS =====

@router.put("/me/profile")
def update_my_profile_enhanced(
    profile_update: schemas.UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update extended profile information"""
    if profile_update.full_name is not None:
        current_user.full_name = profile_update.full_name
    if profile_update.job_title is not None:
        current_user.job_title = profile_update.job_title
    if profile_update.phone is not None:
        current_user.phone = profile_update.phone
    if profile_update.timezone is not None:
        current_user.timezone = profile_update.timezone
    if profile_update.bio is not None:
        current_user.bio = profile_update.bio
    if profile_update.profile_picture is not None:
        current_user.profile_picture = profile_update.profile_picture
    
    db.commit()
    return {"message": "Profile updated successfully"}


@router.put("/me/presence")
def update_presence(
    presence_data: schemas.UserPresenceUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user presence status"""
    if presence_data.presence not in ["online", "away", "dnd", "offline"]:
        raise HTTPException(status_code=400, detail="Invalid presence status")
    
    from datetime import datetime
    current_user.presence = presence_data.presence
    current_user.last_activity_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Presence updated", "presence": presence_data.presence}


@router.put("/me/status")
def update_status_message(
    status_data: schemas.UserStatusUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user status message"""
    current_user.status_text = status_data.status_text
    current_user.status_emoji = status_data.status_emoji
    current_user.status_expires_at = status_data.status_expires_at
    db.commit()
    
    return {"message": "Status updated successfully"}


@router.get("/me/preferences")
def get_my_preferences(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    return {
        "theme": current_user.theme,
        "notification_sound": current_user.notification_sound,
        "email_notifications": current_user.email_notifications
    }


@router.put("/me/preferences")
def update_preferences(
    preferences: schemas.UserPreferencesUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    if preferences.theme is not None:
        if preferences.theme not in ["light", "dark"]:
            raise HTTPException(status_code=400, detail="Invalid theme")
        current_user.theme = preferences.theme
    
    if preferences.notification_sound is not None:
        current_user.notification_sound = preferences.notification_sound
    
    if preferences.email_notifications is not None:
        current_user.email_notifications = preferences.email_notifications
    
    db.commit()
    return {"message": "Preferences updated successfully"}


@router.get("/{user_id}/presence")
def get_user_presence(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's presence status"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "username": user.username,
        "presence": user.presence,
        "status_text": user.status_text,
        "status_emoji": user.status_emoji,
        "status_expires_at": user.status_expires_at,
        "last_activity_at": user.last_activity_at
    }
