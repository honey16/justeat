from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database import get_db
from app.schemas import (
    Restaurant, RestaurantCreate, RestaurantUpdate,
    MenuItem, MenuItemCreate, MenuItemUpdate,
    Order, OrderUpdate
)
from app.models import (
    User, Restaurant as RestaurantModel, MenuItem as MenuItemModel,
    Order as OrderModel, OrderItem, OrderStatus
)
from app.dependencies import get_current_owner
from app.logger import get_logger
from app.exceptions import NotFoundException, ForbiddenException
import uuid

router = APIRouter(prefix="/owner", tags=["Restaurant Owner"])
logger = get_logger(__name__)

@router.get("/restaurant", response_model=Restaurant)
async def get_my_restaurant(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get owner's restaurant details"""
    logger.info(f"Fetching restaurant for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == current_user.restaurant_id).first()
    if not restaurant:
        raise NotFoundException("Restaurant not found")
    
    return restaurant

@router.post("/restaurant", response_model=Restaurant, status_code=201)
async def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Create a new restaurant (owner registration)"""
    logger.info(f"Creating restaurant for owner: {current_user.id}")
    
    if current_user.restaurant_id:
        from app.exceptions import BadRequestException
        raise BadRequestException("Owner already has a restaurant")
    
    # Create restaurant
    restaurant_id = f"r{uuid.uuid4().hex[:8]}"
    new_restaurant = RestaurantModel(
        id=restaurant_id,
        name=restaurant_data.name,
        email=restaurant_data.email,
        cuisine=restaurant_data.cuisine,
        price_range=restaurant_data.price_range,
        delivery_time=restaurant_data.delivery_time,
        location=restaurant_data.location,
        description=restaurant_data.description,
        image=restaurant_data.image,
        gradient=restaurant_data.gradient
    )
    
    db.add(new_restaurant)
    
    # Update user's restaurant_id
    current_user.restaurant_id = restaurant_id
    
    db.commit()
    db.refresh(new_restaurant)
    
    logger.info(f"Restaurant created successfully: {restaurant_id}")
    return new_restaurant

@router.put("/restaurant", response_model=Restaurant)
async def update_restaurant(
    restaurant_data: RestaurantUpdate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Update restaurant details"""
    logger.info(f"Updating restaurant for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == current_user.restaurant_id).first()
    if not restaurant:
        raise NotFoundException("Restaurant not found")
    
    # Update fields
    if restaurant_data.name is not None:
        restaurant.name = restaurant_data.name
    if restaurant_data.email is not None:
        restaurant.email = restaurant_data.email
    if restaurant_data.cuisine is not None:
        restaurant.cuisine = restaurant_data.cuisine
    if restaurant_data.price_range is not None:
        restaurant.price_range = restaurant_data.price_range
    if restaurant_data.delivery_time is not None:
        restaurant.delivery_time = restaurant_data.delivery_time
    if restaurant_data.location is not None:
        restaurant.location = restaurant_data.location
    if restaurant_data.description is not None:
        restaurant.description = restaurant_data.description
    if restaurant_data.image is not None:
        restaurant.image = restaurant_data.image
    if restaurant_data.gradient is not None:
        restaurant.gradient = restaurant_data.gradient
    
    db.commit()
    db.refresh(restaurant)
    
    logger.info(f"Restaurant updated successfully: {restaurant.id}")
    return restaurant

@router.get("/menu", response_model=List[MenuItem])
async def get_my_menu(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get all menu items for owner's restaurant"""
    logger.info(f"Fetching menu for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    menu_items = db.query(MenuItemModel).filter(
        MenuItemModel.restaurant_id == current_user.restaurant_id
    ).all()
    
    return menu_items

@router.post("/menu", response_model=MenuItem, status_code=201)
async def add_menu_item(
    item_data: MenuItemCreate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Add a new menu item"""
    logger.info(f"Adding menu item for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    # Verify owner is adding to their own restaurant
    if item_data.restaurant_id != current_user.restaurant_id:
        raise ForbiddenException("Cannot add items to other restaurants")
    
    # Create menu item
    item_id = f"m{uuid.uuid4().hex[:8]}"
    new_item = MenuItemModel(
        id=item_id,
        restaurant_id=item_data.restaurant_id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        category=item_data.category,
        is_special=item_data.is_special,
        special_label=item_data.special_label
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    logger.info(f"Menu item added successfully: {item_id}")
    return new_item

@router.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(
    item_id: str,
    item_data: MenuItemUpdate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Update a menu item"""
    logger.info(f"Updating menu item: {item_id}")
    
    menu_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not menu_item:
        raise NotFoundException(f"Menu item {item_id} not found")
    
    # Verify ownership
    if menu_item.restaurant_id != current_user.restaurant_id:
        raise ForbiddenException("Cannot update items from other restaurants")
    
    # Update fields
    if item_data.name is not None:
        menu_item.name = item_data.name
    if item_data.description is not None:
        menu_item.description = item_data.description
    if item_data.price is not None:
        menu_item.price = item_data.price
    if item_data.category is not None:
        menu_item.category = item_data.category
    if item_data.is_special is not None:
        menu_item.is_special = item_data.is_special
    if item_data.special_label is not None:
        menu_item.special_label = item_data.special_label
    
    db.commit()
    db.refresh(menu_item)
    
    logger.info(f"Menu item updated successfully: {item_id}")
    return menu_item

@router.delete("/menu/{item_id}")
async def delete_menu_item(
    item_id: str,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Delete a menu item"""
    logger.info(f"Deleting menu item: {item_id}")
    
    menu_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not menu_item:
        raise NotFoundException(f"Menu item {item_id} not found")
    
    # Verify ownership
    if menu_item.restaurant_id != current_user.restaurant_id:
        raise ForbiddenException("Cannot delete items from other restaurants")
    
    db.delete(menu_item)
    db.commit()
    
    logger.info(f"Menu item deleted successfully: {item_id}")
    return {"message": "Menu item deleted successfully"}

@router.get("/orders", response_model=List[Order])
async def get_restaurant_orders(
    status: Optional[OrderStatus] = Query(None),
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get all orders for owner's restaurant"""
    logger.info(f"Fetching orders for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    orders_query = db.query(OrderModel).filter(
        OrderModel.restaurant_id == current_user.restaurant_id
    )
    
    if status:
        orders_query = orders_query.filter(OrderModel.status == status)
    
    orders = orders_query.order_by(desc(OrderModel.created_at)).all()
    
    # Format response
    result = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        customer = db.query(User).filter(User.id == order.customer_id).first()
        
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
async def get_order_details(
    order_id: str,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get order details"""
    logger.info(f"Fetching order details: {order_id}")
    
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise NotFoundException(f"Order {order_id} not found")
    
    # Verify ownership
    if order.restaurant_id != current_user.restaurant_id:
        raise ForbiddenException("Cannot view orders from other restaurants")
    
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

@router.put("/orders/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: str,
    status_update: OrderUpdate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Update order status (pending -> preparing -> delivered)"""
    logger.info(f"Updating order status: {order_id} to {status_update.status}")
    
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise NotFoundException(f"Order {order_id} not found")
    
    # Verify ownership
    if order.restaurant_id != current_user.restaurant_id:
        raise ForbiddenException("Cannot update orders from other restaurants")
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    logger.info(f"Order status updated successfully: {order_id}")
    
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

@router.get("/analytics/popular-items", response_model=List[MenuItem])
async def get_popular_items(
    limit: int = Query(10),
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get most ordered items (automatically identified)"""
    logger.info(f"Fetching popular items for owner: {current_user.id}")
    
    if not current_user.restaurant_id:
        raise NotFoundException("No restaurant associated with this owner")
    
    popular_items = db.query(MenuItemModel).filter(
        MenuItemModel.restaurant_id == current_user.restaurant_id
    ).order_by(desc(MenuItemModel.order_count)).limit(limit).all()
    
    return popular_items
