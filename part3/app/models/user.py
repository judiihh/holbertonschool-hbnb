from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, plain_password):
        """Hash password on setting."""
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, password):
        """Return True if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize user details without the password hash."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # Do NOT include password_hash in the serialized output
        }
