"""Tests for database models"""
import pytest
from app.models import User, Restaurant, MenuItem, Order, OrderItem, UserRole, OrderStatus
from app.auth import get_password_hash, verify_password


class TestUserModel:
    """Test User model"""

    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            id="test-user",
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            role=UserRole.CUSTOMER,
            name="Test User",
            phone="+1234567890",
            address="123 Test St"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id == "test-user"
        assert user.email == "test@example.com"
        assert user.role == UserRole.CUSTOMER
        assert verify_password("password", user.hashed_password)

    def test_user_unique_email(self, db_session):
        """Test user email must be unique"""
        user1 = User(
            id="user1",
            email="same@example.com",
            hashed_password=get_password_hash("password"),
            role=UserRole.CUSTOMER,
            name="User One"
        )
        user2 = User(
            id="user2",
            email="same@example.com",
            hashed_password=get_password_hash("password"),
            role=UserRole.CUSTOMER,
            name="User Two"
        )
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestRestaurantModel:
    """Test Restaurant model"""

    def test_create_restaurant(self, db_session):
        """Test creating a restaurant"""
        restaurant = Restaurant(
            id="rest-1",
            name="Test Restaurant",
            email="contact@test.com",
            cuisine="Italian",
            rating=4.5,
            price_range="$$",
            delivery_time="30-40 min",
            location="Downtown",
            description="Great food",
            gradient="from-blue-500 to-purple-500"
        )
        db_session.add(restaurant)
        db_session.commit()
        db_session.refresh(restaurant)

        assert restaurant.name == "Test Restaurant"
        assert restaurant.email == "contact@test.com"
        assert restaurant.rating == 4.5


class TestMenuItemModel:
    """Test MenuItem model"""

    def test_create_menu_item(self, db_session, test_restaurant):
        """Test creating a menu item"""
        item = MenuItem(
            id="item-1",
            restaurant_id=test_restaurant.id,
            name="Margherita Pizza",
            description="Classic pizza",
            price=12.99,
            category="Pizza",
            is_special=True,
            special_label="Chef's Special",
            order_count=0
        )
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)

        assert item.name == "Margherita Pizza"
        assert item.price == 12.99
        assert item.is_special is True
        assert item.restaurant_id == test_restaurant.id


class TestOrderModel:
    """Test Order model"""

    def test_create_order(self, db_session, test_customer, test_restaurant):
        """Test creating an order"""
        order = Order(
            id="order-1",
            customer_id=test_customer.id,
            restaurant_id=test_restaurant.id,
            restaurant_name=test_restaurant.name,
            status=OrderStatus.PENDING,
            total=25.98
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        assert order.customer_id == test_customer.id
        assert order.restaurant_id == test_restaurant.id
        assert order.status == OrderStatus.PENDING
        assert order.total == 25.98

    def test_order_with_items(self, db_session, test_customer, test_restaurant, test_menu_items):
        """Test creating order with order items"""
        order = Order(
            id="order-2",
            customer_id=test_customer.id,
            restaurant_id=test_restaurant.id,
            restaurant_name=test_restaurant.name,
            status=OrderStatus.PENDING,
            total=28.98
        )
        db_session.add(order)
        db_session.commit()

        # Add order items
        item1 = OrderItem(
            order_id=order.id,
            menu_item_id=test_menu_items[0].id,
            name=test_menu_items[0].name,
            price=test_menu_items[0].price,
            quantity=2
        )
        db_session.add(item1)
        db_session.commit()
        db_session.refresh(order)

        assert len(order.items) == 1
        assert order.items[0].quantity == 2
