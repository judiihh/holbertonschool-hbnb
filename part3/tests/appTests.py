import unittest
import json
from app import create_app
from app.services import facade  # Our global facade instance

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Clear all in-memory repositories before each test
        facade.user_repo.storage.clear()
        facade.amenity_repo.storage.clear()
        facade.place_repo.storage.clear()
        facade.review_repo.storage.clear()

class TestUserEndpoints(BaseTestCase):

    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        # Create a user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_single_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob.jones@example.com"
        })
        data = json.loads(response.data)
        user_id = data["id"]
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["email"], "bob.jones@example.com")

    def test_update_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Carol",
            "last_name": "King",
            "email": "carol.king@example.com"
        })
        data = json.loads(response.data)
        user_id = data["id"]
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Caroline"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "Caroline")

class TestAmenityEndpoints(BaseTestCase):

    def test_create_amenity_valid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)

    def test_get_all_amenities(self):
        self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_update_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        data = json.loads(response.data)
        amenity_id = data["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Valet Parking"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["name"], "Valet Parking")

class TestPlaceEndpoints(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a user to own places
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@example.com"
        })
        self.owner = json.loads(response.data)

    def test_create_place_valid(self):
        response = self.client.post('/api/v1/places/', json={
            "user_id": self.owner["id"],
            "name": "Luxury Villa",
            "description": "A beautiful beachfront villa",
            "number_rooms": 4,
            "number_bathrooms": 3,
            "max_guest": 8,
            "price_by_night": 500,
            "latitude": 25.7617,
            "longitude": -80.1918,
            "amenity_ids": []
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)

    def test_create_place_invalid_user(self):
        response = self.client.post('/api/v1/places/', json={
            "user_id": "non-existent-id",
            "name": "Luxury Villa",
            "description": "A beautiful beachfront villa",
            "number_rooms": 4,
            "number_bathrooms": 3,
            "max_guest": 8,
            "price_by_night": 500,
            "latitude": 25.7617,
            "longitude": -80.1918,
            "amenity_ids": []
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place(self):
        response = self.client.post('/api/v1/places/', json={
            "user_id": self.owner["id"],
            "name": "Old Name",
            "description": "Old description",
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "price_by_night": 100,
            "latitude": 25.0,
            "longitude": -80.0,
            "amenity_ids": []
        })
        data = json.loads(response.data)
        place_id = data["id"]
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "name": "New Luxury Villa",
            "price_by_night": 150
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["name"], "New Luxury Villa")
        self.assertEqual(data["price_by_night"], 150)

    def test_get_all_places(self):
        self.client.post('/api/v1/places/', json={
            "user_id": self.owner["id"],
            "name": "Test Place",
            "description": "Test description",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 200,
            "latitude": 26.0,
            "longitude": -81.0,
            "amenity_ids": []
        })
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

class TestReviewEndpoints(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create a user and a place for reviews
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@example.com"
        })
        self.user = json.loads(user_response.data)
        place_response = self.client.post('/api/v1/places/', json={
            "user_id": self.user["id"],
            "name": "Review Place",
            "description": "Place for reviews",
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "price_by_night": 80,
            "latitude": 25.0,
            "longitude": -80.0,
            "amenity_ids": []
        })
        self.place = json.loads(place_response.data)

    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": "Great place to stay!"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)

    def test_create_review_invalid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": "Nice and cozy!"
        })
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_single_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": "Excellent!"
        })
        self.assertEqual(response.status_code, 201)
        review = json.loads(response.data)
        review_id = review["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["text"], "Excellent!")

    def test_update_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": "Good service."
        })
        self.assertEqual(response.status_code, 201)
        review = json.loads(response.data)
        review_id = review["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text."
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["text"], "Updated review text.")

    def test_delete_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user["id"],
            "place_id": self.place["id"],
            "text": "Review to be deleted."
        })
        self.assertEqual(response.status_code, 201)
        review = json.loads(response.data)
        review_id = review["id"]
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
