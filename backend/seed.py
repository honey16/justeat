from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Restaurant, MenuItem, Order, OrderItem, UserPreference, UserRole, OrderStatus
from app.auth import get_password_hash
import uuid
from datetime import datetime, timedelta

def drop_all_tables():
    """Drop all tables"""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully!")

def create_all_tables():
    """Create all tables"""
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*50)
        print("Starting database seeding...")
        print("="*50 + "\n")
        
        # Create restaurants first (before users with restaurant_id foreign key)
        print("Creating restaurants...")
        restaurants_data = [
            {"id": "r1", "name": "The Golden Fork", "email": "contact@goldenfork.com", "cuisine": "Italian", "rating": 4.8, 
             "price_range": "$$", "delivery_time": "25–35 min", "location": "Hauz Khas",
             "description": "Authentic Italian cuisine crafted with imported ingredients and generations of tradition.",
             "gradient": "from-amber-400 to-orange-500"},
            {"id": "r2", "name": "Sakura House", "email": "info@sakurahouse.com", "cuisine": "Japanese", "rating": 4.9,
             "price_range": "$$$", "delivery_time": "30–45 min", "location": "Defence Colony",
             "description": "Omakase-inspired dishes with the freshest seasonal fish flown in daily.",
             "gradient": "from-rose-400 to-pink-500"},
            {"id": "r3", "name": "Spice Route", "email": "hello@spiceroute.com", "cuisine": "Indian", "rating": 4.6,
             "price_range": "$$", "delivery_time": "20–30 min", "location": "INA",
             "description": "Bold, aromatic flavors from across the Indian subcontinent.",
             "gradient": "from-yellow-500 to-red-500"},
            {"id": "r4", "name": "Le Petit Bistro", "email": "contact@lepetitbistro.com", "cuisine": "French", "rating": 4.7,
             "price_range": "$$$", "delivery_time": "35–50 min", "location": "Connaught Place",
             "description": "Classic French bistro fare with a contemporary twist.",
             "gradient": "from-blue-400 to-indigo-500"},
            {"id": "r5", "name": "Verde Kitchen", "email": "orders@verdekitchen.com", "cuisine": "Mexican", "rating": 4.5,
             "price_range": "$", "delivery_time": "15–25 min", "location": "Rohini",
             "description": "Fresh, vibrant Mexican street food elevated to an art form.",
             "gradient": "from-green-400 to-emerald-500"},
            {"id": "r6", "name": "Seoul Station", "email": "info@seoulstation.com", "cuisine": "Korean", "rating": 4.7,
             "price_range": "$$", "delivery_time": "25–40 min", "location": "Saket",
             "description": "Modern Korean cuisine blending tradition with innovation.",
             "gradient": "from-violet-400 to-purple-500"},
            {"id": "r7", "name": "The Smokehouse", "email": "bbq@smokehouse.com", "cuisine": "American BBQ", "rating": 4.4,
             "price_range": "$$", "delivery_time": "30–45 min", "location": "Lajpat Nagar",
             "description": "Low and slow smoked meats with house-made sauces.",
             "gradient": "from-orange-500 to-red-600"},
            {"id": "r8", "name": "Olive & Thyme", "email": "contact@oliveandthyme.com", "cuisine": "Mediterranean", "rating": 4.6,
             "price_range": "$$", "delivery_time": "20–35 min", "location": "Karol Bagh",
             "description": "Sun-kissed Mediterranean flavors from farm to table.",
             "gradient": "from-teal-400 to-cyan-500"},
        ]
        
        for rest_data in restaurants_data:
            restaurant = Restaurant(**rest_data)
            db.add(restaurant)
            print(f"  ✓ Created restaurant: {restaurant.name} ({restaurant.cuisine})")
        
        db.commit()
        
        # Create menu items
        print("\nCreating menu items...")
        menu_items_data = [
            # The Golden Fork (Italian)
            {"id": "m1", "restaurant_id": "r1", "name": "Margherita Pizza", 
             "description": "San Marzano tomatoes, fresh mozzarella, basil", "price": 14.99, 
             "category": "Pizza", "is_special": True, "special_label": "Today's Special", "order_count": 45},
            {"id": "m2", "restaurant_id": "r1", "name": "Truffle Risotto",
             "description": "Arborio rice, black truffle, parmigiano", "price": 22.99,
             "category": "Mains", "order_count": 32},
            {"id": "m3", "restaurant_id": "r1", "name": "Burrata Salad",
             "description": "Creamy burrata, heirloom tomatoes, olive oil", "price": 16.50,
             "category": "Starters", "order_count": 28},
            {"id": "m4", "restaurant_id": "r1", "name": "Tiramisu",
             "description": "Mascarpone, espresso-soaked ladyfingers, cocoa", "price": 11.99,
             "category": "Desserts", "is_special": True, "special_label": "Deal of the Day", "order_count": 38},
            {"id": "m5", "restaurant_id": "r1", "name": "Penne Arrabbiata",
             "description": "Spicy tomato sauce, garlic, chili flakes", "price": 13.50,
             "category": "Pasta", "order_count": 25},
            
            # Sakura House (Japanese)
            {"id": "m6", "restaurant_id": "r2", "name": "Salmon Sashimi",
             "description": "12 pieces of premium Atlantic salmon", "price": 24.99,
             "category": "Sashimi", "is_special": True, "special_label": "Today's Special", "order_count": 42},
            {"id": "m7", "restaurant_id": "r2", "name": "Dragon Roll",
             "description": "Eel, avocado, cucumber, tobiko", "price": 18.99,
             "category": "Rolls", "order_count": 35},
            {"id": "m8", "restaurant_id": "r2", "name": "Miso Ramen",
             "description": "Rich miso broth, chashu pork, ajitama egg", "price": 16.99,
             "category": "Noodles", "order_count": 40},
            {"id": "m9", "restaurant_id": "r2", "name": "Matcha Mochi",
             "description": "Handmade mochi with ceremonial matcha", "price": 9.99,
             "category": "Desserts", "is_special": True, "special_label": "Deal of the Day", "order_count": 30},
            
            # Spice Route (Indian)
            {"id": "m10", "restaurant_id": "r3", "name": "Butter Chicken",
             "description": "Tandoori chicken in creamy tomato-butter sauce", "price": 17.99,
             "category": "Mains", "is_special": True, "special_label": "Today's Special", "order_count": 55},
            {"id": "m11", "restaurant_id": "r3", "name": "Garlic Naan",
             "description": "Wood-fired flatbread with roasted garlic", "price": 4.99,
             "category": "Breads", "order_count": 60},
            {"id": "m12", "restaurant_id": "r3", "name": "Lamb Biryani",
             "description": "Basmati rice layered with spiced lamb, saffron", "price": 19.99,
             "category": "Rice", "order_count": 48},
            {"id": "m13", "restaurant_id": "r3", "name": "Mango Lassi",
             "description": "Chilled yogurt smoothie with Alphonso mango", "price": 5.99,
             "category": "Drinks", "order_count": 35},
            {"id": "m14", "restaurant_id": "r3", "name": "Paneer Tikka",
             "description": "Marinated cottage cheese, tandoor-grilled", "price": 14.50,
             "category": "Starters", "is_special": True, "special_label": "Deal of the Day", "order_count": 40},
            
            # Le Petit Bistro (French)
            {"id": "m15", "restaurant_id": "r4", "name": "Coq au Vin",
             "description": "Braised chicken, red wine, pearl onions, mushrooms", "price": 26.99,
             "category": "Mains", "is_special": True, "special_label": "Today's Special", "order_count": 30},
            {"id": "m16", "restaurant_id": "r4", "name": "French Onion Soup",
             "description": "Caramelized onions, gruyère crouton", "price": 12.99,
             "category": "Starters", "order_count": 25},
            {"id": "m17", "restaurant_id": "r4", "name": "Crème Brûlée",
             "description": "Vanilla custard, caramelized sugar crust", "price": 10.99,
             "category": "Desserts", "is_special": True, "special_label": "Deal of the Day", "order_count": 35},
            {"id": "m18", "restaurant_id": "r4", "name": "Duck Confit",
             "description": "Slow-cooked duck leg, crispy skin, lentils", "price": 28.50,
             "category": "Mains", "order_count": 28},
            
            # Verde Kitchen (Mexican)
            {"id": "m19", "restaurant_id": "r5", "name": "Carnitas Tacos",
             "description": "Slow-roasted pork, salsa verde, cilantro, onion", "price": 12.99,
             "category": "Tacos", "is_special": True, "special_label": "Today's Special", "order_count": 50},
            {"id": "m20", "restaurant_id": "r5", "name": "Guacamole & Chips",
             "description": "Tableside guacamole, hand-cut tortilla chips", "price": 9.99,
             "category": "Starters", "order_count": 45},
            {"id": "m21", "restaurant_id": "r5", "name": "Chicken Burrito Bowl",
             "description": "Grilled chicken, rice, beans, pico de gallo", "price": 14.50,
             "category": "Bowls", "order_count": 42},
            {"id": "m22", "restaurant_id": "r5", "name": "Churros",
             "description": "Cinnamon sugar, chocolate dipping sauce", "price": 7.99,
             "category": "Desserts", "is_special": True, "special_label": "Deal of the Day", "order_count": 38},
            
            # Seoul Station (Korean)
            {"id": "m23", "restaurant_id": "r6", "name": "Korean Fried Chicken",
             "description": "Double-fried, gochujang glaze, pickled radish", "price": 16.99,
             "category": "Mains", "is_special": True, "special_label": "Today's Special", "order_count": 47},
            {"id": "m24", "restaurant_id": "r6", "name": "Bibimbap",
             "description": "Stone pot rice, vegetables, gochujang, fried egg", "price": 15.99,
             "category": "Rice", "order_count": 40},
            {"id": "m25", "restaurant_id": "r6", "name": "Kimchi Jjigae",
             "description": "Fermented kimchi stew, tofu, pork belly", "price": 14.99,
             "category": "Soups", "order_count": 35},
            {"id": "m26", "restaurant_id": "r6", "name": "Tteokbokki",
             "description": "Spicy rice cakes, fish cakes, scallions", "price": 11.99,
             "category": "Snacks", "is_special": True, "special_label": "Deal of the Day", "order_count": 33},
            
            # The Smokehouse (American BBQ)
            {"id": "m27", "restaurant_id": "r7", "name": "Brisket Platter",
             "description": "14hr smoked brisket, coleslaw, cornbread", "price": 24.99,
             "category": "Platters", "is_special": True, "special_label": "Today's Special", "order_count": 38},
            {"id": "m28", "restaurant_id": "r7", "name": "Pulled Pork Sandwich",
             "description": "Smoked pork, tangy BBQ sauce, brioche bun", "price": 15.99,
             "category": "Sandwiches", "order_count": 35},
            {"id": "m29", "restaurant_id": "r7", "name": "Mac & Cheese",
             "description": "Four-cheese blend, breadcrumb crust", "price": 9.99,
             "category": "Sides", "order_count": 40},
            {"id": "m30", "restaurant_id": "r7", "name": "Smoked Wings",
             "description": "Dry-rubbed, smoked, served with ranch", "price": 13.99,
             "category": "Starters", "is_special": True, "special_label": "Deal of the Day", "order_count": 32},
            
            # Olive & Thyme (Mediterranean)
            {"id": "m31", "restaurant_id": "r8", "name": "Grilled Halloumi Bowl",
             "description": "Halloumi, quinoa, roasted vegetables, tahini", "price": 16.99,
             "category": "Bowls", "is_special": True, "special_label": "Today's Special", "order_count": 30},
            {"id": "m32", "restaurant_id": "r8", "name": "Lamb Kofta",
             "description": "Spiced lamb, tzatziki, warm pita", "price": 18.99,
             "category": "Mains", "order_count": 28},
            {"id": "m33", "restaurant_id": "r8", "name": "Hummus Trio",
             "description": "Classic, roasted red pepper, herb", "price": 11.99,
             "category": "Starters", "order_count": 35},
            {"id": "m34", "restaurant_id": "r8", "name": "Baklava",
             "description": "Phyllo, pistachios, honey syrup", "price": 8.99,
             "category": "Desserts", "is_special": True, "special_label": "Deal of the Day", "order_count": 25},
        ]
        
        for item_data in menu_items_data:
            menu_item = MenuItem(**item_data)
            db.add(menu_item)
        
        print(f"  ✓ Created {len(menu_items_data)} menu items")
        db.commit()
        
        # Create users (after restaurants exist)
        print("\nCreating users...")
        users_data = [
            {"id": "u1", "email": "customer@test.com", "password": "123456", "role": UserRole.CUSTOMER, 
             "name": "Alex Morgan", "phone": "+1 555-0123", "address": "42 Elm Street, Brooklyn, NY"},
            {"id": "u2", "email": "owner@test.com", "password": "123456", "role": UserRole.OWNER, 
             "name": "Sam Rivera", "restaurant_id": "r1"},
            {"id": "u3", "email": "customer2@test.com", "password": "123456", "role": UserRole.CUSTOMER,
             "name": "Jordan Lee", "phone": "+1 555-0124", "address": "15 Oak Avenue, Manhattan, NY"},
            {"id": "u4", "email": "owner2@test.com", "password": "123456", "role": UserRole.OWNER,
             "name": "Maria Garcia", "restaurant_id": "r2"},
        ]
        
        for user_data in users_data:
            password = user_data.pop("password")
            user = User(**user_data, hashed_password=get_password_hash(password))
            db.add(user)
            print(f"  ✓ Created user: {user.email} ({user.role.value})")
        
        db.commit()
        
        # Create user preferences for customers
        print("\nCreating user preferences...")
        preferences_data = [
            {"user_id": "u1", "favorite_restaurants": '["r1", "r2"]', 
             "favorite_cuisines": '["Italian", "Japanese"]', "dietary_restrictions": '[]'},
            {"user_id": "u3", "favorite_restaurants": '["r3"]', 
             "favorite_cuisines": '["Indian"]', "dietary_restrictions": '["Vegetarian"]'},
        ]
        
        for pref_data in preferences_data:
            preference = UserPreference(**pref_data)
            db.add(preference)
            print(f"  ✓ Created preferences for user: {pref_data['user_id']}")
        
        db.commit()
        
        # Create sample orders
        print("\nCreating sample orders...")
        orders_data = [
            {"id": "o1", "customer_id": "u1", "restaurant_id": "r1", "restaurant_name": "The Golden Fork",
             "status": OrderStatus.DELIVERED, "total": 41.97, 
             "created_at": datetime.utcnow() - timedelta(days=6),
             "items": [{"menu_item_id": "m1", "quantity": 2}, {"menu_item_id": "m4", "quantity": 1}]},
            {"id": "o2", "customer_id": "u1", "restaurant_id": "r2", "restaurant_name": "Sakura House",
             "status": OrderStatus.PREPARING, "total": 43.98,
             "created_at": datetime.utcnow() - timedelta(days=3),
             "items": [{"menu_item_id": "m6", "quantity": 1}, {"menu_item_id": "m7", "quantity": 1}]},
            {"id": "o3", "customer_id": "u1", "restaurant_id": "r3", "restaurant_name": "Spice Route",
             "status": OrderStatus.PENDING, "total": 32.96,
             "created_at": datetime.utcnow() - timedelta(hours=2),
             "items": [{"menu_item_id": "m10", "quantity": 1}, {"menu_item_id": "m11", "quantity": 3}]},
            {"id": "o4", "customer_id": "u3", "restaurant_id": "r1", "restaurant_name": "The Golden Fork",
             "status": OrderStatus.DELIVERED, "total": 50.98,
             "created_at": datetime.utcnow() - timedelta(days=5),
             "items": [{"menu_item_id": "m2", "quantity": 1}, {"menu_item_id": "m5", "quantity": 2}]},
        ]
        
        for order_data in orders_data:
            items_data = order_data.pop("items")
            order = Order(**order_data)
            db.add(order)
            
            for item_info in items_data:
                menu_item = db.query(MenuItem).filter(MenuItem.id == item_info["menu_item_id"]).first()
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=item_info["menu_item_id"],
                    name=menu_item.name,
                    price=menu_item.price,
                    quantity=item_info["quantity"]
                )
                db.add(order_item)
        
        print(f"  ✓ Created {len(orders_data)} sample orders")
        db.commit()
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nTest Credentials:")
        print("-" * 50)
        print("Customer Login:")
        print("  Email: customer@test.com")
        print("  Password: 123456")
        print("\nRestaurant Owner Login:")
        print("  Email: owner@test.com")
        print("  Password: 123456")
        print("  Restaurant: The Golden Fork")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        drop_all_tables()
    
    create_all_tables()
    seed_database()
