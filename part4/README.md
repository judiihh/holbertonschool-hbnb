# HBnB Frontend

This is the frontend part of the HBnB (Holberton BnB) project, a web application for property rentals.

## Project Structure

```
part4/
├── images/
│   ├── icon.svg
│   └── logo.svg
├── add_review.html
├── index.html
├── login.html
├── place.html
├── scripts.js
└── styles.css
```

## Features

- User authentication (login/logout)
- List of available places with price filtering
- Detailed view of each place
- Review system with ratings
- Responsive design for all screen sizes

## Setup

1. Make sure you have the backend API running on `http://localhost:5000`
2. Open `index.html` in your web browser
3. You can log in using the provided credentials

## API Integration

The frontend communicates with the backend API using the following endpoints:

- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/places` - List all places
- `GET /api/v1/places/:id` - Get place details
- `POST /api/v1/places/:id/reviews` - Add a review

## Design

The design follows modern web standards with:
- Clean and intuitive user interface
- Consistent color scheme (primary color: #ff8c00)
- Responsive grid layout for places
- Card-based design for places and reviews
- User-friendly forms with proper validation

## Browser Support

The application is compatible with:
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)
- Safari (latest)

## Validation

All HTML files have been validated using the W3C Validator and pass without errors.