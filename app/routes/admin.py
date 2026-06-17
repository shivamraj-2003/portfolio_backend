from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import timedelta
from ..schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminAnalyticsSummary,
    VisitLogResponse
)
from ..utils.jwt import create_access_token, get_current_admin
from ..database import get_database
from ..config import settings
from passlib.context import CryptContext


router = APIRouter(prefix="/admin", tags=["Admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(credentials: AdminLoginRequest):
    """
    Admin login endpoint
    """
    try:
        # Verify credentials against environment variables
        if credentials.email != settings.ADMIN_EMAIL:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if credentials.password != settings.ADMIN_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": credentials.email, "role": "admin"},
            expires_delta=access_token_expires
        )
        
        return AdminLoginResponse(
            access_token=access_token,
            token_type="bearer",
            role="admin"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in admin_login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.get("/analytics", response_model=AdminAnalyticsSummary)
async def get_analytics(current_admin: dict = Depends(get_current_admin)):
    """
    Get all visitor analytics (JWT protected, admin only)
    """
    try:
        db = get_database()
        
        # Fetch all analytics records, sorted by created_at descending
        cursor = db.analytics.find().sort("created_at", -1)
        visits_raw = await cursor.to_list(length=1000) # Limit to last 1000 for performance
        
        total_visits = await db.analytics.count_documents({})
        
        visits = []
        for v in visits_raw:
            visits.append(VisitLogResponse(
                id=str(v["_id"]),
                section=v["section"],
                device=v["device"],
                visitor_name=v.get("visitor_name", "Anonymous"),
                ip_address=v.get("ip_address", "unknown"),
                created_at=v["created_at"]
            ))
            
        return AdminAnalyticsSummary(
            total_visits=total_visits,
            visits=visits
        )
        
    except Exception as e:
        print(f"❌ Error in get_analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching analytics"
        )
