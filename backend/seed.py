"""
Simple database initialization - creates tables only
"""

from backend.database import engine, Base


def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created!")


if __name__ == "__main__":
    init_db()
