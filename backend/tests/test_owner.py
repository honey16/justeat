"""Tests for restaurant owner endpoints"""
import pytest


class TestOwnerEndpoints:
    """Test restaurant owner-specific endpoints"""

    def test_get_owner_restaurant(self, client, test_owner, test_restaurant, auth_headers_owner):
        """Test getting owner's restaurant details"""
        response = client.get("/api/owner/restaurant", headers=auth_headers_owner)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_restaurant.id
        assert data["name"] == "Test Restaurant"

    def test_get_owner_restaurant_unauthorized(self, client):
        """Test getting restaurant without authentication fails"""
        response = client.get("/api/owner/restaurant")
        assert response.status_code == 401

    def test_update_restaurant(self, client, test_owner, test_restaurant, auth_headers_owner):
        """Test updating restaurant details"""
        response = client.put("/api/owner/restaurant", headers=auth_headers_owner, json={
            "name": "Updated Restaurant",
            "email": "updated@restaurant.com",
            "cuisine": "Mexican",
            "description": "Updated description"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Restaurant"
        assert data["email"] == "updated@restaurant.com"
        assert data["cuisine"] == "Mexican"

    def test_get_owner_menu(self, client, test_owner, test_restaurant, test_menu_items, auth_headers_owner):
        """Test getting owner's menu items"""
        response = client.get("/api/owner/menu", headers=auth_headers_owner)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["restaurant_id"] == test_restaurant.id for item in data)

    def test_add_menu_item(self, client, test_owner, test_restaurant, auth_headers_owner):
        """Test adding a new menu item"""
        response = client.post("/api/owner/menu", headers=auth_headers_owner, json={
            "restaurant_id": test_restaurant.id,
            "name": "New Dish",
            "description": "A new delicious dish",
            "price": 18.99,
            "category": "Main",
            "is_special": False,
            "special_label": ""
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Dish"
        assert data["price"] == 18.99
        assert data["restaurant_id"] == test_restaurant.id

    def test_add_menu_item_wrong_restaurant(self, client, test_owner, auth_headers_owner):
        """Test adding menu item to another restaurant fails"""
        response = client.post("/api/owner/menu", headers=auth_headers_owner, json={
            "restaurant_id": "different-restaurant-id",
            "name": "New Dish",
            "price": 18.99,
            "category": "Main"
        })
        assert response.status_code == 403

    def test_update_menu_item(self, client, test_owner, test_restaurant, test_menu_items, auth_headers_owner):
        """Test updating a menu item"""
        item_id = test_menu_items[0].id
        response = client.put(f"/api/owner/menu/{item_id}", headers=auth_headers_owner, json={
            "name": "Updated Pizza",
            "price": 14.99,
            "is_special": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Pizza"
        assert data["price"] == 14.99
        assert data["is_special"] is False

    def test_delete_menu_item(self, client, test_owner, test_restaurant, test_menu_items, auth_headers_owner):
        """Test deleting a menu item"""
        item_id = test_menu_items[0].id
        response = client.delete(f"/api/owner/menu/{item_id}", headers=auth_headers_owner)
        assert response.status_code == 200

        # Verify item is deleted
        response = client.get("/api/owner/menu", headers=auth_headers_owner)
        data = response.json()
        assert len(data) == 1
        assert not any(item["id"] == item_id for item in data)

    def test_get_owner_orders(self, client, test_owner, test_customer, test_restaurant, test_menu_items, auth_headers_owner, auth_headers_customer):
        """Test getting orders for owner's restaurant"""
        # Place an order as customer
        client.post("/api/customer/orders", headers=auth_headers_customer, json={
            "restaurant_id": test_restaurant.id,
            "items": [{"menu_item_id": test_menu_items[0].id, "quantity": 1}]
        })

        # Get orders as owner
        response = client.get("/api/owner/orders", headers=auth_headers_owner)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["restaurant_id"] == test_restaurant.id

    def test_update_order_status(self, client, test_owner, test_customer, test_restaurant, test_menu_items, auth_headers_owner, auth_headers_customer, db_session):
        """Test updating order status"""
        # Place an order
        order_response = client.post("/api/customer/orders", headers=auth_headers_customer, json={
            "restaurant_id": test_restaurant.id,
            "items": [{"menu_item_id": test_menu_items[0].id, "quantity": 1}]
        })
        order_id = order_response.json()["id"]

        # Update status
        response = client.put(f"/api/owner/orders/{order_id}/status", headers=auth_headers_owner, json={
            "status": "preparing"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "preparing"

    def test_get_popular_items(self, client, test_owner, test_restaurant, test_menu_items, auth_headers_owner):
        """Test getting popular items analytics"""
        response = client.get("/api/owner/analytics/popular-items", headers=auth_headers_owner)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Should be sorted by order_count descending
        assert data[0]["name"] == "Test Pizza"
        assert data[0]["order_count"] == 10
