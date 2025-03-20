from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    """Abstract base class for repository implementations"""
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """A simple in-memory repository to store entities"""
    def __init__(self):
        self.storage = {}

    def add(self, entity):
        """Adds an entity to the storage"""
        self.storage[entity.id] = entity

    def get(self, entity_id):
        """Retrieves an entity by its ID"""
        return self.storage.get(entity_id)

    def update(self, entity):
        """Updates an existing entity in the storage"""
        if entity.id in self.storage:
            self.storage[entity.id] = entity

    def get_all(self):
        """Retrieves all entities in the storage"""
        return list(self.storage.values())  # Fix: Convert dict values to a list

    def get_by_attribute(self, attribute, value):
        """Retrieves an entity by a specific attribute (e.g., email)"""
        for entity in self.storage.values():
            if getattr(entity, attribute, None) == value:
                return entity
        return None  # If no entity matches the attribute

    def delete(self, obj_id):
        """Deletes an entity by its ID"""
        if obj_id in self.storage:
            del self.storage[obj_id]


class SQLAlchemyRepository(Repository):
    """A repository implementation using SQLAlchemy for database operations"""
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Adds an object to the database"""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieves an object by its ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieves all objects of this model"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Updates an object with the provided data"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Deletes an object by its ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves an object by a specific attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
