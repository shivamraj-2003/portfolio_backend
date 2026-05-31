# Portfolio Backend API

FastAPI backend for personal portfolio website with MongoDB visitor tracking and Admin analytics.

## Features
- ✅ Visitor tracking (section-based)
- ✅ Admin dashboard API for analytics
- ✅ JWT-based authentication
- ✅ MongoDB integration (Motor async)
- ✅ Swagger/OpenAPI documentation

## Tech Stack
- **FastAPI**
- **MongoDB (Motor)**
- **JWT**
- **Pydantic**

## Installation

### 1. Configure Environment
Copy `.env.example` to `.env` and update:
- `MONGODB_URL`: Your MongoDB connection string.
- `SECRET_KEY`: Generate a secure key for JWT.
- `ADMIN_EMAIL` & `ADMIN_PASSWORD`: Your dashboard credentials.

### 2. Run Setup
```bash
setup.bat
```

## Running the Application
```bash
# Activation
venv\Scripts\activate
# Start
python -m app.main
```
The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

## API Endpoints

### Visitor Tracking
**POST** `/analytics/visit`
Tracks a section visit.
```json
{
  "section": "projects",
  "device": "desktop"
}
```

### Admin
**POST** `/admin/login`: Get JWT token.
**GET** `/admin/analytics`: Get detailed visitor logs (Protected).

## License
MIT
