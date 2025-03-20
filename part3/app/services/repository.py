class InMemoryRepository:
    """A singleton in-memory repository to store entities persistently while the server is running."""

    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InMemoryRepository, cls).__new__(cls)
            cls._instance.storage = {}  # Persistent in-memory storage
        return cls._instance

    def add(self, entity):
        """Adds an entity to the storage"""
        print(f"DEBUG: Storing entity {entity.id}: {entity.__dict__}")  # Debugging
        self.storage[entity.id] = entity

    def get(self, entity_id):
        """Retrieves an entity by its ID"""
        print(f"DEBUG: Fetching entity with ID {entity_id}")  # Debugging
        return self.storage.get(entity_id)

    def update(self, entity):
        """Updates an existing entity in the storage"""
        if entity.id in self.storage:
            self.storage[entity.id] = entity

    def get_all(self):
        """Retrieves all stored entities"""
        return list(self.storage.values())

    def get_by_attribute(self, attr, value):
        """Retrieve an entity by a specific attribute (e.g., email)"""
        return next((entity for entity in self.storage.values() if getattr(entity, attr, None) == value), None)
