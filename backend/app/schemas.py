"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8)
    confirm_password: str
    agree_to_terms: bool
    agree_to_privacy: bool
    subscribe_newsletter: bool = False
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('agree_to_terms')
    def must_agree_to_terms(cls, v):
        if not v:
            raise ValueError('You must agree to the Terms of Service')
        return v
    
    @validator('agree_to_privacy')
    def must_agree_to_privacy(cls, v):
        if not v:
            raise ValueError('You must agree to the Privacy Policy')
        return v
    
    @validator('full_name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Name can only contain letters and spaces')
        return v.strip()


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    subscribe_newsletter: bool
    created_at: datetime
    last_login: Optional[datetime]
    total_scans: int
    phishing_detected: int
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    subscribe_newsletter: Optional[bool] = None


# ==================== Token Schemas ====================

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Data encoded in JWT token"""
    user_id: Optional[int] = None
    email: Optional[str] = None


# ==================== Auth Response Schemas ====================

class AuthResponse(BaseModel):
    """Standard authentication response"""
    success: bool
    message: str
    data: Optional[dict] = None


class LoginResponse(BaseModel):
    """Login response with token and user data"""
    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class RegisterResponse(BaseModel):
    """Registration response"""
    success: bool
    message: str
    user: UserResponse
