from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class AdminLoginRequest(BaseModel):
    """Admin login request schema"""
    
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "admin123"
            }
        }


class AdminLoginResponse(BaseModel):
    """Admin login response schema"""
    
    access_token: str
    token_type: str = "bearer"
    role: str = "admin"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "role": "admin"
            }
        }


class VisitLogResponse(BaseModel):
    """Analytics visit log response schema"""
    
    id: str
    section: str
    device: str
    ip_address: str
    created_at: datetime


class AdminAnalyticsSummary(BaseModel):
    """Summary of analytics for admin dashboard"""
    
    total_visits: int
    visits: List[VisitLogResponse]
