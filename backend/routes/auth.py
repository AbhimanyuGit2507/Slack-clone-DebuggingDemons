from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from typing import Optional

from ..database import get_db
from ..models import User, Session as SessionModel
from ..schemas import UserCreate, UserLogin, User as UserSchema, AuthResponse, LogoutResponse
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Helper functions (simplified - no encryption)
def hash_password(password: str) -> str:
    """Store password as plain text (simplified for demo)"""
    return password

def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify password by direct comparison"""
    return plain_password == stored_password

def create_session(user_id: int, db: Session) -> str:
    """Create a new session for a user"""
    session_id = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=settings.SESSION_EXPIRY_HOURS)
    
    session = SessionModel(
        session_id=session_id,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    
    return session_id

def get_current_user(
    session_id: Optional[str] = Cookie(None, alias=settings.SESSION_COOKIE_NAME),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from session cookie"""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    
    if session.expires_at < datetime.utcnow():
        db.delete(session)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# Routes
@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, response: Response, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        status="online"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create session
    session_id = create_session(new_user.id, db)
    
    # Set cookie
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        max_age=settings.SESSION_EXPIRY_HOURS * 3600,
        samesite="lax"
    )
    
    return AuthResponse(
        message="User registered successfully",
        user=UserSchema.model_validate(new_user)
    )

@router.post("/login", response_model=AuthResponse)
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Login a user"""
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Update user status
    user.status = "online"
    db.commit()
    
    # Create session
    session_id = create_session(user.id, db)
    
    # Set cookie
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        max_age=settings.SESSION_EXPIRY_HOURS * 3600,
        samesite="lax"
    )
    
    return AuthResponse(
        message="Login successful",
        user=UserSchema.model_validate(user)
    )

@router.post("/logout", response_model=LogoutResponse)
def logout(
    response: Response,
    session_id: Optional[str] = Cookie(None, alias=settings.SESSION_COOKIE_NAME),
    db: Session = Depends(get_db)
):
    """Logout a user"""
    if session_id:
        # Delete session from database
        session = db.query(SessionModel).filter(
            SessionModel.session_id == session_id
        ).first()
        
        if session:
            # Update user status
            user = db.query(User).filter(User.id == session.user_id).first()
            if user:
                user.status = "offline"
            
            db.delete(session)
            db.commit()
    
    # Clear cookie
    response.delete_cookie(key=settings.SESSION_COOKIE_NAME)
    
    return LogoutResponse(message="Logout successful")

@router.get("/me", response_model=UserSchema)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return UserSchema.model_validate(current_user)

@router.get("/check")
def check_auth(
    session_id: Optional[str] = Cookie(None, alias=settings.SESSION_COOKIE_NAME),
    db: Session = Depends(get_db)
):
    """Check if user is authenticated"""
    if not session_id:
        return {"authenticated": False}
    
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id
    ).first()
    
    if not session or session.expires_at < datetime.utcnow():
        return {"authenticated": False}
    
    return {"authenticated": True, "user_id": session.user_id}
