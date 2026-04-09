# JustEat - Restaurant Management & Food Delivery Platform

A full-stack food delivery application with separate customer and restaurant owner interfaces. Built with FastAPI (Python) backend and React frontend.

## 🚀 Features

### Customer Features

- Browse restaurants with filters (cuisine, location, price range)
- View restaurant menus and special items
- Add items to cart and place orders
- Track order status in real-time
- Manage profile and delivery addresses
- Save favorite restaurants and cuisines
- Get personalized restaurant recommendations
- Order history with search functionality

### Restaurant Owner Features

- Dashboard with analytics (revenue, orders, ratings)
- Manage restaurant details (name, email, cuisine, location)
- Add, edit, and delete menu items
- Mark items as specials or deals
- View and manage incoming orders
- Update order status (pending → preparing → delivered)
- View most ordered items

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Git**

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd JustEat
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL databases
psql -U postgres
CREATE DATABASE justeat;
CREATE DATABASE "justeat-test";
\q

# Configure environment variables
# Edit .env file with your database credentials
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/justeat

# Run database migrations
alembic upgrade head

# Seed the database with sample data
python seed.py

# Start the backend server
uvicorn main:app --reload
```

Backend will run on: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will run on: **http://localhost:8081**

## 🔐 Test Credentials

### Customer Account

- **Email:** customer@test.com
- **Password:** 123456

### Restaurant Owner Account

- **Email:** owner@test.com
- **Password:** 123456
- **Restaurant:** The Golden Fork

## 📚 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user (customer/owner)
- `POST /api/auth/login` - Login
- `POST /api/auth/reset-password` - Reset password

### Restaurants (Public)

- `GET /api/restaurants` - List all restaurants (with filters)
- `GET /api/restaurants/{id}` - Get restaurant details
- `GET /api/restaurants/{id}/menu` - Get restaurant menu
- `GET /api/restaurants/{id}/specials` - Get special items
- `GET /api/restaurants/{id}/popular` - Get popular items

### Customer (Protected)

- `GET /api/customer/profile` - Get customer profile
- `PUT /api/customer/profile` - Update profile
- `POST /api/customer/orders` - Place new order
- `GET /api/customer/orders` - Get order history
- `GET /api/customer/orders/{id}` - Get order details
- `GET /api/customer/preferences` - Get user preferences
- `PUT /api/customer/preferences` - Update preferences
- `GET /api/customer/recommendations` - Get restaurant recommendations

### Owner (Protected)

- `GET /api/owner/restaurant` - Get restaurant details
- `PUT /api/owner/restaurant` - Update restaurant
- `POST /api/owner/restaurant` - Create restaurant
- `GET /api/owner/menu` - Get menu items
- `POST /api/owner/menu` - Add menu item
- `PUT /api/owner/menu/{id}` - Update menu item
- `DELETE /api/owner/menu/{id}` - Delete menu item
- `GET /api/owner/orders` - Get restaurant orders
- `PUT /api/owner/orders/{id}/status` - Update order status
- `GET /api/owner/analytics/popular-items` - Get analytics

For complete API documentation, visit: **http://localhost:8000/docs**

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Activate virtual environment
venv\Scripts\activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test class or method
pytest tests/test_auth.py::TestAuthEndpoints::test_login_success
```

**Test Coverage:**

- 48 test cases across 6 test files
- Authentication tests (8 tests)
- Restaurant endpoints tests (10 tests)
- Customer operations tests (10 tests)
- Owner operations tests (13 tests)
- Database models tests (7 tests)

**Test Database:**
Tests use a separate database: `justeat-test`

## 📁 Project Structure

```
JustEat/
├── backend/
│   ├── app/
│   │   ├── routers/          # API route handlers
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── customer.py   # Customer endpoints
│   │   │   ├── owner.py      # Owner endpoints
│   │   │   └── restaurants.py # Public restaurant endpoints
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── database.py       # Database configuration
│   │   ├── auth.py           # JWT authentication
│   │   ├── dependencies.py   # Dependency injection
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── logger.py         # Logging configuration
│   ├── tests/                # Pytest test suite
│   │   ├── conftest.py       # Test fixtures
│   │   ├── test_auth.py
│   │   ├── test_customer.py
│   │   ├── test_owner.py
│   │   ├── test_restaurants.py
│   │   └── test_models.py
│   ├── alembic/              # Database migrations
│   ├── main.py               # FastAPI application
│   ├── seed.py               # Database seeder
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── features/         # Feature modules
│   │   │   ├── auth/         # Authentication
│   │   │   ├── customer/     # Customer features
│   │   │   └── restaurant/   # Owner features
│   │   ├── context/          # React context providers
│   │   ├── services/         # API service layer
│   │   ├── hooks/            # Custom React hooks
│   │   └── pages/            # Page components
│   └── package.json          # Node dependencies
│
└── .gitignore
```

## 🔧 Technologies Used

### Backend

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **React Router** - Navigation
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Sonner** - Toast notifications
- **Lucide React** - Icons

## 🗄️ Database Migrations

### Create a new migration

```bash
cd backend
alembic revision -m "description of change"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history
```

### Frontend (Azure Static Web Apps)

```bash
# Build frontend
cd frontend
npm run build

# Deploy to Azure Static Web Apps
az staticwebapp create --name justeat-web --resource-group JustEatResourceGroup
```

See deployment guide for detailed instructions.

## 📝 Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/justeat
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```
