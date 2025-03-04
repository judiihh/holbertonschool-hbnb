# 🏠 HBnB Project - Part 2

## 🔍 Overview

Part 2 of the HBnB Project focuses on implementing the core Business Logic and API Endpoints for the HBnB application. In this part, we build the Presentation and Business Logic layers using Python, Flask, and flask-restx. The project uses an in-memory repository to simulate persistence and follows a modular architecture with clear separation of concerns. This version supports CRUD operations for Users, Amenities, Places, and Reviews (with DELETE implemented only for reviews).

> **Note:** JWT authentication and role-based access control will be implemented in Part 3.

---

## 💃 Project Structure

```
part2/
├── app/
│   ├── __init__.py                # Application factory & API namespace registration
│   ├── api/
│   │   └── v1/
│   │       ├── users.py           # User endpoints (POST, GET, PUT)
│   │       ├── amenities.py       # Amenity endpoints (POST, GET, PUT)
│   │       ├── places.py          # Place endpoints (POST, GET, PUT)
│   │       └── reviews.py         # Review endpoints (POST, GET, PUT, DELETE)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py          # Base model (id, created_at, updated_at)
│   │   ├── user.py                # User model
│   │   ├── amenity.py             # Amenity model
│   │   ├── place.py               # Place model
│   │   └── review.py              # Review model
│   ├── persistence/
│   │   └── repository.py          # In-memory repository implementation
│   └── services/
│       ├── __init__.py            # Global facade instance initialization
│       └── facade.py              # HBnBFacade: Business logic, validations, CRUD
├── appTests.py                    # Automated unit tests using unittest
└── README.md                      # This file
```

---

## 🛠️ Setup and Installation

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the required packages:**

   ```bash
   pip install flask flask-restx
   ```

---

## 🚀 Running the Application

Set the environment variables and run the server:

```bash
export FLASK_APP=app
export FLASK_ENV=development  # Optional: enables debug mode
flask run
```

The API endpoints will be available at:

- **Users:** `http://127.0.0.1:5000/api/v1/users/`
- **Amenities:** `http://127.0.0.1:5000/api/v1/amenities/`
- **Places:** `http://127.0.0.1:5000/api/v1/places/`
- **Reviews:** `http://127.0.0.1:5000/api/v1/reviews/`

---

## 🔧 API Endpoints

### Users

- **POST **``\
  Create a new user.
- **GET **``\
  Retrieve all users.
- **GET **``\
  Retrieve a user by ID.
- **PUT **``\
  Update user information.

### Amenities

- **POST **``\
  Create a new amenity.
- **GET **``\
  Retrieve all amenities.
- **PUT **``\
  Update an amenity.

### Places

- **POST **``\
  Create a new place.
- **GET **``\
  Retrieve all places.
- **GET **``\
  Retrieve a place by ID.
- **PUT **``\
  Update place data.

### Reviews

- **POST **``\
  Create a new review.
- **GET **``\
  Retrieve all reviews.
- **GET **``\
  Retrieve a review by ID.
- **PUT **``\
  Update a review.
- **DELETE **``\
  Delete a review.

---

## 💻 Business Logic and Persistence

- **Facade Pattern:** Simplifies communication between the Presentation and Business Logic layers.
- **Validations:** Ensures correct user inputs for Users, Amenities, Places, and Reviews.
- **In-Memory Repository:** Temporary object storage for CRUD operations.

---

## 🔧 Automated Testing

Run tests with:

```bash
python3 -m unittest appTests.py
```

Expected output:

```
Ran 18 tests in X.XXXs
OK
```

---

## 📑 Swagger Documentation

View API documentation at:

```
http://127.0.0.1:5000/
(This only works running with flask inside local machine)
```

---

## ✅ Conclusion

Part 2 successfully implements the core Business Logic and API endpoints for the HBnB application using Flask and flask-restx. This foundation will support database integration and authentication in Part 3.
