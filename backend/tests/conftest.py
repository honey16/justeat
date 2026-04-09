"""Pytest configuration and fixtures for testing"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import User, Restaurant, MenuItem, Order, OrderItem, UserRole, OrderStatus
from app.auth import get_password_hash
from main import app

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:root@localhost:5432/justeat-test"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_customer(db_session):
    """Create a test customer user"""
    customer = User(
        id="test-customer-1",
        email="testcustomer@test.com",
        hashed_password=get_password_hash("password123"),
        role=UserRole.CUSTOMER,
        name="Test Customer",
        phone="+1234567890",
        address="123 Test Street"
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def test_restaurant(db_session):
    """Create a test restaurant"""
    restaurant = Restaurant(
        id="test-restaurant-1",
        name="Test Restaurant",
        email="test@restaurant.com",
        cuisine="Italian",
        rating=4.5,
        price_range="$$",
        delivery_time="30-45 min",
        location="Test Location",
        description="Test description",
        image="",
        gradient="from-blue-400 to-purple-500"
    )
    db_session.add(restaurant)
    db_session.commit()
    db_session.refresh(restaurant)
    return restaurant


@pytest.fixture
def test_owner(db_session, test_restaurant):
    """Create a test owner user with restaurant"""
    owner = User(
        id="test-owner-1",
        email="testowner@test.com",
        hashed_password=get_password_hash("password123"),
        role=UserRole.OWNER,
        name="Test Owner",
        phone="+1234567890",
        restaurant_id=test_restaurant.id
    )
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner


@pytest.fixture
def test_menu_items(db_session, test_restaurant):
    """Create test menu items"""
    items = [
        MenuItem(
            id="test-item-1",
            restaurant_id=test_restaurant.id,
            name="Test Pizza",
            description="Delicious pizza",
            price=12.99,
            category="Pizza",
            is_special=True,
            special_label="Today's Special",
            order_count=10
        ),
        MenuItem(
            id="test-item-2",
            restaurant_id=test_restaurant.id,
            name="Test Pasta",
            description="Amazing pasta",
            price=15.99,
            category="Pasta",
            is_special=False,
            order_count=5
        )
    ]
    for item in items:
        db_session.add(item)
    db_session.commit()
    for item in items:
        db_session.refresh(item)
    return items


@pytest.fixture
def customer_token(client):
    """Get authentication token for test customer"""
    response = client.post("/api/auth/login", json={
        "email": "testcustomer@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


@pytest.fixture
def owner_token(client):
    """Get authentication token for test owner"""
    response = client.post("/api/auth/login", json={
        "email": "testowner@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_headers_customer(customer_token):
    """Get authorization headers for customer"""
    return {"Authorization": f"Bearer {customer_token}"}


@pytest.fixture
def auth_headers_owner(owner_token):
    """Get authorization headers for owner"""
    return {"Authorization": f"Bearer {owner_token}"}
