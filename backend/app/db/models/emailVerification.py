from sqlalchemy import Column, Integer, String, DateTime,Boolean
from app.db.models.base import Base,SerializerMixin
from datetime import datetime
class EmailVerificationDB(Base,SerializerMixin):
    __tablename__ = "email_verifications"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, index=True,unique=True)
    username = Column(String, nullable=False,unique=True)
    hashed_password = Column(String, nullable=False)  
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)