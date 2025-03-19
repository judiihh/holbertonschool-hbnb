from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for BaseModel
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
