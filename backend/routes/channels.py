from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api/channels", tags=["channels"])

@router.post("", response_model=schemas.Channel, status_code=status.HTTP_201_CREATED)
def create_channel(
    payload: schemas.ChannelCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new channel"""
    # Check if channel name already exists
    existing = db.query(models.Channel).filter(models.Channel.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Channel name already exists"
        )
    
    # Create channel
    channel = models.Channel(
        name=payload.name,
        description=payload.description,
        is_private=payload.is_private,
        created_by=current_user.id
    )
    
    # Add members (including creator)
    member_ids = set(payload.members or [])
    member_ids.add(current_user.id)
    
    users = db.query(models.User).filter(models.User.id.in_(member_ids)).all()
    channel.members = users
    
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.get("", response_model=List[schemas.Channel])
def list_channels(
    include_private: bool = False,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all channels accessible to current user"""
    if include_private:
        # Show all channels user is a member of (public + private they belong to)
        channels = db.query(models.Channel).join(
            models.channel_members
        ).filter(
            models.channel_members.c.user_id == current_user.id
        ).all()
    else:
        # Show only public channels
        channels = db.query(models.Channel).filter(
            models.Channel.is_private == False
        ).all()
    
    return channels

@router.get("/my-channels", response_model=List[schemas.Channel])
def get_my_channels(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all channels current user is a member of"""
    channels = db.query(models.Channel).join(
        models.channel_members
    ).filter(
        models.channel_members.c.user_id == current_user.id
    ).all()
    
    return channels

@router.get("/{channel_identifier}", response_model=schemas.Channel)
def get_channel(
    channel_identifier: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get channel details by ID or name"""
    # Try to parse as integer ID first
    try:
        channel_id = int(channel_identifier)
        channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    except ValueError:
        # If not an integer, treat as channel name
        channel = db.query(models.Channel).filter(models.Channel.name == channel_identifier).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user has access to private channel
    if channel.is_private:
        is_member = current_user in channel.members
        if not is_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this private channel"
            )
    
    return channel

@router.put("/{channel_id}", response_model=schemas.Channel)
def update_channel(
    channel_id: int,
    update_data: schemas.ChannelUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update channel details (creator only)"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Only creator can update
    if channel.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only channel creator can update channel details"
        )
    
    # Update fields
    if update_data.name is not None:
        # Check if new name already exists
        existing = db.query(models.Channel).filter(
            models.Channel.name == update_data.name,
            models.Channel.id != channel_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel name already exists"
            )
        channel.name = update_data.name
    
    if update_data.description is not None:
        channel.description = update_data.description
    
    if update_data.is_private is not None:
        channel.is_private = update_data.is_private
    
    db.commit()
    db.refresh(channel)
    return channel

@router.post("/{channel_id}/join", response_model=schemas.Channel)
def join_channel(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a channel"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Can't join private channels directly
    if channel.is_private:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot join private channel. You must be invited."
        )
    
    # Check if already a member
    if current_user in channel.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of this channel"
        )
    
    # Add user to channel
    channel.members.append(current_user)
    db.commit()
    db.refresh(channel)
    
    return channel

@router.post("/{channel_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_channel(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Leave a channel"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user is a member
    if current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of this channel"
        )
    
    # Remove user from channel
    channel.members.remove(current_user)
    db.commit()
    
    return None

@router.post("/{channel_id}/invite/{user_id}", response_model=schemas.Channel)
def invite_to_channel(
    channel_id: int,
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invite a user to a channel (members can invite to public, creator can invite to private)"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check permissions
    if channel.is_private and channel.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only channel creator can invite to private channel"
        )
    
    if not channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a member to invite others"
        )
    
    # Get user to invite
    user_to_invite = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already a member
    if user_to_invite in channel.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this channel"
        )
    
    # Add user to channel
    channel.members.append(user_to_invite)
    
    # Create system message for channel
    system_message = models.Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=f"added {user_to_invite.full_name or user_to_invite.username} to #{channel.name}.",
        is_system_message=True
    )
    db.add(system_message)
    
    # Create activity for invited user
    activity = models.Activity(
        user_id=user_to_invite.id,
        activity_type='invitation',
        description=f'{current_user.username} invited you to #{channel.name}',
        target_type='channel',
        target_id=channel_id,
        activity_metadata=f'{{"channel_id": {channel_id}, "invited_by": {current_user.id}}}'
    )
    db.add(activity)
    
    db.commit()
    db.refresh(channel)
    
    return channel

@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a channel (creator only)"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Only creator can delete
    if channel.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only channel creator can delete the channel"
        )
    
    db.delete(channel)
    db.commit()
    
    return None


# ===== NEW CHANNEL TOPIC AND SECTION ENDPOINTS =====

@router.put("/{channel_id}/topic")
def update_channel_topic(
    channel_id: int,
    topic_update: schemas.ChannelTopicUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update channel topic and purpose"""
    from datetime import datetime
    
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if user is member
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    if topic_update.topic is not None:
        channel.topic = topic_update.topic
        channel.topic_set_by = current_user.id
        channel.topic_set_at = datetime.utcnow()
    
    if topic_update.purpose is not None:
        channel.purpose = topic_update.purpose
    
    db.commit()
    return {"message": "Channel topic/purpose updated successfully"}


@router.put("/{channel_id}/section")
def update_channel_section(
    channel_id: int,
    section: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update channel section (for organizing channels in sidebar)"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if user is member
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    channel.section = section
    db.commit()
    
    return {"message": "Channel section updated successfully"}


@router.get("/by-section")
def get_channels_by_section(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all channels grouped by section"""
    # Get all channels user is member of
    user_channels = current_user.channels
    
    # Group by section
    sections = {}
    for channel in user_channels:
        section = channel.section or "Channels"
        if section not in sections:
            sections[section] = []
        sections[section].append({
            "id": channel.id,
            "name": channel.name,
            "description": channel.description,
            "is_private": channel.is_private,
            "topic": channel.topic
        })
    
    return sections

@router.get("/{channel_id}/members", response_model=List[schemas.User])
def get_channel_members(
    channel_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all members of a channel"""
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user has access to this channel
    if channel.is_private and current_user not in channel.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    return channel.members

