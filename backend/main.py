import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .config import settings
from .routes import (
    messages, channels, users, auth, direct_messages, search, attachments,
    notifications, pins, bookmarks, activity, drafts, scheduled_messages,
    user_groups, custom_emojis, canvas, workflows, permalinks, calls
)
from . import models

app = FastAPI(title=settings.APP_NAME)

# CORS for Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(channels.router)
app.include_router(messages.router)
app.include_router(direct_messages.router)
app.include_router(search.router)
app.include_router(attachments.router)

# New feature routers
app.include_router(notifications.router)
app.include_router(pins.router)
app.include_router(bookmarks.router)
app.include_router(activity.router)
app.include_router(drafts.router)
app.include_router(scheduled_messages.router)
app.include_router(user_groups.router)
app.include_router(custom_emojis.router)
app.include_router(canvas.router)
app.include_router(workflows.router)
app.include_router(permalinks.router)
app.include_router(calls.router)

@app.on_event("startup")
def startup():
    # ensure data dir exists
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # create tables
    Base.metadata.create_all(bind=engine)

    # seed DB if empty using data/seed.json
    from sqlalchemy.orm import Session
    from .database import SessionLocal

    db: Session = SessionLocal()
    try:
        user_count = db.query(models.User).count()
        if user_count == 0:
            # Try demo_seed.json first, fallback to seed.json
            demo_seed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'demo_seed.json')
            seed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed.json')
            
            file_to_use = demo_seed_path if os.path.exists(demo_seed_path) else seed_path
            
            if os.path.exists(file_to_use):
                with open(file_to_use, 'r', encoding='utf-8') as f:
                    seed = json.load(f)
                
                # users with enhanced fields
                users_map = {}
                for u in seed.get('users', []):
                    # Store password as plain text (simplified)
                    password = u.get('password', 'password123')
                    password_hash = password
                    
                    user = models.User(
                        id=u.get('id'),
                        username=u.get('username'),
                        email=u.get('email'),
                        password_hash=password_hash,
                        name=u.get('name'),
                        full_name=u.get('full_name'),
                        profile_picture=u.get('profile_picture'),
                        status=u.get('status', 'offline'),
                        presence=u.get('presence', 'offline'),
                        status_text=u.get('status_text'),
                        status_emoji=u.get('status_emoji'),
                        job_title=u.get('job_title'),
                        phone=u.get('phone'),
                        timezone=u.get('timezone'),
                        bio=u.get('bio')
                    )
                    db.add(user)
                    users_map[user.id] = user
                db.commit()
                
                # channels with enhanced fields
                for c in seed.get('channels', []):
                    chan = models.Channel(
                        id=c.get('id'),
                        name=c.get('name'),
                        description=c.get('description'),
                        is_private=c.get('is_private', False),
                        created_by=c.get('created_by'),
                        topic=c.get('topic'),
                        purpose=c.get('purpose'),
                        section=c.get('section')
                    )
                    member_ids = c.get('members', [])
                    if member_ids:
                        members = db.query(models.User).filter(models.User.id.in_(member_ids)).all()
                        chan.members = members
                    db.add(chan)
                db.commit()
                
                # messages
                from datetime import datetime
                for m in seed.get('messages', []):
                    ts = None
                    try:
                        ts = datetime.fromisoformat(m.get('timestamp').replace('Z', '+00:00'))
                    except Exception:
                        ts = datetime.utcnow()
                    msg = models.Message(
                        id=m.get('id'),
                        channel_id=m.get('channel_id'),
                        user_id=m.get('user_id'),
                        content=m.get('content'),
                        timestamp=ts
                    )
                    db.add(msg)
                db.commit()
                
                # user_groups
                for ug in seed.get('user_groups', []):
                    user_group = models.UserGroup(
                        id=ug.get('id'),
                        name=ug.get('name'),
                        handle=ug.get('handle'),
                        description=ug.get('description'),
                        created_by=ug.get('created_by')
                    )
                    member_ids = ug.get('members', [])
                    if member_ids:
                        members = db.query(models.User).filter(models.User.id.in_(member_ids)).all()
                        user_group.members = members
                    db.add(user_group)
                db.commit()
                
                # direct messages
                for dm in seed.get('direct_messages', []):
                    ts = None
                    try:
                        ts = datetime.fromisoformat(dm.get('timestamp').replace('Z', '+00:00'))
                    except Exception:
                        ts = datetime.utcnow()
                    direct_msg = models.DirectMessage(
                        id=dm.get('id'),
                        sender_id=dm.get('sender_id'),
                        receiver_id=dm.get('receiver_id'),
                        content=dm.get('content'),
                        timestamp=ts
                    )
                    db.add(direct_msg)
                db.commit()
                
                # contacts
                for contact in seed.get('contacts', []):
                    user_id = contact.get('user_id')
                    contact_ids = contact.get('contact_ids', [])
                    user = db.query(models.User).filter(models.User.id == user_id).first()
                    if user and contact_ids:
                        contacts = db.query(models.User).filter(models.User.id.in_(contact_ids)).all()
                        user.contacts_list = contacts
                db.commit()
                
                print(f"✅ Database seeded successfully from {os.path.basename(file_to_use)}")
                print(f"   - {len(seed.get('users', []))} users")
                print(f"   - {len(seed.get('channels', []))} channels")
                print(f"   - {len(seed.get('user_groups', []))} user groups")
                print(f"   - {len(seed.get('messages', []))} messages")
                print(f"   - {len(seed.get('direct_messages', []))} direct messages")
    finally:
        db.close()
