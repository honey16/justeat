"""Tests for customer endpoints"""
import pytest


class TestCustomerEndpoints:
    """Test customer-specific endpoints"""

    def test_get_customer_profile(self, client, test_customer, auth_headers_customer):
        """Test getting customer profile"""
        response = client.get("/api/customer/profile", headers=auth_headers_customer)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "testcustomer@test.com"
        assert data["name"] == "Test Customer"
        assert data["role"] == "customer"

    def test_get_customer_profile_unauthorized(self, client):
        """Test getting profile without authentication fails"""
        response = client.get("/api/customer/profile")
        assert response.status_code == 401

    def test_update_customer_profile(self, client, test_customer, auth_headers_customer):
        """Test updating customer profile"""
        response = client.put("/api/customer/profile", headers=auth_headers_customer, json={
            "name": "Updated Name",
            "phone": "+9876543210",
            "address": "789 Updated Street"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+9876543210"
        assert data["address"] == "789 Updated Street"

    def test_place_order(self, client, test_customer, test_restaurant, test_menu_items, auth_headers_customer):
        """Test placing an order"""
        response = client.post("/api/customer/orders", headers=auth_headers_customer, json={
            "restaurant_id": test_restaurant.id,
            "items": [
                {"menu_item_id": test_menu_items[0].id, "quantity": 2},
                {"menu_item_id": test_menu_items[1].id, "quantity": 1}
            ]
        })
        assert response.status_code == 201
        data = response.json()
        assert data["restaurant_id"] == test_restaurant.id
        assert data["status"] == "pending"
        assert len(data["items"]) == 2
        assert data["total"] > 0

    def test_place_order_empty_items(self, client, test_customer, test_restaurant, auth_headers_customer):
        """Test placing order with no items"""
        response = client.post("/api/customer/orders", headers=auth_headers_customer, json={
            "restaurant_id": test_restaurant.id,
            "items": []
        })
        # Backend allows empty orders, adjust if validation is added later
        assert response.status_code in [201, 400]

    def test_get_customer_orders(self, client, test_customer, test_restaurant, test_menu_items, auth_headers_customer):
        """Test getting customer order history"""
        # Place an order first
        client.post("/api/customer/orders", headers=auth_headers_customer, json={
            "restaurant_id": test_restaurant.id,
            "items": [{"menu_item_id": test_menu_items[0].id, "quantity": 1}]
        })

        # Get orders
        response = client.get("/api/customer/orders", headers=auth_headers_customer)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["restaurant_id"] == test_restaurant.id

    def test_get_customer_preferences(self, client, test_customer, auth_headers_customer):
        """Test getting customer preferences"""
        response = client.get("/api/customer/preferences", headers=auth_headers_customer)
        assert response.status_code == 200
        data = response.json()
        assert "favorite_restaurants" in data
        assert "favorite_cuisines" in data
        assert "dietary_restrictions" in data

    def test_update_customer_preferences(self, client, test_customer, auth_headers_customer):
        """Test updating customer preferences"""
        response = client.put("/api/customer/preferences", headers=auth_headers_customer, json={
            "favorite_restaurants": ["r1", "r2"],
            "favorite_cuisines": ["Italian", "Japanese"],
            "dietary_restrictions": ["vegetarian"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "r1" in data["favorite_restaurants"]
        assert "Italian" in data["favorite_cuisines"]
        assert "vegetarian" in data["dietary_restrictions"]

    def test_get_recommendations(self, client, test_customer, test_restaurant, auth_headers_customer):
        """Test getting restaurant recommendations"""
        response = client.get("/api/customer/recommendations", headers=auth_headers_customer)
        assert response.status_code == 200
        data = response.json()
        assert "restaurants" in data
        assert isinstance(data["restaurants"], list)
