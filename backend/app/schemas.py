from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, OrderStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str
    restaurant_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class PasswordReset(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

class User(UserBase):
    id: str
    restaurant_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Restaurant Schemas
class RestaurantBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    cuisine: str
    price_range: str
    delivery_time: str
    location: str
    description: Optional[str] = None
    image: Optional[str] = ""
    gradient: Optional[str] = ""

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cuisine: Optional[str] = None
    price_range: Optional[str] = None
    delivery_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    gradient: Optional[str] = None

class Restaurant(RestaurantBase):
    id: str
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True

# MenuItem Schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_special: bool = False
    special_label: str = ""

class MenuItemCreate(MenuItemBase):
    restaurant_id: str

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_special: Optional[bool] = None
    special_label: Optional[str] = None

class MenuItem(MenuItemBase):
    id: str
    restaurant_id: str
    order_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class RestaurantWithMenu(Restaurant):
    menu: List[MenuItem] = []

# Order Item Schemas
class OrderItemBase(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: int

class OrderItem(OrderItemBase):
    class Config:
        from_attributes = True

# Order Schemas
class OrderCreate(BaseModel):
    restaurant_id: str
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatus

class Order(BaseModel):
    id: str
    customer_id: str
    restaurant_id: str
    restaurant_name: str
    status: OrderStatus
    total: float
    items: List[OrderItemBase]
    created_at: datetime

    class Config:
        from_attributes = True

# User Preferences Schemas
class UserPreferenceBase(BaseModel):
    favorite_restaurants: List[str] = []
    favorite_cuisines: List[str] = []
    dietary_restrictions: List[str] = []

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: str

    class Config:
        from_attributes = True

# Search and Filter Schemas
class RestaurantSearch(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    cuisine: Optional[str] = None
    price_range: Optional[str] = None

class OrderSearch(BaseModel):
    query: Optional[str] = None
    status: Optional[OrderStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# Recommendation Schema
class Recommendation(BaseModel):
    restaurants: List[Restaurant]
    reason: str
