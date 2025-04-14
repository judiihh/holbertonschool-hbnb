from .base_model import BaseModel
from app import db
from sqlalchemy.orm import relationship

# Define the association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenity.id'), primary_key=True)
)

class Place(BaseModel):
    """Represents a place (listing)."""
    
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    number_rooms = db.Column(db.Integer, default=0, nullable=False)
    number_bathrooms = db.Column(db.Integer, default=0, nullable=False)
    max_guest = db.Column(db.Integer, default=0, nullable=False)
    price_by_night = db.Column(db.Integer, default=0, nullable=False)
    price = db.Column(db.Integer, default=0, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Foreign keys
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, 
                             backref=db.backref('places', lazy='dynamic'), 
                             lazy='dynamic')

    def __init__(self, *args, **kwargs):
        """Initialize a Place instance with given attributes."""
        super().__init__(*args, **kwargs)

        # Convert or parse each argument from kwargs into the correct type
        self.owner_id = str(kwargs.get("owner_id", ""))
        self.title = str(kwargs.get("title", ""))
        self.description = str(kwargs.get("description", ""))

        self.number_rooms = int(kwargs.get("number_rooms", 0))
        self.number_bathrooms = int(kwargs.get("number_bathrooms", 0))
        self.max_guest = int(kwargs.get("max_guest", 0))
        self.price_by_night = int(kwargs.get("price_by_night", 0))
        self.price = int(kwargs.get("price", 0))

        # Cast latitude and longitude to float
        self.latitude = float(kwargs.get("latitude", 0.0))
        self.longitude = float(kwargs.get("longitude", 0.0))

        # Amenities are now handled through SQLAlchemy relationship
        
    def to_dict(self):
        """Overrides the BaseModel to_dict to include amenity_ids"""
        obj_dict = super().to_dict()
        # Add amenity_ids to the dictionary
        obj_dict['amenity_ids'] = [amenity.id for amenity in self.amenities.all()]
        
        # Add the owner's name as 'host'
        from app.models.user import User
        from app import db
        owner = db.session.query(User).filter(User.id == self.owner_id).first()
        if owner:
            obj_dict['host'] = f"{owner.first_name} {owner.last_name}"
        
        return obj_dict
