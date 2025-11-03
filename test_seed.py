"""Test script to verify database seeding with demo data"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Remove existing database
db_path = os.path.join(os.path.dirname(__file__), 'data', 'slack_rl.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Removed old database: {db_path}")
else:
    print(f"ℹ️  No existing database found at: {db_path}")

# Import and run startup
from backend.database import engine, Base, SessionLocal
from backend import models
import json

print("\n🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

# Seed database
print("\n📦 Seeding database with demo data...")
db = SessionLocal()
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    demo_seed_path = os.path.join(os.path.dirname(__file__), 'data', 'demo_seed.json')
    
    if os.path.exists(demo_seed_path):
        with open(demo_seed_path, 'r', encoding='utf-8') as f:
            seed = json.load(f)
        
        # Users
        print(f"\n👥 Creating {len(seed.get('users', []))} users...")
        users_map = {}
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
            users_map[user.id] = user
            print(f"   ✓ {user.full_name} ({user.email}) - {user.job_title}")
        db.commit()
        print(f"✅ {len(users_map)} users created")
        
        # Channels
        print(f"\n📺 Creating {len(seed.get('channels', []))} channels...")
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
            privacy = "🔒 Private" if chan.is_private else "🌐 Public"
            print(f"   ✓ #{chan.name} ({privacy}) - {len(member_ids)} members - Section: {chan.section}")
        db.commit()
        print(f"✅ {len(seed.get('channels', []))} channels created")
        
        # Messages
        from datetime import datetime
        print(f"\n💬 Creating {len(seed.get('messages', []))} messages...")
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
        print(f"✅ {len(seed.get('messages', []))} messages created")
        
        # User Groups
        print(f"\n👨‍👩‍👧‍👦 Creating {len(seed.get('user_groups', []))} user groups...")
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
            print(f"   ✓ {user_group.handle} - {user_group.name} ({len(member_ids)} members)")
        db.commit()
        print(f"✅ {len(seed.get('user_groups', []))} user groups created")
        
        # Contacts
        contacts_data = seed.get('contacts', [])
        if contacts_data:
            print(f"\n📞 Creating contacts...")
            for contact in contacts_data:
                user_id = contact.get('user_id')
                contact_ids = contact.get('contact_ids', [])
                user = db.query(models.User).filter(models.User.id == user_id).first()
                if user and contact_ids:
                    contacts = db.query(models.User).filter(models.User.id.in_(contact_ids)).all()
                    user.contacts_list = contacts
            db.commit()
            print(f"✅ Contacts created")
        
        # Verify data
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        user_count = db.query(models.User).count()
        channel_count = db.query(models.Channel).count()
        message_count = db.query(models.Message).count()
        group_count = db.query(models.UserGroup).count()
        
        print(f"👥 Total Users: {user_count}")
        print(f"📺 Total Channels: {channel_count}")
        print(f"💬 Total Messages: {message_count}")
        print(f"👨‍👩‍👧‍👦 Total User Groups: {group_count}")
        
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📝 Sample Login Credentials:")
        print("   Email: sarah.johnson@company.com")
        print("   Password: password123")
        print("\n🚀 You can now start the backend server with:")
        print("   python -m uvicorn backend.main:app --reload --port 8000")
        print("\n📖 API Documentation will be available at:")
        print("   http://localhost:8000/docs")
        
    else:
        print(f"❌ Demo seed file not found: {demo_seed_path}")
        
finally:
    db.close()
