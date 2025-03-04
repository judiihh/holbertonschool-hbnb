class InMemoryRepository:
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
        return list(self.storage.values())

    def get_by_attribute(self, attr, value):
        """Retrieve an entity by a specific attribute (e.g., email)"""
        return next((entity for entity in self.storage.values() if getattr(entity, attr, None) == value), None)
