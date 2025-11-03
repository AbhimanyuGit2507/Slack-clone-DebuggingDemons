from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from .database import SessionLocal
from .models import Session as SessionModel, User
from .config import settings


class SessionAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle session authentication for protected routes"""
    
    # Routes that don't require authentication
    PUBLIC_ROUTES = [
        "/api/auth/signup",
        "/api/auth/login",
        "/api/auth/check",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Check if route requires authentication
        path = request.url.path
        
        # Allow public routes
        if any(path.startswith(route) for route in self.PUBLIC_ROUTES):
            return await call_next(request)
        
        # Allow OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # For protected API routes, verify session
        if path.startswith("/api/"):
            session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
            
            if not session_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Not authenticated"}
                )
            
            # Verify session in database
            db = SessionLocal()
            try:
                session = db.query(SessionModel).filter(
                    SessionModel.session_id == session_id
                ).first()
                
                if not session:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid session"}
                    )
                
                if session.expires_at < datetime.utcnow():
                    db.delete(session)
                    db.commit()
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Session expired"}
                    )
                
                # Session is valid, continue with request
                user = db.query(User).filter(User.id == session.user_id).first()
                if not user:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "User not found"}
                    )
                
            finally:
                db.close()
        
        response = await call_next(request)
        return response


def get_current_session_user(request: Request, db: Session) -> Optional[User]:
    """Helper function to get current user from session in request"""
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    
    if not session_id:
        return None
    
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id
    ).first()
    
    if not session or session.expires_at < datetime.utcnow():
        return None
    
    user = db.query(User).filter(User.id == session.user_id).first()
    return user
