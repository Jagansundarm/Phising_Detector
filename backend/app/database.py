"""
Database configuration and models for user authentication
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL - Use SQLite for development, PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./phishguard.db")

# Handle Render's postgres:// URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class User(Base):
    """User model for storing user details"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Preferences
    subscribe_newsletter = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Statistics
    total_scans = Column(Integer, default=0)
    phishing_detected = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<User {self.email}>"


class ScanHistory(Base):
    """Model for storing user scan history"""
    __tablename__ = "scan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)  # Nullable for anonymous scans
    
    url = Column(Text, nullable=False)
    prediction = Column(String(50), nullable=False)  # 'legitimate' or 'phishing'
    confidence = Column(String(10), nullable=False)  # Stored as string for simplicity
    risk_level = Column(String(20), nullable=False)
    
    # Timestamps
    scanned_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScanHistory {self.url[:30]}... - {self.prediction}>"


# Dependency to get database session
def get_db():
    """Dependency that provides a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
