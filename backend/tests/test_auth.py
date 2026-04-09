"""Tests for authentication endpoints"""
import pytest


class TestAuthEndpoints:
    """Test authentication-related endpoints"""

    def test_register_customer(self, client):
        """Test customer registration"""
        response = client.post("/api/auth/register", json={
            "email": "newcustomer@test.com",
            "password": "password123",
            "name": "New Customer",
            "role": "customer",
            "phone": "+1234567890",
            "address": "456 New Street"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == "newcustomer@test.com"
        assert data["user"]["role"] == "customer"
        assert "access_token" in data


    def test_register_duplicate_email(self, client, test_customer):
        """Test registration with duplicate email fails"""
        response = client.post("/api/auth/register", json={
            "email": "testcustomer@test.com",
            "password": "password123",
            "name": "Another User",
            "role": "customer"
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_login_success(self, client, test_customer):
        """Test successful login"""
        response = client.post("/api/auth/login", json={
            "email": "testcustomer@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "testcustomer@test.com"
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_customer):
        """Test login with wrong password fails"""
        response = client.post("/api/auth/login", json={
            "email": "testcustomer@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user fails"""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "password123"
        })
        assert response.status_code == 401

    def test_reset_password_success(self, client, test_customer):
        """Test password reset"""
        response = client.post("/api/auth/reset-password", json={
            "email": "testcustomer@test.com",
            "old_password": "password123",
            "new_password": "newpassword123"
        })
        assert response.status_code == 200
        assert "successful" in response.json()["message"].lower()

        # Test login with new password
        response = client.post("/api/auth/login", json={
            "email": "testcustomer@test.com",
            "password": "newpassword123"
        })
        assert response.status_code == 200

    def test_reset_password_wrong_old_password(self, client, test_customer):
        """Test password reset with wrong old password fails"""
        response = client.post("/api/auth/reset-password", json={
            "email": "testcustomer@test.com",
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        })
        assert response.status_code == 401
