from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Activity

def inspect_activities():
    db: Session = SessionLocal()
    try:
        activities = db.query(Activity).all()
        for activity in activities:
            print(activity.id, activity.description, activity.created_at)
    finally:
        db.close()

if __name__ == "__main__":
    inspect_activities()