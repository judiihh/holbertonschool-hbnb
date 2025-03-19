from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign keys: linking the review to its author (User) and the reviewed place.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
