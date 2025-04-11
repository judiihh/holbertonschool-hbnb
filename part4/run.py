from app import create_app, db
from app.db_init import init_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Initialize the application with the appropriate config
    env = os.getenv("FLASK_ENV", "development")
    app = create_app(f"config.{env.capitalize()}Config")

    with app.app_context():
        # Initialize database tables if they don't exist
        db.create_all()

    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
