from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.schemas import (
    Order, OrderCreate, User as UserSchema, UserUpdate,
    UserPreference, UserPreferenceUpdate, Recommendation, Restaurant
)
from app.models import (
    User, Order as OrderModel, OrderItem, MenuItem, Restaurant as RestaurantModel,
    UserPreference as UserPreferenceModel, OrderStatus
)
from app.dependencies import get_current_customer
from app.logger import get_logger
from app.exceptions import NotFoundException, BadRequestException
import uuid
import json

router = APIRouter(prefix="/customer", tags=["Customer"])
logger = get_logger(__name__)

@router.get("/profile", response_model=UserSchema)
async def get_profile(current_user: User = Depends(get_current_customer)):
    """Get customer profile"""
    logger.info(f"Fetching profile for user: {current_user.id}")
    return current_user

@router.put("/profile", response_model=UserSchema)
async def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Update customer profile"""
    logger.info(f"Updating profile for user: {current_user.id}")
    
    if profile_data.name is not None:
        current_user.name = profile_data.name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.address is not None:
        current_user.address = profile_data.address
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"Profile updated successfully for user: {current_user.id}")
    return current_user

@router.post("/orders", response_model=Order, status_code=201)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Create a new order"""
    logger.info(f"Creating order for user: {current_user.id}, restaurant: {order_data.restaurant_id}")
    
    # Validate restaurant
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == order_data.restaurant_id).first()
    if not restaurant:
        raise NotFoundException(f"Restaurant {order_data.restaurant_id} not found")
    
    # Calculate total and validate items
    total = 0.0
    order_items = []
    
    for item_data in order_data.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
        if not menu_item:
            raise NotFoundException(f"Menu item {item_data.menu_item_id} not found")
        
        if menu_item.restaurant_id != order_data.restaurant_id:
            raise BadRequestException("All items must be from the same restaurant")
        
        item_total = menu_item.price * item_data.quantity
        total += item_total
        
        order_items.append({
            "menu_item_id": menu_item.id,
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": item_data.quantity
        })
        
        # Update order count for menu item
        menu_item.order_count += item_data.quantity
    
    # Create order
    order_id = f"o{uuid.uuid4().hex[:8]}"
    new_order = OrderModel(
        id=order_id,
        customer_id=current_user.id,
        restaurant_id=order_data.restaurant_id,
        restaurant_name=restaurant.name,
        total=total,
        status=OrderStatus.PENDING
    )
    
    db.add(new_order)
    
    # Create order items
    for item in order_items:
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=item["menu_item_id"],
            name=item["name"],
            price=item["price"],
            quantity=item["quantity"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    logger.info(f"Order created successfully: {order_id}")
    
    # Format response
    response_items = [
        {"id": item["menu_item_id"], "name": item["name"], "price": item["price"], "quantity": item["quantity"]}
        for item in order_items
    ]
    
    return Order(
        id=new_order.id,
        customer_id=new_order.customer_id,
        restaurant_id=new_order.restaurant_id,
        restaurant_name=new_order.restaurant_name,
        status=new_order.status,
        total=new_order.total,
        items=response_items,
        created_at=new_order.created_at
    )

@router.get("/orders", response_model=List[Order])
async def get_orders(
    status: Optional[OrderStatus] = Query(None),
    query: Optional[str] = Query(None),
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get customer's order history with optional search and filter"""
    logger.info(f"Fetching orders for user: {current_user.id}")
    
    orders_query = db.query(OrderModel).filter(OrderModel.customer_id == current_user.id)
    
    # Apply filters
    if status:
        orders_query = orders_query.filter(OrderModel.status == status)
    
    if query:
        orders_query = orders_query.filter(
            or_(
                OrderModel.restaurant_name.ilike(f"%{query}%"),
                OrderModel.id.ilike(f"%{query}%")
            )
        )
    
    orders = orders_query.order_by(desc(OrderModel.created_at)).all()
    
    # Format response
    result = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        result.append(Order(
            id=order.id,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            restaurant_name=order.restaurant_name,
            status=order.status,
            total=order.total,
            items=[{"id": item.menu_item_id, "name": item.name, "price": item.price, "quantity": item.quantity} for item in items],
            created_at=order.created_at
        ))
    
    logger.info(f"Found {len(result)} orders")
    return result

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get a specific order"""
    logger.info(f"Fetching order: {order_id}")
    
    order = db.query(OrderModel).filter(
        OrderModel.id == order_id,
        OrderModel.customer_id == current_user.id
    ).first()
    
    if not order:
        raise NotFoundException(f"Order {order_id} not found")
    
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return Order(
        id=order.id,
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        restaurant_name=order.restaurant_name,
        status=order.status,
        total=order.total,
        items=[{"id": item.menu_item_id, "name": item.name, "price": item.price, "quantity": item.quantity} for item in items],
        created_at=order.created_at
    )

@router.get("/preferences", response_model=UserPreference)
async def get_preferences(
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get customer preferences"""
    logger.info(f"Fetching preferences for user: {current_user.id}")
    
    preference = db.query(UserPreferenceModel).filter(UserPreferenceModel.user_id == current_user.id).first()
    if not preference:
        # Create default preferences
        preference = UserPreferenceModel(user_id=current_user.id)
        db.add(preference)
        db.commit()
        db.refresh(preference)
    
    return UserPreference(
        id=preference.id,
        user_id=preference.user_id,
        favorite_restaurants=json.loads(preference.favorite_restaurants),
        favorite_cuisines=json.loads(preference.favorite_cuisines),
        dietary_restrictions=json.loads(preference.dietary_restrictions)
    )

@router.put("/preferences", response_model=UserPreference)
async def update_preferences(
    preference_data: UserPreferenceUpdate,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Update customer preferences"""
    logger.info(f"Updating preferences for user: {current_user.id}")
    
    preference = db.query(UserPreferenceModel).filter(UserPreferenceModel.user_id == current_user.id).first()
    if not preference:
        preference = UserPreferenceModel(user_id=current_user.id)
        db.add(preference)
    
    preference.favorite_restaurants = json.dumps(preference_data.favorite_restaurants)
    preference.favorite_cuisines = json.dumps(preference_data.favorite_cuisines)
    preference.dietary_restrictions = json.dumps(preference_data.dietary_restrictions)
    
    db.commit()
    db.refresh(preference)
    
    logger.info(f"Preferences updated for user: {current_user.id}")
    
    return UserPreference(
        id=preference.id,
        user_id=preference.user_id,
        favorite_restaurants=json.loads(preference.favorite_restaurants),
        favorite_cuisines=json.loads(preference.favorite_cuisines),
        dietary_restrictions=json.loads(preference.dietary_restrictions)
    )

@router.get("/recommendations", response_model=Recommendation)
async def get_recommendations(
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get personalized restaurant recommendations based on order history and preferences"""
    logger.info(f"Generating recommendations for user: {current_user.id}")
    
    # Get user preferences
    preference = db.query(UserPreferenceModel).filter(UserPreferenceModel.user_id == current_user.id).first()
    favorite_cuisines = json.loads(preference.favorite_cuisines) if preference else []
    favorite_restaurants = json.loads(preference.favorite_restaurants) if preference else []
    
    # Get order history to find frequently ordered cuisines
    orders = db.query(OrderModel).filter(OrderModel.customer_id == current_user.id).all()
    restaurant_ids = [order.restaurant_id for order in orders]
    
    cuisine_count = {}
    for rid in restaurant_ids:
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == rid).first()
        if restaurant:
            cuisine_count[restaurant.cuisine] = cuisine_count.get(restaurant.cuisine, 0) + 1
    
    # Combine preferences and order history
    recommended_cuisines = list(set(favorite_cuisines + list(cuisine_count.keys())))
    
    # Get recommendations
    recommendations = []
    reason = "Based on your order history and preferences"
    
    if recommended_cuisines:
        recommendations = db.query(RestaurantModel).filter(
            RestaurantModel.cuisine.in_(recommended_cuisines)
        ).limit(5).all()
    
    if not recommendations:
        # Fallback to top-rated restaurants
        recommendations = db.query(RestaurantModel).order_by(desc(RestaurantModel.rating)).limit(5).all()
        reason = "Top-rated restaurants for you"
    
    logger.info(f"Generated {len(recommendations)} recommendations")
    
    return Recommendation(
        restaurants=recommendations,
        reason=reason
    )
