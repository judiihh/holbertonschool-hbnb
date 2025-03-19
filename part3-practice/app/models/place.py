from app import db
from app.models.base_model import BaseModel
from app.models.association import place_amenity  # Import the association table

class Place(BaseModel):
    __tablename__ = 'places'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    # Foreign key: the owner (User) of the place.
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # One-to-Many: A place can have many reviews.
    reviews = db.relationship('Review', backref='place', lazy=True)

    # Many-to-Many: A place can have many amenities.
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places', lazy='subquery')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
