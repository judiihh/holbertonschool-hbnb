from app import db
from app.models.base_model import BaseModel
from app.models.association import place_amenity  # Import the association table

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # Many-to-Many: An amenity can belong to many places.
    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
