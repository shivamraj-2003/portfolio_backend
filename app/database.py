from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings


class Database:
    """MongoDB database connection manager"""
    
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.db = db.client[settings.DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("✅ MongoDB connection closed")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Analytics indexes
        await db.db.analytics.create_index("created_at", name="analytics_created_at_idx")
        await db.db.analytics.create_index("section", name="section_idx")
        await db.db.analytics.create_index("device", name="device_idx")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️ Error creating indexes: {e}")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db.db
