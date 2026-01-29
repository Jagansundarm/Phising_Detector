"""
Authentication API endpoints
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db, User, init_db
from .schemas import (
    UserCreate, UserLogin, UserResponse, UserProfileUpdate,
    LoginResponse, RegisterResponse, AuthResponse
)
from .auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Password must contain:
    - At least 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    - One special character
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        subscribe_newsletter=user_data.subscribe_newsletter,
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RegisterResponse(
        success=True,
        message="Account created successfully! Please check your email to verify your account.",
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been disabled. Please contact support."
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if credentials.remember_me:
        token_expires = timedelta(days=30)  # Extended token for "remember me"
    
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=token_expires
    )
    
    return LoginResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    if profile_update.full_name is not None:
        current_user.full_name = profile_update.full_name
    
    if profile_update.subscribe_newsletter is not None:
        current_user.subscribe_newsletter = profile_update.subscribe_newsletter
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=AuthResponse)
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout user (client should discard the token).
    Server-side logout would require token blacklisting.
    """
    return AuthResponse(
        success=True,
        message="Logged out successfully"
    )


@router.delete("/me", response_model=AuthResponse)
async def delete_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete current user's account."""
    db.delete(current_user)
    db.commit()
    
    return AuthResponse(
        success=True,
        message="Account deleted successfully"
    )


@router.get("/stats", response_model=dict)
async def get_user_stats(current_user: User = Depends(get_current_active_user)):
    """Get user's scanning statistics."""
    return {
        "total_scans": current_user.total_scans,
        "phishing_detected": current_user.phishing_detected,
        "legitimate_urls": current_user.total_scans - current_user.phishing_detected,
        "account_created": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None
    }


# Initialize database on module load
init_db()
