## How to Run Both Servers

### **Start Backend (Terminal 1)**

```bash
cd backend
.\venv\Scripts\Activate.ps1
python main.py
# or
uvicorn main:app --reload
```

**Running on:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### **Start Frontend (Terminal 2)**

```bash
cd frontend
npm run dev
```

**Running on:** http://localhost:5173

## 🔐 Test Credentials

### Customer Account

- **Email:** customer@test.com
- **Password:** 123456
- **Can:** Browse restaurants, place orders, track orders, manage preferences

### Restaurant Owner Account

- **Email:** owner@test.com
- **Password:** 123456
- **Restaurant:** The Golden Fork
- **Can:** Manage menu, process orders, view analytics

## 📝 Quick Test Flow

1. **Start both servers** (backend on 8000, frontend on 5173)

2. **Login as Customer:**
   - Go to http://localhost:5173/login
   - Use customer@test.com / 123456
   - Browse restaurants
   - Add items to cart
   - Place an order
   - View order history

3. **Login as Owner:**
   - Logout and login with owner@test.com / 123456
   - View orders from customers
   - Update order status
   - Manage menu items
   - Add special labels

## 🔧 Files Modified

### Frontend

- ✅ `src/services/endpoints.ts` - All API calls now use real backend
- ✅ `src/services/api.ts` - Already had JWT auth configured
- ✅ `src/context/AuthContext.tsx` - Updated User interface
- ✅ `src/features/customer/CartPage.tsx` - Updated order placement format
- ✅ `src/features/restaurant/ManageMenu.tsx` - Updated to use backend fields
- ✅ `.env` - Added API base URL configuration

### Backend

- ✅ `app/routers/auth.py` - Enhanced registration with role validation
- ✅ `app/auth.py` - Fixed bcrypt compatibility
- ✅ `seed.py` - Fixed foreign key constraint ordering
- ✅ All endpoints tested and working

## 🌐 API Endpoints Used

### Auth

- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register (customer or owner)
- `POST /api/auth/reset-password` - Password reset

### Restaurants (Public)

- `GET /api/restaurants` - List restaurants (with filters)
- `GET /api/restaurants/{id}` - Get restaurant + menu
- `GET /api/restaurants/{id}/specials` - Special items
- `GET /api/restaurants/{id}/popular` - Popular items

### Customer (Protected)

- `GET /api/customer/profile` - Get profile
- `PUT /api/customer/profile` - Update profile
- `POST /api/customer/orders` - Place order
- `GET /api/customer/orders` - Order history (searchable)
- `GET /api/customer/preferences` - Get preferences
- `PUT /api/customer/preferences` - Update preferences
- `GET /api/customer/recommendations` - Get recommendations

### Owner (Protected)

- `GET /api/owner/restaurant` - Get restaurant
- `PUT /api/owner/restaurant` - Update restaurant
- `GET /api/owner/menu` - Get menu items
- `POST /api/owner/menu` - Add menu item
- `PUT /api/owner/menu/{id}` - Update menu item
- `DELETE /api/owner/menu/{id}` - Delete menu item
- `GET /api/owner/orders` - Get orders
- `PUT /api/owner/orders/{id}/status` - Update order status
- `GET /api/owner/analytics/popular-items` - Popular items

## ✨ Features Working End-to-End

### Customer Journey

1. ✅ Register/Login
2. ✅ Browse restaurants with filters
3. ✅ View restaurant details and menu
4. ✅ Add items to cart
5. ✅ Place order
6. ✅ Track order status
7. ✅ View order history
8. ✅ Get personalized recommendations
9. ✅ Manage preferences

### Owner Journey

1. ✅ Login as restaurant owner
2. ✅ View restaurant details
3. ✅ Add/Edit/Delete menu items
4. ✅ Mark items as specials
5. ✅ View incoming orders
6. ✅ Update order status
7. ✅ View popular items

## 🔒 Security Features

- ✅ JWT authentication on all protected routes
- ✅ Role-based authorization (customer/owner)
- ✅ Automatic token validation
- ✅ Password hashing with bcrypt
- ✅ CORS configured for frontend
- ✅ Request/response validation
