#!/usr/bin/env python3
"""
Script to add amenities to the HBnB application using curl commands with authentication
"""
import os
import json
import subprocess

# API URL and Token
API_URL = "http://localhost:5000/api/v1"
AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDM5MjE0NCwianRpIjoiMGMyOTczOWUtN2E0MS00MmZhLWI3NjktODg0NDA0ZWI5Mjc1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE4MDY3MWJkLTVhODMtNDVjNy04YjAxLTZmZTMzZjc5ZmE5ZiIsIm5iZiI6MTc0NDM5MjE0NCwiZXhwIjoxNzQ0MzkzMDQ0LCJpc19hZG1pbiI6ZmFsc2V9._cItD8hx4ILw4dqILoBgj36roAfKWL4Cxf1QG4hU8N4"

def run_curl_command(name):
    """Run a curl command to add an amenity with authentication"""
    print(f"Adding amenity: {name}...")
    
    # Create the JSON payload
    payload = json.dumps({"name": name})
    
    # Run the curl command with auth token
    try:
        cmd = [
            "curl", 
            "-X", "POST", 
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {AUTH_TOKEN}",
            "-d", payload,
            f"{API_URL}/amenities"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            try:
                response_data = json.loads(result.stdout)
                amenity_id = response_data.get('id')
                print(f"Successfully added amenity: {name} with ID: {amenity_id}")
                return amenity_id
            except json.JSONDecodeError:
                print(f"Could not parse response: {result.stdout}")
                return None
        else:
            print(f"Error adding amenity: {result.stderr}")
            print(f"Response: {result.stdout}")
            return None
    except Exception as e:
        print(f"Error running curl command: {e}")
        return None

if __name__ == "__main__":
    # Add the amenities
    amenity_ids = {}
    
    wifi_id = run_curl_command("WiFi")
    if wifi_id:
        amenity_ids['WiFi'] = wifi_id
    
    pool_id = run_curl_command("Pool")
    if pool_id:
        amenity_ids['Pool'] = pool_id
    
    ac_id = run_curl_command("Air Conditioning")
    if ac_id:
        amenity_ids['Air Conditioning'] = ac_id
    
    # Print the results
    if amenity_ids:
        print("\nAmenity IDs for reference:")
        for name, id in amenity_ids.items():
            print(f"{name}: {id}")
        
        amenity_ids_json = ', '.join([f'"{id}"' for id in amenity_ids.values()])
        
        print("\nTo add these amenities to a place, use the following format in your API request:")
        print(f'{{"amenity_ids": [{amenity_ids_json}]}}')
        
        print("\nTo update a place with these amenities, use this curl command:")
        curl_cmd = f'curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" '
        curl_cmd += f'-d \'{{"amenity_ids": [{amenity_ids_json}]}}\' {API_URL}/places/PLACE_ID_HERE'
        print(curl_cmd)
    else:
        print("\nNo amenities were added successfully.") 