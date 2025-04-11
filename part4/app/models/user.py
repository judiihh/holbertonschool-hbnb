from .base_model import BaseModel
from app import bcrypt, db

class User(BaseModel):
    """User model with authentication attributes"""
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = db.relationship('Place', backref='user', lazy=True, cascade="all, delete-orphan", foreign_keys='Place.owner_id')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes a User instance with attributes from kwargs"""
        super().__init__(*args, **kwargs)

        # Set default values if not provided in kwargs
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.is_admin = kwargs.get("is_admin", False)
        
        # Hash password if one is provided
        if "password" in kwargs and kwargs["password"]:
            self.hash_password(kwargs["password"])
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
        
    def to_dict(self):
        """Converts user object to dictionary excluding password"""
        user_dict = super().to_dict()
        # Remove password from the dictionary for security
        if 'password' in user_dict:
            del user_dict['password']
        return user_dict
