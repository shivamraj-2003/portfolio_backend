from fastapi import APIRouter, HTTPException, status, Request
from ..schemas.analytics import AnalyticsRequest, AnalyticsResponse
from ..models.analytics import Analytics
from ..database import get_database
from datetime import datetime


router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request
    
    Checks X-Forwarded-For header first (for proxies/load balancers),
    then falls back to direct client IP
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/visit", response_model=AnalyticsResponse, status_code=status.HTTP_201_CREATED)
async def track_section_visit(analytics: AnalyticsRequest, request: Request):
    """
    Track section visit analytics
    
    - Captures section name (about, projects, experience, contact)
    - Records device type (desktop, mobile)
    - Automatically captures IP address
    - Stores timestamp
    - No authentication required
    """
    try:
        db = get_database()
        
        # Get client IP address
        ip_address = get_client_ip(request)
        
        # Create analytics document
        analytics_data = Analytics(
            section=analytics.section,
            device=analytics.device,
            visitor_name=analytics.visitor_name,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        
        # Insert into database
        result = await db.analytics.insert_one(analytics_data.model_dump(by_alias=True, exclude={"id"}))
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to track visit"
            )
        
        return AnalyticsResponse(
            success=True,
            message="Visit tracked successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in track_section_visit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while tracking visit"
        )
