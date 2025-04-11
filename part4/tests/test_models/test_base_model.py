import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test case for the BaseModel class"""

    def test_instance_creation(self):
        """Test if BaseModel instance is correctly created"""
        obj = BaseModel()
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

if __name__ == "__main__":
    unittest.main()

