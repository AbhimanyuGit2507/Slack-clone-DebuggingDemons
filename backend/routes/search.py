from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional

from ..database import get_db
from ..models import User, Channel, Message, DirectMessage
from ..schemas import SearchResponse, SearchResult
from .auth import get_current_user

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    search_type: str = Query("all", description="Type: all, messages, channels, users"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Universal search across messages, channels, and users
    """
    results = []
    
    # Search Users
    if search_type in ["all", "users"]:
        search_term = f"%{q}%"
        users = db.query(User).filter(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
                User.name.ilike(search_term) if User.name else False
            )
        ).limit(limit).all()
        
        for user in users:
            results.append(SearchResult(
                result_type="user",
                id=user.id,
                content={
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": user.profile_picture,
                    "status": user.status
                }
            ))
    
    # Search Channels
    if search_type in ["all", "channels"]:
        search_term = f"%{q}%"
        channels_query = db.query(Channel).filter(
            or_(
                Channel.name.ilike(search_term),
                Channel.description.ilike(search_term)
            )
        )
        
        # Filter out private channels user doesn't have access to
        channels = []
        for channel in channels_query.limit(limit).all():
            if not channel.is_private or current_user in channel.members:
                channels.append(channel)
        
        for channel in channels:
            results.append(SearchResult(
                result_type="channel",
                id=channel.id,
                content={
                    "name": channel.name,
                    "description": channel.description,
                    "is_private": channel.is_private,
                    "member_count": len(channel.members)
                }
            ))
    
    # Search Messages in Channels
    if search_type in ["all", "messages"]:
        search_term = f"%{q}%"
        
        # Get channels user is a member of
        user_channel_ids = [c.id for c in current_user.channels]
        
        messages = db.query(Message).filter(
            and_(
                Message.content.ilike(search_term),
                Message.channel_id.in_(user_channel_ids),
                Message.is_deleted == False
            )
        ).order_by(Message.timestamp.desc()).limit(limit).all()
        
        for msg in messages:
            results.append(SearchResult(
                result_type="message",
                id=msg.id,
                content={
                    "content": msg.content,
                    "channel_id": msg.channel_id,
                    "channel_name": msg.channel.name,
                    "user_id": msg.user_id,
                    "username": msg.user.username,
                    "timestamp": msg.timestamp.isoformat()
                }
            ))
        
        # Search Direct Messages
        direct_messages = db.query(DirectMessage).filter(
            and_(
                DirectMessage.content.ilike(search_term),
                or_(
                    DirectMessage.sender_id == current_user.id,
                    DirectMessage.receiver_id == current_user.id
                ),
                DirectMessage.is_deleted == False
            )
        ).order_by(DirectMessage.timestamp.desc()).limit(limit).all()
        
        for dm in direct_messages:
            other_user = dm.sender if dm.sender_id != current_user.id else dm.receiver
            results.append(SearchResult(
                result_type="direct_message",
                id=dm.id,
                content={
                    "content": dm.content,
                    "other_user_id": other_user.id,
                    "other_username": other_user.username,
                    "timestamp": dm.timestamp.isoformat(),
                    "is_sent_by_me": dm.sender_id == current_user.id
                }
            ))
    
    return SearchResponse(
        query=q,
        results=results[:limit],
        total_count=len(results)
    )

@router.get("/messages", response_model=List[dict])
def search_messages(
    q: str = Query(..., min_length=1),
    channel_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search messages in channels user has access to"""
    search_term = f"%{q}%"
    
    query = db.query(Message).filter(
        and_(
            Message.content.ilike(search_term),
            Message.is_deleted == False
        )
    )
    
    # Filter by channel if specified
    if channel_id:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if channel and (not channel.is_private or current_user in channel.members):
            query = query.filter(Message.channel_id == channel_id)
        else:
            return []
    else:
        # Only search in channels user is member of
        user_channel_ids = [c.id for c in current_user.channels]
        query = query.filter(Message.channel_id.in_(user_channel_ids))
    
    messages = query.order_by(Message.timestamp.desc()).limit(limit).all()
    
    return [{
        "id": msg.id,
        "content": msg.content,
        "channel_id": msg.channel_id,
        "channel_name": msg.channel.name,
        "user_id": msg.user_id,
        "username": msg.user.username,
        "timestamp": msg.timestamp.isoformat()
    } for msg in messages]

@router.get("/users", response_model=List[dict])
def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search for users"""
    search_term = f"%{q}%"
    
    users = db.query(User).filter(
        or_(
            User.username.ilike(search_term),
            User.email.ilike(search_term),
            User.name.ilike(search_term) if User.name else False
        )
    ).limit(limit).all()
    
    return [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_picture": user.profile_picture,
        "status": user.status
    } for user in users]

@router.get("/channels", response_model=List[dict])
def search_channels(
    q: str = Query(..., min_length=1),
    include_private: bool = Query(False),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search for channels"""
    search_term = f"%{q}%"
    
    query = db.query(Channel).filter(
        or_(
            Channel.name.ilike(search_term),
            Channel.description.ilike(search_term)
        )
    )
    
    channels = query.limit(limit * 2).all()  # Get more to filter
    
    results = []
    for channel in channels:
        # Include public channels or private channels user is member of
        if not channel.is_private or (include_private and current_user in channel.members):
            results.append({
                "id": channel.id,
                "name": channel.name,
                "description": channel.description,
                "is_private": channel.is_private,
                "member_count": len(channel.members),
                "is_member": current_user in channel.members
            })
            
            if len(results) >= limit:
                break
    
    return results

@router.get("/direct-messages", response_model=List[dict])
def search_direct_messages(
    q: str = Query(..., min_length=1),
    user_id: Optional[int] = Query(None, description="Search DMs with specific user"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search direct messages"""
    search_term = f"%{q}%"
    
    query = db.query(DirectMessage).filter(
        and_(
            DirectMessage.content.ilike(search_term),
            or_(
                DirectMessage.sender_id == current_user.id,
                DirectMessage.receiver_id == current_user.id
            ),
            DirectMessage.is_deleted == False
        )
    )
    
    # Filter by specific conversation
    if user_id:
        query = query.filter(
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
        )
    
    messages = query.order_by(DirectMessage.timestamp.desc()).limit(limit).all()
    
    return [{
        "id": dm.id,
        "content": dm.content,
        "sender_id": dm.sender_id,
        "receiver_id": dm.receiver_id,
        "other_user": {
            "id": dm.sender.id if dm.sender_id != current_user.id else dm.receiver.id,
            "username": dm.sender.username if dm.sender_id != current_user.id else dm.receiver.username,
        },
        "timestamp": dm.timestamp.isoformat(),
        "is_sent_by_me": dm.sender_id == current_user.id
    } for dm in messages]
