from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Allow overriding the database via environment variables. This makes it
# easy to mount a persistent disk (set DATABASE_FILE to the mounted path) or
# use a managed database by setting DATABASE_URL (e.g. postgres://...)
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_FILE = os.getenv('DATABASE_FILE') or os.path.join(os.path.dirname(__file__), '..', 'data', 'slack_rl.db')

if DATABASE_URL:
    # e.g. postgres or another SQLAlchemy-compatible URL
    engine = create_engine(DATABASE_URL)
else:
    db_path = os.path.abspath(DATABASE_FILE)
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
