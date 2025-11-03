"""
Seed activities data for the Activity page
This script adds various types of activities to demonstrate all activity types
"""

import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Activity, User, Channel, Base

# Activity types with descriptions
ACTIVITY_TYPES = {
    'workspace_invitation': 'Accepted your invitation to join Slack',
    'mention': 'mentioned you in',
    'reaction': 'reacted to your message with',
    'thread_reply': 'replied to a thread you\'re following',
    'saved_item': 'You saved a message from',
    'message_sent': 'sent a message in',
    'file_uploaded': 'uploaded a file to',
    'channel_joined': 'joined',
    'channel_created': 'created',
    'dm_sent': 'sent you a direct message',
}

def seed_activities():
    """Seed activity data"""
    db = SessionLocal()
    
    try:
        # Get existing users
        users = db.query(User).limit(5).all()
        if len(users) < 2:
            print("Not enough users in database. Please ensure at least 2 users exist.")
            return
        
        # Get a channel
        channels = db.query(Channel).limit(3).all()
        if not channels:
            print("No channels found. Please create channels first.")
            return
        
        current_user = users[0]  # Assuming first user is the current user
        other_users = users[1:]
        
        # Clear existing activities
        db.query(Activity).delete()
        db.commit()
        
        print("Creating activity entries...")
        
        activities_data = []
        base_time = datetime.utcnow()
        
        # 1. Workspace invitation (most recent)
        if len(other_users) > 0:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'workspace_invitation',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["workspace_invitation"]}',
                'target_type': 'user',
                'target_id': current_user.id,
                'activity_metadata': '{"action": "invitation_accepted"}',
                'created_at': base_time - timedelta(minutes=5)
            })
        
        # 2. Mention in channel
        if len(other_users) > 1 and len(channels) > 0:
            activities_data.append({
                'user_id': other_users[1].id,
                'activity_type': 'mention',
                'description': f'{other_users[1].username} {ACTIVITY_TYPES["mention"]} #{channels[0].name}',
                'target_type': 'channel',
                'target_id': channels[0].id,
                'activity_metadata': f'{{"channel_name": "{channels[0].name}", "mentioned_user_id": {current_user.id}}}',
                'created_at': base_time - timedelta(minutes=15)
            })
        
        # 3. Reaction to message
        if len(other_users) > 0:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'reaction',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["reaction"]} 👍',
                'target_type': 'message',
                'target_id': 1,
                'activity_metadata': '{"emoji": "👍", "message_id": 1}',
                'created_at': base_time - timedelta(hours=1)
            })
        
        # 4. Thread reply
        if len(other_users) > 1:
            activities_data.append({
                'user_id': other_users[1].id,
                'activity_type': 'thread_reply',
                'description': f'{other_users[1].username} {ACTIVITY_TYPES["thread_reply"]}',
                'target_type': 'message',
                'target_id': 2,
                'activity_metadata': '{"thread_id": 2, "message_count": 3}',
                'created_at': base_time - timedelta(hours=2)
            })
        
        # 5. Message sent in channel
        if len(other_users) > 0 and len(channels) > 1:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'message_sent',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["message_sent"]} #{channels[1].name}',
                'target_type': 'channel',
                'target_id': channels[1].id,
                'activity_metadata': f'{{"channel_name": "{channels[1].name}"}}',
                'created_at': base_time - timedelta(hours=3)
            })
        
        # 6. File uploaded
        if len(other_users) > 1 and len(channels) > 0:
            activities_data.append({
                'user_id': other_users[1].id,
                'activity_type': 'file_uploaded',
                'description': f'{other_users[1].username} {ACTIVITY_TYPES["file_uploaded"]} #{channels[0].name}',
                'target_type': 'channel',
                'target_id': channels[0].id,
                'activity_metadata': f'{{"file_name": "project_update.pdf", "channel_name": "{channels[0].name}"}}',
                'created_at': base_time - timedelta(hours=5)
            })
        
        # 7. Channel joined
        if len(other_users) > 0 and len(channels) > 2:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'channel_joined',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["channel_joined"]} #{channels[2].name}',
                'target_type': 'channel',
                'target_id': channels[2].id,
                'activity_metadata': f'{{"channel_name": "{channels[2].name}"}}',
                'created_at': base_time - timedelta(hours=8)
            })
        
        # 8. Direct message
        if len(other_users) > 1:
            activities_data.append({
                'user_id': other_users[1].id,
                'activity_type': 'dm_sent',
                'description': f'{other_users[1].username} {ACTIVITY_TYPES["dm_sent"]}',
                'target_type': 'dm',
                'target_id': other_users[1].id,
                'activity_metadata': f'{{"user_id": {other_users[1].id}}}',
                'created_at': base_time - timedelta(hours=12)
            })
        
        # 9. Channel created
        if len(other_users) > 0 and len(channels) > 0:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'channel_created',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["channel_created"]} #{channels[0].name}',
                'target_type': 'channel',
                'target_id': channels[0].id,
                'activity_metadata': f'{{"channel_name": "{channels[0].name}"}}',
                'created_at': base_time - timedelta(days=1)
            })
        
        # 10. Another mention
        if len(other_users) > 0 and len(channels) > 1:
            activities_data.append({
                'user_id': other_users[0].id,
                'activity_type': 'mention',
                'description': f'{other_users[0].username} {ACTIVITY_TYPES["mention"]} #{channels[1].name}',
                'target_type': 'channel',
                'target_id': channels[1].id,
                'activity_metadata': f'{{"channel_name": "{channels[1].name}", "mentioned_user_id": {current_user.id}}}',
                'created_at': base_time - timedelta(days=2)
            })
        
        # Insert all activities
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"✓ Successfully created {len(activities_data)} activity entries")
        
        # Display created activities
        print("\nCreated activities:")
        for i, activity in enumerate(activities_data, 1):
            print(f"{i}. {activity['activity_type']}: {activity['description']}")
        
    except Exception as e:
        print(f"Error seeding activities: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Activity Data Seeding Script")
    print("=" * 60)
    print()
    print("This script will:")
    print("1. Clear existing activities")
    print("2. Create sample activities of various types:")
    print("   - Workspace invitations")
    print("   - Mentions")
    print("   - Reactions")
    print("   - Thread replies")
    print("   - Messages sent")
    print("   - Files uploaded")
    print("   - Channel joins")
    print("   - Direct messages")
    print("   - Channel creations")
    print()
    
    response = input("Continue? (yes/no): ").lower()
    if response == 'yes' or response == 'y':
        seed_activities()
        print("\n✓ Activity seeding completed!")
    else:
        print("Seeding cancelled.")
