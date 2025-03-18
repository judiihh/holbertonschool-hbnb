from app import db

class SQLAlchemyRepository:
    """Repository that handles CRUD operations using SQLAlchemy."""

    def add(self, entity):
        """Add a new entity to the database and commit."""
        db.session.add(entity)
        db.session.commit()
        return entity

    def get(self, model, entity_id):
        """Retrieve an entity by its ID from the given model."""
        return model.query.get(entity_id)

    def update(self):
        """Commit any pending changes in the session."""
        db.session.commit()

    def delete(self, entity):
        """Delete an entity from the database and commit."""
        db.session.delete(entity)
        db.session.commit()

    def list(self, model):
        """Return all entities of a given model."""
        return model.query.all()
