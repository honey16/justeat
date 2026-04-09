"""Tests for restaurant endpoints"""
import pytest


class TestRestaurantEndpoints:
    """Test public restaurant endpoints"""

    def test_get_restaurants(self, client, test_restaurant):
        """Test getting list of restaurants"""
        response = client.get("/api/restaurants")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["name"] == "Test Restaurant"

    def test_get_restaurants_with_filter(self, client, test_restaurant):
        """Test filtering restaurants by cuisine"""
        response = client.get("/api/restaurants", params={"cuisine": "Italian"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(r["cuisine"] == "Italian" for r in data)

    def test_get_restaurants_with_location_filter(self, client, test_restaurant):
        """Test filtering restaurants by location"""
        response = client.get("/api/restaurants", params={"location": "Test Location"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(r["location"] == "Test Location" for r in data)

    def test_get_restaurant_by_id(self, client, test_restaurant, test_menu_items):
        """Test getting restaurant details"""
        response = client.get(f"/api/restaurants/{test_restaurant.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_restaurant.id
        assert data["name"] == "Test Restaurant"
        assert "menu" in data
        assert len(data["menu"]) == 2

    def test_get_restaurant_by_id_not_found(self, client):
        """Test getting nonexistent restaurant returns 404"""
        response = client.get("/api/restaurants/nonexistent-id")
        assert response.status_code == 404

    def test_get_restaurant_menu(self, client, test_restaurant, test_menu_items):
        """Test getting restaurant menu"""
        response = client.get(f"/api/restaurants/{test_restaurant.id}/menu")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] in ["Test Pizza", "Test Pasta"]

    def test_get_restaurant_menu_by_category(self, client, test_restaurant, test_menu_items):
        """Test filtering menu by category"""
        response = client.get(f"/api/restaurants/{test_restaurant.id}/menu", params={"category": "Pizza"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Pizza"

    def test_get_restaurant_specials(self, client, test_restaurant, test_menu_items):
        """Test getting special menu items"""
        response = client.get(f"/api/restaurants/{test_restaurant.id}/specials")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_special"] is True
        assert data[0]["name"] == "Test Pizza"

    def test_get_restaurant_popular(self, client, test_restaurant, test_menu_items):
        """Test getting popular menu items"""
        response = client.get(f"/api/restaurants/{test_restaurant.id}/popular")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Should be sorted by order_count descending
        assert data[0]["name"] == "Test Pizza"
        assert data[0]["order_count"] == 10
