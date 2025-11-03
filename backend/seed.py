"""
Database seeding script for Slack Clone
Creates initial database schema and populates with sample data
"""

import sys
from database import engine, SessionLocal
from models import Base, User, Channel, Message, DirectMessage


def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


def seed_data():
    """Seed database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("✓ Database already seeded, skipping...")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample users
        users = [
            User(
                id=1,
                username="john_doe",
                email="john@example.com",
                full_name="John Doe",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqA6jfq"  # password: password123
            ),
            User(
                id=2,
                username="jane_smith",
                email="jane@example.com",
                full_name="Jane Smith",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqA6jfq"
            ),
            User(
                id=3,
                username="bob_wilson",
                email="bob@example.com",
                full_name="Bob Wilson",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqA6jfq"
            ),
        ]
        db.add_all(users)
        
        # Create sample channels
        channels = [
            Channel(
                id=1,
                name="general",
                description="General discussion for the team",
                is_private=False,
                created_by=1
            ),
            Channel(
                id=2,
                name="random",
                description="Random chatter and fun stuff",
                is_private=False,
                created_by=1
            ),
            Channel(
                id=3,
                name="engineering",
                description="Engineering team discussions",
                is_private=False,
                created_by=2
            ),
        ]
        db.add_all(channels)
        
        # Create sample messages
        messages = [
            Message(
                id=1,
                content="Welcome to the team! 👋",
                channel_id=1,
                user_id=1
            ),
            Message(
                id=2,
                content="Thanks! Excited to be here!",
                channel_id=1,
                user_id=2
            ),
            Message(
                id=3,
                content="Let's build something amazing!",
                channel_id=1,
                user_id=3
            ),
        ]
        db.add_all(messages)
        
        db.commit()
        print("✓ Database seeded successfully with sample data!")
        print(f"  - Created {len(users)} users")
        print(f"  - Created {len(channels)} channels")
        print(f"  - Created {len(messages)} messages")
        
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Slack Clone - Database Initialization")
    print("=" * 50)
    
    init_db()
    seed_data()
    
    print("=" * 50)
    print("Database setup complete! 🚀")
    print("=" * 50)
