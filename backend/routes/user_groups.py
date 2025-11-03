from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid
import os

from ..database import get_db
from ..models import User, UserGroup, user_group_members
from ..schemas import UserGroupCreate, UserGroupUpdate, UserGroupSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/groups", tags=["user-groups"])


@router.post("/", response_model=UserGroupSchema)
def create_user_group(
    group_data: UserGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new user group"""
    # Check if handle already exists
    existing = db.query(UserGroup).filter(UserGroup.handle == group_data.handle).first()
    if existing:
        raise HTTPException(status_code=400, detail="Handle already exists")
    
    # Create group
    group = UserGroup(
        name=group_data.name,
        handle=group_data.handle,
        description=group_data.description,
        created_by=current_user.id
    )
    db.add(group)
    db.flush()
    
    # Add members
    if group_data.member_ids:
        for member_id in group_data.member_ids:
            user = db.query(User).filter(User.id == member_id).first()
            if user:
                db.execute(
                    user_group_members.insert().values(
                        group_id=group.id,
                        user_id=member_id
                    )
                )
    
    db.commit()
    db.refresh(group)
    return group


@router.get("/", response_model=List[UserGroupSchema])
def list_user_groups(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all user groups"""
    groups = db.query(UserGroup).offset(skip).limit(limit).all()
    return groups


@router.get("/{group_id}", response_model=UserGroupSchema)
def get_user_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=UserGroupSchema)
def update_user_group(
    group_id: int,
    group_update: UserGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Only creator can update
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only group creator can update")
    
    if group_update.name is not None:
        group.name = group_update.name
    if group_update.description is not None:
        group.description = group_update.description
    
    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}")
def delete_user_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Only creator can delete
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only group creator can delete")
    
    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}


@router.post("/{group_id}/members/{user_id}")
def add_group_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a member to a user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Only creator can add members
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only group creator can add members")
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already member
    existing = db.execute(
        user_group_members.select().where(
            user_group_members.c.group_id == group_id,
            user_group_members.c.user_id == user_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already in group")
    
    # Add member
    db.execute(
        user_group_members.insert().values(
            group_id=group_id,
            user_id=user_id
        )
    )
    db.commit()
    
    return {"message": "Member added successfully"}


@router.delete("/{group_id}/members/{user_id}")
def remove_group_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a member from a user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Only creator can remove members
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only group creator can remove members")
    
    # Remove member
    db.execute(
        user_group_members.delete().where(
            user_group_members.c.group_id == group_id,
            user_group_members.c.user_id == user_id
        )
    )
    db.commit()
    
    return {"message": "Member removed successfully"}


@router.get("/{group_id}/members")
def get_group_members(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all members of a user group"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get member IDs
    members_data = db.execute(
        user_group_members.select().where(
            user_group_members.c.group_id == group_id
        )
    ).fetchall()
    
    member_ids = [m.user_id for m in members_data]
    
    # Get user details
    users = db.query(User).filter(User.id.in_(member_ids)).all()
    
    return {
        "group_id": group_id,
        "group_name": group.name,
        "members": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "profile_picture": u.profile_picture
            }
            for u in users
        ]
    }
