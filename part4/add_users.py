#!/usr/bin/env python3
"""
Script to add test users to the HBnB application
"""
import sys
import os
import json
import requests

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try using the API directly first
API_URL = "http://localhost:5000/api/v1"

def add_user_api(first_name, last_name, email, password):
    """Add a user via API call"""
    print(f"Adding user {first_name} {last_name} with email {email}...")
    
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{API_URL}/users", json=data)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 201 or response.status_code == 200:
            print(f"Successfully added user {first_name} {last_name}")
            return True
        else:
            print(f"Failed to add user. Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error adding user via API: {e}")
        return False

# Try adding users directly to the database as a fallback
def add_user_direct():
    """Add users directly to the database as a fallback"""
    try:
        from app.models import db, User
        from app.app import app
        
        with app.app_context():
            # Check if users already exist
            jane = User.query.filter_by(email="janesmith@gmail.com").first()
            if not jane:
                jane = User(
                    first_name="Jane",
                    last_name="Smith",
                    email="janesmith@gmail.com",
                    password="jane123"
                )
                db.session.add(jane)
                print("Added Jane Smith")
            else:
                print("Jane Smith already exists")
                
            robert = User.query.filter_by(email="robertbrown@gmail.com").first()
            if not robert:
                robert = User(
                    first_name="Robert",
                    last_name="Brown",
                    email="robertbrown@gmail.com",
                    password="robert123"
                )
                db.session.add(robert)
                print("Added Robert Brown")
            else:
                print("Robert Brown already exists")
                
            db.session.commit()
            print("Users added successfully!")
            return True
    except Exception as e:
        print(f"Error adding users directly to database: {e}")
        return False

if __name__ == "__main__":
    # Try API method first
    api_success = (
        add_user_api("Jane", "Smith", "janesmith@gmail.com", "jane123") and
        add_user_api("Robert", "Brown", "robertbrown@gmail.com", "robert123")
    )
    
    # If API method fails, try direct database method
    if not api_success:
        print("API method failed, trying direct database method...")
        add_user_direct() 