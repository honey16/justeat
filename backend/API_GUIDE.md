# API Usage Guide

Complete guide for using the Restaurant Management API.

## Quick Start

### 1. Authentication

#### Register a Customer

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newcustomer@example.com",
    "password": "password123",
    "name": "John Doe",
    "role": "customer",
    "phone": "+1 555-0199",
    "address": "123 Main St"
  }'
```

#### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@test.com",
    "password": "123456"
  }'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "u1",
    "email": "customer@test.com",
    "name": "Alex Morgan",
    "role": "customer",
    "phone": "+1 555-0123",
    "address": "42 Elm Street, Brooklyn, NY",
    "restaurant_id": null,
    "created_at": "2026-04-05T10:00:00"
  }
}
```

Save the `access_token` for subsequent requests.

### 2. Browse Restaurants

#### Get All Restaurants

```bash
curl http://localhost:8000/api/restaurants
```

#### Search Restaurants

```bash
# By location
curl "http://localhost:8000/api/restaurants?location=Hauz%20Khas"

# By cuisine
curl "http://localhost:8000/api/restaurants?cuisine=Italian"

# By search query
curl "http://localhost:8000/api/restaurants?query=pizza"

# Combined filters
curl "http://localhost:8000/api/restaurants?cuisine=Italian&location=Hauz%20Khas&price_range=$$"
```

#### Get Restaurant Details with Menu

```bash
curl http://localhost:8000/api/restaurants/r1
```

### 3. Customer Operations

All customer endpoints require authentication. Include the token in the header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### View Profile

```bash
curl http://localhost:8000/api/customer/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Update Profile

```bash
curl -X PUT http://localhost:8000/api/customer/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Morgan Updated",
    "phone": "+1 555-9999",
    "address": "New Address"
  }'
```

#### Place an Order

```bash
curl -X POST http://localhost:8000/api/customer/orders \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": "r1",
    "items": [
      {"menu_item_id": "m1", "quantity": 2},
      {"menu_item_id": "m4", "quantity": 1}
    ]
  }'
```

#### View Order History

```bash
# All orders
curl http://localhost:8000/api/customer/orders \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by status
curl "http://localhost:8000/api/customer/orders?status=delivered" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Search orders
curl "http://localhost:8000/api/customer/orders?query=Golden%20Fork" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Manage Preferences

```bash
# Get preferences
curl http://localhost:8000/api/customer/preferences \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Update preferences
curl -X PUT http://localhost:8000/api/customer/preferences \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "favorite_restaurants": ["r1", "r2"],
    "favorite_cuisines": ["Italian", "Japanese"],
    "dietary_restrictions": ["Vegetarian"]
  }'
```

#### Get Recommendations

```bash
curl http://localhost:8000/api/customer/recommendations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Restaurant Owner Operations

Login as owner first:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@test.com",
    "password": "123456"
  }'
```

#### Get My Restaurant

```bash
curl http://localhost:8000/api/owner/restaurant \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN"
```

#### Create Restaurant (for new owners)

```bash
curl -X POST http://localhost:8000/api/owner/restaurant \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New Restaurant",
    "cuisine": "Italian",
    "price_range": "$$",
    "delivery_time": "30-45 min",
    "location": "Downtown",
    "description": "Amazing food!",
    "gradient": "from-blue-400 to-purple-500"
  }'
```

#### Update Restaurant

```bash
curl -X PUT http://localhost:8000/api/owner/restaurant \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Restaurant Name",
    "description": "New description"
  }'
```

#### Add Menu Item

```bash
curl -X POST http://localhost:8000/api/owner/menu \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": "r1",
    "name": "Special Pasta",
    "description": "Delicious pasta with secret sauce",
    "price": 18.99,
    "category": "Pasta",
    "is_special": true,
    "special_label": "Today'\''s Special"
  }'
```

#### Update Menu Item

```bash
curl -X PUT http://localhost:8000/api/owner/menu/m1 \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 16.99,
    "is_special": false
  }'
```

#### Delete Menu Item

```bash
curl -X DELETE http://localhost:8000/api/owner/menu/m5 \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN"
```

#### View Orders

```bash
# All orders
curl http://localhost:8000/api/owner/orders \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN"

# Filter by status
curl "http://localhost:8000/api/owner/orders?status=pending" \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN"
```

#### Update Order Status

```bash
curl -X PUT http://localhost:8000/api/owner/orders/o1/status \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "preparing"
  }'
```

Status flow: `pending` → `preparing` → `delivered`

#### Get Popular Items

```bash
curl http://localhost:8000/api/owner/analytics/popular-items \
  -H "Authorization: Bearer OWNER_ACCESS_TOKEN"
```

## Common Patterns

### Error Handling

All errors return JSON with a `detail` field:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### Pagination

Currently, endpoints return all results. For production, add pagination:

```
?page=1&limit=20
```

### Filtering

Most list endpoints support filtering via query parameters:

- Restaurants: `location`, `cuisine`, `price_range`, `query`
- Orders: `status`, `query`

## Testing with Postman

1. Import the API into Postman from the Swagger UI
2. Create an environment with:
   - `base_url`: http://localhost:8000
   - `token`: (set after login)
3. Use `{{base_url}}` and `{{token}}` in requests

## Testing with Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "customer@test.com",
    "password": "123456"
})
data = response.json()
token = data["access_token"]

# Use token
headers = {"Authorization": f"Bearer {token}"}

# Get restaurants
restaurants = requests.get(f"{BASE_URL}/restaurants").json()
print(restaurants)

# Get profile
profile = requests.get(f"{BASE_URL}/customer/profile", headers=headers).json()
print(profile)

# Place order
order = requests.post(f"{BASE_URL}/customer/orders", headers=headers, json={
    "restaurant_id": "r1",
    "items": [
        {"menu_item_id": "m1", "quantity": 2}
    ]
}).json()
print(order)
```

## Frontend Integration Example

```javascript
// Login
const login = async (email, password) => {
  const response = await fetch("http://localhost:8000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  localStorage.setItem("token", data.access_token);
  return data;
};

// Authenticated request
const getProfile = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch("http://localhost:8000/api/customer/profile", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return await response.json();
};

// Get restaurants
const getRestaurants = async (filters = {}) => {
  const params = new URLSearchParams(filters);
  const response = await fetch(
    `http://localhost:8000/api/restaurants?${params}`,
  );
  return await response.json();
};

// Place order
const placeOrder = async (restaurantId, items) => {
  const token = localStorage.getItem("token");
  const response = await fetch("http://localhost:8000/api/customer/orders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ restaurant_id: restaurantId, items }),
  });
  return await response.json();
};
```

## WebSocket Support (Future)

For real-time order updates, WebSocket support can be added:

```python
# Future implementation
ws://localhost:8000/ws/orders/{order_id}
```

## Rate Limiting (Production)

For production, implement rate limiting:

```python
# Example: 100 requests per minute per IP
from slowapi import Limiter
```

## Monitoring

The API logs all requests to `logs/app.log`. Monitor this file for:

- Failed login attempts
- Errors
- Performance issues
- Security incidents
