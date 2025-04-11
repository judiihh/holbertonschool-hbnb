-- Drop existing tables in reverse order of dependencies
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Create Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    first_name VARCHAR(80),
    last_name VARCHAR(80),
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Places table
CREATE TABLE places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    price INTEGER,
    owner_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Create Reviews table
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    rating INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    place_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

-- Create Amenities table
CREATE TABLE amenities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create association table for many-to-many relationship between Places and Amenities
CREATE TABLE place_amenity (
    place_id INTEGER NOT NULL,
    amenity_id INTEGER NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert initial data

-- Insert an administrator user (Note: Replace 'hashed_admin_password' with an actual hashed value)
INSERT INTO users (username, first_name, last_name, email, password_hash, is_admin)
VALUES ('admin', 'Admin', 'User', 'admin@example.com', 'admin123', 1);

-- Insert some amenities
INSERT INTO amenities (name, description) VALUES 
('WiFi', 'Wireless internet access'),
('Parking', 'On-site parking available'),
('Pool', 'Outdoor swimming pool');

-- (Optional) Insert a sample place owned by the admin (id=1)
INSERT INTO places (name, description, price, owner_id)
VALUES ('Luxury Villa', 'A beautiful villa with a great view', 350, 1);

-- (Optional) Insert a sample review for the place
INSERT INTO reviews (content, rating, user_id, place_id)
VALUES ('Amazing place!', 5, 1, 1);
