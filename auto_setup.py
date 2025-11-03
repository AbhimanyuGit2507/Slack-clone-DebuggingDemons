"""
Auto-setup script - handles everything automatically
Run this with: python auto_setup.py
"""
import os
import sys

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("🚀 Starting automatic setup...")
print(f"📁 Working directory: {script_dir}")
print()

# Step 1: Install dependencies
print("📦 Installing dependencies...")
os.system(f'{sys.executable} -m pip install -q -r requirements.txt')
print("✅ Dependencies installed")
print()

# Step 2: Remove old database if exists
db_path = os.path.join('data', 'slack_rl.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"🗑️  Removed old database")

# Step 3: Import and setup database
print("🔧 Setting up database...")
sys.path.insert(0, os.path.join(script_dir, 'backend'))

from backend.database import engine, Base, SessionLocal
from backend import models
import json
from passlib.context import CryptContext
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

# Seed database
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

try:
    demo_seed_path = os.path.join('data', 'demo_seed.json')
    
    with open(demo_seed_path, 'r', encoding='utf-8') as f:
        seed = json.load(f)
    
    print(f"🌱 Seeding database with demo data...")
    
    # Users
    print(f"👥 Creating {len(seed.get('users', []))} users...")
    for u in seed.get('users', []):
        password = u.get('password', 'password123')
        password_hash = pwd_context.hash(password)
        
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
    db.commit()
    print(f"   ✅ {len(seed.get('users', []))} users created")
    
    # Channels
    print(f"📺 Creating {len(seed.get('channels', []))} channels...")
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
    print(f"   ✅ {len(seed.get('channels', []))} channels created")
    
    # Messages
    print(f"💬 Creating {len(seed.get('messages', []))} messages...")
    for m in seed.get('messages', []):
        try:
            ts = datetime.fromisoformat(m.get('timestamp').replace('Z', '+00:00'))
        except:
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
    print(f"   ✅ {len(seed.get('messages', []))} messages created")
    
    # User Groups
    print(f"👨‍👩‍👧‍👦 Creating {len(seed.get('user_groups', []))} user groups...")
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
    print(f"   ✅ {len(seed.get('user_groups', []))} user groups created")
    
    # Contacts
    for contact in seed.get('contacts', []):
        user_id = contact.get('user_id')
        contact_ids = contact.get('contact_ids', [])
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user and contact_ids:
            contacts = db.query(models.User).filter(models.User.id.in_(contact_ids)).all()
            user.contacts_list = contacts
    db.commit()
    print(f"   ✅ Contacts created")
    
    print()
    print("="*80)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*80)
    print()
    print(f"📊 Summary:")
    print(f"   - {db.query(models.User).count()} Users")
    print(f"   - {db.query(models.Channel).count()} Channels")
    print(f"   - {db.query(models.Message).count()} Messages")
    print(f"   - {db.query(models.UserGroup).count()} User Groups")
    print()
    print("📍 Database: data/slack_rl.db")
    print()
    print("🔑 Test Login:")
    print("   Email: sarah.johnson@company.com")
    print("   Password: password123")
    print()
    print("🚀 Starting server...")
    print("="*80)
    print()
    
finally:
    db.close()

# Step 4: Start server
import uvicorn
from backend.main import app

print("🌐 Server running at: http://localhost:8000")
print("📖 API Docs at: http://localhost:8000/docs")
print()
print("Press CTRL+C to stop the server")
print()

uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
