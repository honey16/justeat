# Restaurant Management API

Complete FastAPI backend for a restaurant management system with PostgreSQL, JWT authentication, and role-based access control.

## Features

### Authentication & Authorization

- ✅ JWT-based authentication
- ✅ Role-based access control (Customer & Restaurant Owner)
- ✅ Secure password hashing with bcrypt
- ✅ Password reset functionality
- ✅ Session handling via JWT tokens

### Customer Features

- ✅ Browse and search restaurants (by location, cuisine, name)
- ✅ View restaurant menus with prices and details
- ✅ Filter restaurants by cuisine type, price range, location
- ✅ Add items to cart and place orders
- ✅ Track order status (pending → preparing → delivered)
- ✅ View and search order history
- ✅ View and update profile
- ✅ Save preferences (favorite restaurants, cuisines, dietary restrictions)
- ✅ Get personalized recommendations based on order history

### Restaurant Owner Features

- ✅ Register and manage restaurants
- ✅ Add, edit, and delete menu items
- ✅ Manage customer orders
- ✅ Update order status
- ✅ Mark items as specials ("Today's Special", "Deal of the Day")
- ✅ View "Mostly Ordered" items (automatic tracking)
- ✅ View order details and analytics

### Technical Features

- ✅ Comprehensive logging system
- ✅ Exception handling and error responses
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ RESTful API design
- ✅ Interactive API documentation (Swagger UI)
- ✅ CORS support for frontend integration

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── auth.py              # JWT authentication utilities
│   ├── database.py          # Database configuration
│   ├── dependencies.py      # FastAPI dependencies (auth guards)
│   ├── exceptions.py        # Custom exceptions and handlers
│   ├── logger.py           # Logging configuration
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic schemas for validation
│   └── routers/
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints
│       ├── customer.py     # Customer endpoints
│       ├── owner.py        # Restaurant owner endpoints
│       └── restaurants.py  # Public restaurant endpoints
├── logs/                   # Application logs
├── main.py                # FastAPI application entry point
├── seed.py                # Database seeding script
├── .env                   # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+

### 1. Database Setup

Install and start PostgreSQL, then create a database:

```bash
# Using psql
createdb restaurant_db

# Or using SQL
CREATE DATABASE restaurant_db;
```

### 2. Environment Configuration

Update the `.env` file with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/restaurant_db
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

### 3. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 4. Initialize Database

Run the seed script to create tables and populate initial data:

```bash
python seed.py
```

To reset the database (drop and recreate all tables):

```bash
python seed.py --reset
```

### 5. Start the Server

```bash
# Run with auto-reload
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Test Credentials

After running the seed script, use these credentials:

### Customer Account

- **Email**: customer@test.com
- **Password**: 123456

### Restaurant Owner Account

- **Email**: owner@test.com
- **Password**: 123456
- **Restaurant**: The Golden Fork

## API Endpoints

### Authentication (`/api/auth`)

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/reset-password` - Reset password

### Restaurants (`/api/restaurants`)

- `GET /restaurants` - List all restaurants (with filters)
- `GET /restaurants/{id}` - Get restaurant with menu
- `GET /restaurants/{id}/menu` - Get restaurant menu
- `GET /restaurants/{id}/specials` - Get special items
- `GET /restaurants/{id}/popular` - Get popular items

### Customer (`/api/customer`) - Protected

- `GET /customer/profile` - Get profile
- `PUT /customer/profile` - Update profile
- `POST /customer/orders` - Create order
- `GET /customer/orders` - Get order history (with search)
- `GET /customer/orders/{id}` - Get order details
- `GET /customer/preferences` - Get preferences
- `PUT /customer/preferences` - Update preferences
- `GET /customer/recommendations` - Get recommendations

### Restaurant Owner (`/api/owner`) - Protected

- `GET /owner/restaurant` - Get restaurant details
- `POST /owner/restaurant` - Create restaurant
- `PUT /owner/restaurant` - Update restaurant
- `GET /owner/menu` - Get menu items
- `POST /owner/menu` - Add menu item
- `PUT /owner/menu/{id}` - Update menu item
- `DELETE /owner/menu/{id}` - Delete menu item
- `GET /owner/orders` - Get all orders
- `GET /owner/orders/{id}` - Get order details
- `PUT /owner/orders/{id}/status` - Update order status
- `GET /owner/analytics/popular-items` - Get popular items

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

To get a token, login via `/api/auth/login` endpoint.

## Database Schema

### Users

- Stores customer and restaurant owner accounts
- Password hashing with bcrypt
- Role-based access control

### Restaurants

- Restaurant information and details
- Linked to owner users

### Menu Items

- Restaurant menu with pricing
- Special labels and order tracking
- Automatic "Mostly Ordered" calculation

### Orders

- Customer orders with items
- Status tracking (pending/preparing/delivered/cancelled)
- Order history and totals

### User Preferences

- Customer favorites and dietary restrictions
- Used for personalized recommendations

## Logging

Application logs are stored in the `logs/` directory:

- `app.log` - All application logs

Logs include:

- API requests and responses
- Authentication attempts
- Database operations
- Errors and exceptions

## Error Handling

The API uses custom exception handlers:

- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

All errors return JSON with a `detail` field.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

## Frontend Integration

The backend is configured to work with the React frontend:

- CORS enabled for `http://localhost:5173` and `http://localhost:3000`
- JWT tokens for authentication
- RESTful endpoints matching frontend expectations

## Production Deployment

1. Update `.env` with production values
2. Change `SECRET_KEY` to a strong random key
3. Set `DEBUG=False`
4. Use a production-grade ASGI server (e.g., Gunicorn with Uvicorn workers)
5. Set up SSL/TLS certificates
6. Configure PostgreSQL for production
7. Set up proper logging and monitoring

## License

MIT
