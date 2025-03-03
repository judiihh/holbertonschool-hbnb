class InMemoryRepository:
    """A simple in-memory repository to store users."""

    def __init__(self):
        self.data = {}

    def add(self, obj):
        """Add an object to the repository."""
        self.data[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.data.get(obj_id)

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by an attribute value."""
        for obj in self.data.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None
