# 🏗️ Project Architecture

## Directory Structure

```
Backend/
│
├── 📁 app/                          # Main application package
│   ├── 📄 __init__.py              # Package initializer
│   ├── 📄 main.py                  # FastAPI app & CORS setup
│   ├── 📄 config.py                # Environment configuration
│   ├── 📄 database.py              # MongoDB connection & indexes
│   │
│   ├── 📁 models/                  # Database models (MongoDB documents)
│   │   ├── 📄 contact.py           # Contact message model
│   │   ├── 📄 analytics.py         # Analytics tracking model
│   │   └── 📄 admin.py             # Admin user model
│   │
│   ├── 📁 schemas/                 # Pydantic schemas (validation)
│   │   ├── 📄 contact.py           # Contact request/response schemas
│   │   ├── 📄 analytics.py         # Analytics request/response schemas
│   │   └── 📄 admin.py             # Admin auth & message schemas
│   │
│   ├── 📁 routes/                  # API endpoints
│   │   ├── 📄 contact.py           # POST /contact
│   │   ├── 📄 analytics.py         # POST /analytics/visit
│   │   └── 📄 admin.py             # Admin endpoints (login, messages)
│   │
│   └── 📁 utils/                   # Utility functions
│       ├── 📄 jwt.py               # JWT token creation & verification
│       └── 📄 email.py             # Email notification service
│
├── 📄 .env.example                 # Environment variables template
├── 📄 ENV_TEMPLATE.txt             # Manual .env creation guide
├── 📄 .gitignore                   # Git ignore rules
├── 📄 requirements.txt             # Python dependencies
├── 📄 Procfile                     # Heroku deployment config
├── 📄 runtime.txt                  # Python version for deployment
│
├── 📄 setup.bat                    # Windows setup script
├── 📄 start.bat                    # Windows start script
├── 📄 generate_secret.py           # JWT secret key generator
│
├── 📄 README.md                    # Full documentation
├── 📄 QUICKSTART.md                # Quick start guide
└── 📄 FRONTEND_INTEGRATION.md      # Frontend integration examples
```

---

## 🔄 Request Flow

### 1. Contact Form Submission

```
Frontend (HTML/React)
    ↓
POST /contact
    ↓
routes/contact.py
    ↓
schemas/contact.py (Validation)
    ↓
models/contact.py (Create document)
    ↓
database.py (MongoDB insert)
    ↓
utils/email.py (Send notification)
    ↓
Response: {success: true, message: "..."}
```

### 2. Analytics Tracking

```
Frontend (Swiper slide change)
    ↓
POST /analytics/visit
    ↓
routes/analytics.py
    ↓
schemas/analytics.py (Validation)
    ↓
models/analytics.py (Create document)
    ↓
database.py (MongoDB insert)
    ↓
Response: {success: true, message: "Visit tracked"}
```

### 3. Admin Authentication

```
Admin Login Page
    ↓
POST /admin/login
    ↓
routes/admin.py (Verify credentials)
    ↓
utils/jwt.py (Create JWT token)
    ↓
Response: {access_token: "...", role: "admin"}
    ↓
Frontend stores token
```

### 4. Admin Dashboard (Protected)

```
Admin Dashboard
    ↓
GET /admin/messages
    ↓
routes/admin.py
    ↓
utils/jwt.py (Verify token) ← Authorization: Bearer <token>
    ↓
database.py (Fetch messages)
    ↓
Response: [{id, name, email, message, ...}, ...]
```

---

## 🗄️ Database Collections

### contact_messages

```javascript
{
  _id: ObjectId("..."),
  name: "John Doe",
  email: "john@example.com",
  message: "I'd like to discuss...",
  is_read: false,
  created_at: ISODate("2024-01-01T00:00:00Z")
}
```

**Indexes:**

- `created_at` (descending) - For sorting
- `is_read` - For filtering
- `email` - For searching

### analytics

```javascript
{
  _id: ObjectId("..."),
  section: "projects",
  device: "desktop",
  ip_address: "192.168.1.1",
  created_at: ISODate("2024-01-01T00:00:00Z")
}
```

**Indexes:**

- `created_at` (descending) - For time-based queries
- `section` - For section-wise analytics
- `device` - For device-wise analytics

---

## 🔐 Security Layers

### 1. Input Validation (Pydantic)

- Type checking
- Field validation
- Min/max length
- Email format validation

### 2. JWT Authentication

- Token-based auth
- Expiration time
- Role-based access (admin)
- Bearer token in headers

### 3. CORS Protection

- Whitelist allowed origins
- Credentials support
- Method restrictions

### 4. Environment Variables

- Sensitive data in .env
- Not committed to git
- Different configs per environment

---

## 📊 API Endpoints Summary

| Method | Endpoint                    | Auth | Description          |
| ------ | --------------------------- | ---- | -------------------- |
| GET    | `/`                         | ❌   | API info & health    |
| GET    | `/health`                   | ❌   | Health check         |
| POST   | `/contact`                  | ❌   | Submit contact form  |
| POST   | `/analytics/visit`          | ❌   | Track section visit  |
| POST   | `/admin/login`              | ❌   | Admin authentication |
| GET    | `/admin/messages`           | ✅   | Get all messages     |
| PUT    | `/admin/messages/{id}/read` | ✅   | Mark as read         |
| DELETE | `/admin/messages/{id}`      | ✅   | Delete message       |

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│  (Netlify/Vercel/GitHub Pages)                  │
│                                                  │
│  - HTML/CSS/JavaScript                          │
│  - Swiper for sections                          │
│  - Contact form                                 │
│  - Admin dashboard                              │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS/CORS
                   ↓
┌─────────────────────────────────────────────────┐
│              FastAPI Backend                     │
│     (Railway/Render/Heroku)                     │
│                                                  │
│  - Contact API                                  │
│  - Analytics API                                │
│  - Admin API (JWT protected)                    │
└──────────┬─────────────────┬────────────────────┘
           │                 │
           ↓                 ↓
┌──────────────────┐  ┌─────────────────┐
│   MongoDB Atlas  │  │  SMTP Server    │
│                  │  │  (Gmail)        │
│  - Messages      │  │                 │
│  - Analytics     │  │  - Notifications│
└──────────────────┘  └─────────────────┘
```

---

## 🔧 Technology Stack Details

### Backend

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **python-jose** - JWT implementation
- **passlib** - Password hashing
- **aiosmtplib** - Async email sending

### Database

- **MongoDB Atlas** - Cloud database
- **Indexes** - Optimized queries
- **Collections** - contact_messages, analytics

### Authentication

- **JWT** - JSON Web Tokens
- **Bearer Token** - Authorization header
- **Role-based** - Admin access control

### Email

- **SMTP** - Email protocol
- **Gmail** - Email provider
- **HTML Templates** - Rich email formatting

---

## 📈 Scalability Considerations

1. **Database Indexes** - Fast queries even with millions of records
2. **Async Operations** - Non-blocking I/O for better performance
3. **Connection Pooling** - Efficient database connections
4. **Stateless API** - Easy horizontal scaling
5. **JWT Tokens** - No server-side session storage
6. **CORS** - Multiple frontend deployments

---

## 🧪 Testing Strategy

1. **Swagger UI** - Interactive API testing
2. **Manual Testing** - cURL commands
3. **Frontend Integration** - Real-world usage
4. **Email Testing** - Verify notifications
5. **Auth Testing** - JWT token validation
6. **Error Handling** - Edge cases

---

## 📝 Best Practices Implemented

✅ Environment-based configuration
✅ Proper error handling
✅ Input validation
✅ Security best practices
✅ Clean code structure
✅ Comprehensive documentation
✅ Production-ready setup
✅ Easy deployment
✅ CORS configuration
✅ Database indexing
✅ Async operations
✅ Type hints
✅ Logging
✅ Health checks
