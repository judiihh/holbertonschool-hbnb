from uuid import uuid4
from datetime import datetime
from app import db
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(db.Model):
    """Base model with common attributes and methods for SQLAlchemy models"""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.
        
        Args:
            *args: Variable length argument list.
            **kwargs (dict): Key/value pairs of attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key not in ['__class__', 'id', 'created_at', 'updated_at']:
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """Updates the updated_at attribute and saves the model to database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """Converts object attributes to a dictionary"""
        obj_dict = {}
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if isinstance(value, datetime):
                obj_dict[key] = value.isoformat()
            else:
                obj_dict[key] = value
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict

    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()
