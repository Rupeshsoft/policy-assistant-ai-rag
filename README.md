# Policy Assistant AI App

A FastAPI-based authentication and authorization system with role-based access control (Admin/User).

## Features

- ✅ User Registration with role assignment (USER/ADMIN)
- ✅ Secure password hashing using bcrypt
- ✅ JWT-based authentication
- ✅ Role-based access control
- ✅ Admin dashboard endpoint
- ✅ CORS enabled
- ✅ MySQL database with SQLAlchemy 

## Tech Stack

| Technology | Purpose |
|------------|---------|ORM
| **FastAPI** | Web framework |
| **SQLAlchemy** | ORM for database interaction |
| **PyMySQL** | MySQL database driver |
| **bcrypt** | Password hashing |
| **python-jose** | JWT token creation/validation |
| **Pydantic** | Request/response validation |
| **Alembic** | Database migrations (optional) |

## Project Structure

```
policy-assistant-ai-app/
├── .env                        # Environment variables
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TODO.md                     # Task tracking
└── app/
    ├── __init__.py
    ├── main.py                 # FastAPI app entry point
    ├── create_tables.py        # Database table creation script
    ├── auth/
    │   ├── __init__.py
    │   ├── jwt_handler.py      # JWT token creation
    │   ├── password.py         # bcrypt password hashing
    │   ├── roles.py            # Role-based authorization deps
    │   └── security.py         # OAuth2 + get_current_user
    ├── core/
    │   └── __init__.py
    ├── database/
    │   ├── __init__.py
    │   └── database.py         # SQLAlchemy engine & session
    ├── models/
    │   ├── __init__.py
    │   └── user.py             # User database model
    ├── routers/
    │   ├── __init__.py
    │   ├── admin.py            # Admin dashboard endpoint
    │   └── auth.py             # Register & Login endpoints
    ├── schemas/
    │   ├── __init__.py
    │   └── user.py             # Pydantic request/response models
    ├── services/
    │   └── __init__.py
    └── uploads/
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL server running on `localhost:3306`
- pip (Python package manager)

### Step 1: Clone & Navigate

```bash
cd policy-assistant-ai-app
```

### Step 2: Create & Activate Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
pip install bcrypt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost:3306/policy_assistant_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
```

> **Note**: The default config uses `root` with empty password. Change as needed.

### Step 5: Create Database

Open MySQL and create the database:

```sql
CREATE DATABASE policy_assistant_db;
```

### Step 6: Create Tables

```bash
python app/create_tables.py
```

### Step 7: Start the Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

#### 1. Home

```
GET /
```

Response:
```json
{
  "message": "Welcome to Policy Assistant AI App!"
}
```

#### 2. Register User

```
POST /auth/register
```

Request Body:
```json
{
  "fullname": "John Doe",
  "email": "john@example.com",
  "mobile": "1234567890",
  "password": "securepass",
  "role": "USER"
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `fullname` | string | ✅ | - | User's full name |
| `email` | string (email) | ✅ | - | Must be unique |
| `mobile` | string | ✅ | - | Must be unique |
| `password` | string | ✅ | - | Will be bcrypt-hashed |
| `role` | string | ❌ | `"USER"` | `"USER"` or `"ADMIN"` |

Response:
```json
{
  "message": "Registration Successful"
}
```

#### 3. Login

```
POST /auth/login
```

Request Body:
```json
{
  "email": "john@example.com",
  "password": "securepass"
}
```

**Regular User Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "USER"
}
```

**Admin User Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "ADMIN",
  "redirect_url": "/admin/dashboard"
}
```

#### 4. Admin Dashboard (Protected)

```
GET /admin/dashboard
Authorization: Bearer <token>
```

**Required Role**: `ADMIN`

Response:
```json
{
  "message": "Welcome Admin",
  "user": {
    "sub": "admin@example.com",
    "role": "ADMIN",
    "exp": 1700000000
  }
}
```

## Usage Examples

### Create an Admin User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "Admin User",
    "email": "admin@example.com",
    "mobile": "9999999999",
    "password": "admin123",
    "role": "ADMIN"
  }'
```

### Login & Get Token

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### Access Admin Dashboard

```bash
curl http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer <your-token-here>"
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

Run from the project root directory and ensure virtual environment is activated:

```bash
cd policy-assistant-ai-app
python app/create_tables.py
```

### `ValueError: password cannot be longer than 72 bytes`

This indicates an incompatible `passlib` + `bcrypt` version. The project uses direct `bcrypt` library instead. Ensure you have `bcrypt>=4.0.0` installed:

```bash
pip install bcrypt
```

### `500 Internal Server Error` on Register/Login

Ensure all `__init__.py` files exist in subdirectories. Re-run table creation:

```bash
python app/create_tables.py
```

## License

MIT

