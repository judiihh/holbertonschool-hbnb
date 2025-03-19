class Config:
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Update the SQLALCHEMY_DATABASE_URI to use MySQL for production
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@hostname/dbname'
