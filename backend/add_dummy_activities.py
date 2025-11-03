"""Add dummy activity data for testing"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend import models

def add_dummy_activities():
    db = SessionLocal()
    
    try:
        # Check if we already have activities
        existing = db.query(models.Activity).count()
        if existing > 0:
            print(f"Already have {existing} activities in database")
            response = input("Do you want to add more? (y/n): ")
            if response.lower() != 'y':
                return
        
        # Get users for activities
        users = db.query(models.User).all()
        if not users:
            print("No users found! Please seed users first.")
            return
        
        # Get channels for activities
        channels = db.query(models.Channel).all()
        if not channels:
            print("No channels found! Please seed channels first.")
            return
        
        # Activity templates
        activity_templates = [
            {
                "type": "mention",
                "description": "mentioned you in #{channel}",
                "target_type": "message",
            },
            {
                "type": "invitation",
                "description": "invited you to #{channel}",
                "target_type": "channel",
            },
            {
                "type": "reaction",
                "description": "reacted to your message with 👍",
                "target_type": "message",
            },
            {
                "type": "reply",
                "description": "replied to your message in #{channel}",
                "target_type": "message",
            },
            {
                "type": "channel_created",
                "description": "created #{channel}",
                "target_type": "channel",
            },
            {
                "type": "file_shared",
                "description": "shared a file in #{channel}",
                "target_type": "file",
            },
        ]
        
        activities_to_add = []
        
        # Create 15-20 activities
        num_activities = random.randint(15, 20)
        
        for i in range(num_activities):
            # Pick a random user and channel
            user = random.choice(users)
            channel = random.choice(channels)
            template = random.choice(activity_templates)
            
            # Create timestamp going back in time
            hours_ago = random.randint(1, 72)  # 1-72 hours ago
            created_at = datetime.utcnow() - timedelta(hours=hours_ago)
            
            # Replace {channel} in description
            description = template["description"].replace("{channel}", channel.name)
            
            # Add user's name at the beginning for better context
            full_description = f"{user.full_name or user.username} {description}"
            
            activity = models.Activity(
                user_id=user.id,
                activity_type=template["type"],
                description=full_description,
                target_type=template["target_type"],
                target_id=random.randint(1, 100),  # Mock target ID
                activity_metadata='{}',
                created_at=created_at
            )
            activities_to_add.append(activity)
        
        # Add all activities
        db.add_all(activities_to_add)
        db.commit()
        
        print(f"✅ Successfully added {len(activities_to_add)} dummy activities!")
        
        # Show sample of what was added
        print("\nSample activities:")
        for activity in activities_to_add[:5]:
            print(f"  - [{activity.activity_type}] {activity.description}")
        
    except Exception as e:
        print(f"❌ Error adding activities: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_dummy_activities()
