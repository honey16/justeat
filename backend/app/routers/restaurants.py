from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.schemas import Restaurant, RestaurantWithMenu, MenuItem, RestaurantSearch
from app.models import Restaurant as RestaurantModel, MenuItem as MenuItemModel
from app.logger import get_logger

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
logger = get_logger(__name__)

@router.get("", response_model=List[Restaurant])
async def get_restaurants(
    location: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    price_range: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all restaurants with optional filters.
    Customers can search and filter restaurants.
    """
    logger.info(f"Fetching restaurants - location: {location}, cuisine: {cuisine}, query: {query}")
    
    restaurants = db.query(RestaurantModel)
    
    # Apply filters
    if location and location != "All Locations":
        restaurants = restaurants.filter(RestaurantModel.location == location)
    
    if cuisine:
        restaurants = restaurants.filter(RestaurantModel.cuisine == cuisine)
    
    if price_range:
        restaurants = restaurants.filter(RestaurantModel.price_range == price_range)
    
    if query:
        restaurants = restaurants.filter(
            or_(
                RestaurantModel.name.ilike(f"%{query}%"),
                RestaurantModel.cuisine.ilike(f"%{query}%"),
                RestaurantModel.description.ilike(f"%{query}%")
            )
        )
    
    results = restaurants.all()
    logger.info(f"Found {len(results)} restaurants")
    
    return results

@router.get("/{restaurant_id}", response_model=RestaurantWithMenu)
async def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    """Get a specific restaurant with its menu"""
    logger.info(f"Fetching restaurant: {restaurant_id}")
    
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if not restaurant:
        from app.exceptions import NotFoundException
        raise NotFoundException(f"Restaurant {restaurant_id} not found")
    
    # Get menu items
    menu_items = db.query(MenuItemModel).filter(MenuItemModel.restaurant_id == restaurant_id).all()
    
    # Convert to response model
    restaurant_dict = {
        **restaurant.__dict__,
        "menu": menu_items
    }
    
    return restaurant_dict

@router.get("/{restaurant_id}/menu", response_model=List[MenuItem])
async def get_restaurant_menu(
    restaurant_id: str,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get menu items for a restaurant with optional category filter"""
    logger.info(f"Fetching menu for restaurant: {restaurant_id}, category: {category}")
    
    query = db.query(MenuItemModel).filter(MenuItemModel.restaurant_id == restaurant_id)
    
    if category:
        query = query.filter(MenuItemModel.category == category)
    
    menu_items = query.all()
    logger.info(f"Found {len(menu_items)} menu items")
    
    return menu_items

@router.get("/{restaurant_id}/specials", response_model=List[MenuItem])
async def get_restaurant_specials(restaurant_id: str, db: Session = Depends(get_db)):
    """Get special menu items for a restaurant"""
    logger.info(f"Fetching specials for restaurant: {restaurant_id}")
    
    specials = db.query(MenuItemModel).filter(
        MenuItemModel.restaurant_id == restaurant_id,
        MenuItemModel.is_special == True
    ).all()
    
    return specials

@router.get("/{restaurant_id}/popular", response_model=List[MenuItem])
async def get_popular_items(restaurant_id: str, limit: int = Query(5), db: Session = Depends(get_db)):
    """Get most ordered items for a restaurant"""
    logger.info(f"Fetching popular items for restaurant: {restaurant_id}")
    
    popular_items = db.query(MenuItemModel).filter(
        MenuItemModel.restaurant_id == restaurant_id
    ).order_by(MenuItemModel.order_count.desc()).limit(limit).all()
    
    return popular_items
