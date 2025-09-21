import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.main import api  
from fastapi.testclient import TestClient
import pytest

client = TestClient(api)

# ===========================
# Test: Index route
# ===========================
def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}

# ===========================
# Test: Add book
# ===========================
def test_add_book():
    book_data = {
        "id": 1,
        "name": "Python 101",
        "description": "Introduction to Python",
        "isAvailable": True
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Python 101"

# ===========================
# Test: Get books
# ===========================
def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

# ===========================
# Test: Update book
# ===========================
def test_update_book():
    updated_data = {
        "id": 1,
        "name": "Python 102",
        "description": "Advanced Python",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Python 102"

# ===========================
# Test: Delete book
# ===========================
def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# ===========================
# Test: Delete non-existent book
# ===========================
def test_delete_nonexistent_book():
    response = client.delete("/book/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found, deletion failed"}
