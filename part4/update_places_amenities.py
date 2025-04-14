#!/usr/bin/env python3
"""
Script to update places with specified amenities
"""
import os
import json
import subprocess

# API URL and Authentication Token
API_URL = "http://localhost:5000/api/v1"
AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDM5MjE0NCwianRpIjoiMGMyOTczOWUtN2E0MS00MmZhLWI3NjktODg0NDA0ZWI5Mjc1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE4MDY3MWJkLTVhODMtNDVjNy04YjAxLTZmZTMzZjc5ZmE5ZiIsIm5iZiI6MTc0NDM5MjE0NCwiZXhwIjoxNzQ0MzkzMDQ0LCJpc19hZG1pbiI6ZmFsc2V9._cItD8hx4ILw4dqILoBgj36roAfKWL4Cxf1QG4hU8N4"

# Place IDs
LUXURY_BEACH_HOUSE_ID = "d4432664-4d33-4b22-ae56-3ba5a4059106"
MAJESTIC_BLUE_HOUSE_ID = "2e4f90fb-d0c1-488d-a84b-3c01e8826353" 
PINK_PARADISE_HOUSE_ID = "7b0caf0b-5d99-468f-b9b8-82be589c2f1b"

# Amenity IDs
AMENITIES = {
    "WiFi": "ce3b7da9-9656-46b4-af5c-e7051253dd6e",
    "Pool": "f732480e-fae9-4d08-9bbb-6555247d974b",
    "Air Conditioning": "561d531b-8049-45d8-be5f-c888b386119a",
    "Jacuzzi": "ed0d840c-a347-4674-b559-148d8b6e146b",
    "Pet-friendly": "12482476-9ff3-47c4-ba52-8d988620c99a",
    "Free parking": "27be0a90-0ac0-4a1d-9eb2-af975e6d487d",
    "Heating": "f8c27d98-a0c9-42b9-8226-cc5ea0f84547",
    "Snack table": "90eb9471-490f-4c0d-b21d-7ac1bdeb8a70",
    "a fully equipped kitchen": "0f472b71-41e4-466b-87fb-6fb11b58401d"
}

# Place amenity assignments
LUXURY_BEACH_HOUSE_AMENITIES = [
    AMENITIES["WiFi"],
    AMENITIES["Pool"],
    AMENITIES["Air Conditioning"],
    AMENITIES["Jacuzzi"],
    AMENITIES["Pet-friendly"],
    AMENITIES["Free parking"]
]

MAJESTIC_BLUE_HOUSE_AMENITIES = [
    AMENITIES["WiFi"],
    AMENITIES["Pool"],
    AMENITIES["Air Conditioning"],
    AMENITIES["Heating"],
    AMENITIES["Snack table"]
]

PINK_PARADISE_HOUSE_AMENITIES = [
    AMENITIES["WiFi"],
    AMENITIES["Pool"],
    AMENITIES["Air Conditioning"],
    AMENITIES["Pet-friendly"],
    AMENITIES["Jacuzzi"],
    AMENITIES["a fully equipped kitchen"]
]

def update_place(place_id, place_name, amenity_ids):
    """Update a place with specified amenities"""
    print(f"Updating {place_name} with amenities...")
    
    # Create the JSON payload
    payload = json.dumps({
        "amenity_ids": amenity_ids
    })
    
    # Run the curl command
    try:
        cmd = [
            "curl", 
            "-X", "PUT", 
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {AUTH_TOKEN}",
            "-d", payload,
            f"{API_URL}/places/{place_id}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully updated {place_name}!")
            print(f"Response: {result.stdout}")
            return True
        else:
            print(f"Error updating {place_name}.")
            print(f"Error: {result.stderr}")
            print(f"Response: {result.stdout}")
            return False
    except Exception as e:
        print(f"Exception occurred while updating {place_name}: {e}")
        return False

if __name__ == "__main__":
    # Update Luxury Beach House
    update_place(
        LUXURY_BEACH_HOUSE_ID,
        "Luxury Beach House",
        LUXURY_BEACH_HOUSE_AMENITIES
    )
    
    # Update Majestic Blue House
    update_place(
        MAJESTIC_BLUE_HOUSE_ID,
        "Majestic Blue House",
        MAJESTIC_BLUE_HOUSE_AMENITIES
    )
    
    # Update Pink Paradise House
    update_place(
        PINK_PARADISE_HOUSE_ID,
        "Pink Paradise House",
        PINK_PARADISE_HOUSE_AMENITIES
    )
    
    print("\nAll places have been updated with their amenities.") 