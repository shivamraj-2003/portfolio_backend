from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Analytics(BaseModel):
    """Analytics model for tracking section visits"""
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    section: Literal["home", "about", "projects", "experience", "contact"]
    device: Literal["desktop", "mobile"]
    visitor_name: Optional[str] = "Anonymous"
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "section": "projects",
                "device": "desktop",
                "visitor_name": "John Doe",
                "ip_address": "192.168.1.1",
                "created_at": "2024-01-01T00:00:00"
            }
        }
