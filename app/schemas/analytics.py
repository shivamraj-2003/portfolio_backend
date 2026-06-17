from pydantic import BaseModel, field_validator
from typing import Literal, Optional


class AnalyticsRequest(BaseModel):
    """Analytics tracking request schema"""
    
    section: Literal["home", "about", "projects", "experience", "contact"]
    device: Literal["desktop", "mobile"]
    visitor_name: Optional[str] = "Anonymous"
    
    @field_validator('section')
    @classmethod
    def validate_section(cls, v):
        allowed_sections = ["home", "about", "projects", "experience", "contact"]
        if v not in allowed_sections:
            raise ValueError(f'Section must be one of: {", ".join(allowed_sections)}')
        return v
    
    @field_validator('device')
    @classmethod
    def validate_device(cls, v):
        allowed_devices = ["desktop", "mobile"]
        if v not in allowed_devices:
            raise ValueError(f'Device must be one of: {", ".join(allowed_devices)}')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "section": "projects",
                "device": "desktop",
                "visitor_name": "John Doe"
            }
        }


class AnalyticsResponse(BaseModel):
    """Analytics tracking response schema"""
    
    success: bool
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Visit tracked successfully"
            }
        }
