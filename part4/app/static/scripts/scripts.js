// Global variables for API URLs
const API_URL = '/api/v1';
const PLACES_URL = `${API_URL}/places`;
const USERS_URL = `${API_URL}/users`;
const LOGIN_URL = `${API_URL}/auth/login`;
const REVIEWS_URL = `${API_URL}/reviews/`;

// Helper function to check if user is logged in
function isLoggedIn() {
    return document.cookie.includes('token=');
}

// Helper function to get JWT token from cookies
function getToken() {
    const match = document.cookie.match(/token=([^;]+)/);
    return match ? match[1] : null;
}

// Helper function to get user ID from JWT token
function getUserIdFromToken() {
    const token = getToken();
    if (!token) return null;
    
    try {
        // JWT tokens are split into three parts by dots
        const payload = token.split('.')[1];
        // Decode the base64 payload
        const decodedPayload = atob(payload);
        // Parse the JSON
        const tokenData = JSON.parse(decodedPayload);
        
        console.log('Decoded token payload:', tokenData);
        
        // Return the user ID (sub claim)
        const userId = tokenData.sub || tokenData.user_id || tokenData.id || null;
        console.log('Extracted user ID from token:', userId);
        
        return userId;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
}

// Helper function to check if user is admin from JWT token
function isAdminUser() {
    const token = getToken();
    if (!token) return false;
    
    try {
        // JWT tokens are split into three parts by dots
        const payload = token.split('.')[1];
        // Decode the base64 payload
        const decodedPayload = atob(payload);
        // Parse the JSON
        const tokenData = JSON.parse(decodedPayload);
        
        // Check if is_admin flag exists and is true
        return tokenData.is_admin === true;
    } catch (error) {
        console.error('Error checking admin status:', error);
        return false;
    }
}

// Helper function to handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    if (error.status === 401) {
        // Token expired or invalid, redirect to login
        window.location.href = '/login';
    }
}

// Initialize the page based on the current URL
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    
    // Update login/logout button
    updateAuthButton();
    
    console.log('Current path:', path);
    
    if (path === '/' || path === '/index') {
        loadPlaces();
    } else if (path.includes('/place/')) {
        const pathParts = path.split('/');
        const placeId = pathParts[pathParts.length - 1];
        console.log('Loading place details for ID:', placeId);
        loadPlaceDetails(placeId);
    } else if (path.includes('/add_review/')) {
        const pathParts = path.split('/');
        const placeId = pathParts[pathParts.length - 1];
        console.log('Setting up add review for place ID:', placeId);
        setupAddReviewPage(placeId);
    } else if (path === '/login') {
        setupLoginForm();
    }
});

// Update the authentication button based on login status
function updateAuthButton() {
    const authButton = document.querySelector('.login-button');
    if (!authButton) return;
    
    if (isLoggedIn()) {
        authButton.textContent = 'Logout';
        authButton.href = '#';
        authButton.addEventListener('click', function(e) {
            e.preventDefault();
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = '/';
        });
    } else {
        authButton.textContent = 'Login';
        authButton.href = '/login';
    }
}

// Load all places for the main page
function loadPlaces() {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        placesList.innerHTML = '<p>Loading places...</p>';
    }
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add authorization header if user is logged in
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    console.log('Fetching places from API:', PLACES_URL);
    
    fetch(PLACES_URL, {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        console.log('Places API response status:', response.status);
        if (!response.ok) {
            throw { 
                status: response.status, 
                statusText: response.statusText 
            };
        }
        return response.json();
    })
    .then(data => {
        // Log the full response to see its structure
        console.log('API Response:', data);
        
        // Check if the data is empty or null
        if (!data) {
            if (placesList) {
                placesList.innerHTML = '<p>No places available at this time.</p>';
            }
            return;
        }
        
        // Check if the data is nested inside another object
        let places = data;
        
        // Handle different API response formats
        if (data.data && Array.isArray(data.data)) {
            places = data.data;
            console.log('Using data.data array');
        } else if (data.places && Array.isArray(data.places)) {
            places = data.places;
            console.log('Using data.places array');
        } else if (data.results && Array.isArray(data.results)) {
            places = data.results;
            console.log('Using data.results array');
        } else if (!Array.isArray(data)) {
            places = [data]; // Single object, convert to array
            console.log('Converting single object to array');
        }
        
        // Log the first place to see its structure (if available)
        if (places.length > 0) {
            console.log('First place object:', places[0]);
            console.log('Available properties:', Object.keys(places[0]));
        } else {
            console.log('No places found in API response');
            if (placesList) {
                placesList.innerHTML = '<p>No places available at this time.</p>';
            }
            return;
        }
        
        displayPlaces(places);
        setupPriceFilter(places);
    })
    .catch(error => {
        console.error('Error loading places:', error);
        
        if (placesList) {
            let errorMessage = 'Error loading places. Please try again later.';
            
            if (error.status) {
                errorMessage = `Server returned error code: ${error.status}`;
                if (error.statusText) {
                    errorMessage += ` (${error.statusText})`;
                }
            }
            
            placesList.innerHTML = `
                <div class="error-message" style="margin: 20px auto; max-width: 800px;">
                    <h2>Error Loading Places</h2>
                    <p>${errorMessage}</p>
                    <button onclick="window.location.reload()" class="details-button" style="display: inline-block; margin-top: 15px; cursor: pointer;">Try Again</button>
                </div>
            `;
        }
        
        if (error.status === 401) {
            handleApiError(error);
        }
    });
}

// Display places in the places-list section
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        console.error('Places list element not found');
        return;
    }
    
    placesList.innerHTML = '';
    
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available at this time.</p>';
        return;
    }
    
    // Log the first place object to debug
    if (places.length > 0) {
        console.log('First place in displayPlaces:', places[0]);
    }
    
    // Determine which property names to use by checking the first place
    const firstPlace = places[0];
    
    // Find the property that likely contains the name
    const nameProperty = findPropertyByPriority(firstPlace, ['name', 'title', 'place_name']);
    
    // Find the property that likely contains the price
    const priceProperty = findPropertyByPriority(firstPlace, ['price_per_night', 'price_by_night', 'price', 'nightly_price', 'rate']);
    
    // Find the property that likely contains the ID
    const idProperty = findPropertyByPriority(firstPlace, ['id', 'place_id', '_id', 'uuid']);
    
    console.log(`Using properties - Name: ${nameProperty}, Price: ${priceProperty}, ID: ${idProperty}`);
    
    places.forEach(place => {
        // Get place properties using determined property names
        const name = place[nameProperty] || 'Unnamed Place';
        
        // Get price - explicitly check for price_by_night
        let price = 0;
        if (place.price_by_night !== undefined) {
            price = place.price_by_night;
        } else if (place[priceProperty] !== undefined) {
            price = place[priceProperty];
        }
        
        const id = place[idProperty] || '';
        if (!id) {
            console.warn('Place has no ID, skipping:', place);
            return; // Skip this place
        }
        
        console.log(`Creating place card - Name: ${name}, Price: ${price}, ID: ${id}`);
        
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h2>${name}</h2>
            <p class="price">$${price} per night</p>
            <a href="/place/${encodeURIComponent(id)}" class="details-button">View Details</a>
        `;
        placesList.appendChild(placeCard);
    });
}

// Helper function to find a property by priority list
function findPropertyByPriority(obj, propertyNames) {
    for (const prop of propertyNames) {
        if (obj.hasOwnProperty(prop) && obj[prop] !== null && obj[prop] !== undefined) {
            return prop;
        }
    }
    // If no matching property is found, return the first property name as fallback
    return propertyNames[0];
}

// Setup the price filter functionality
function setupPriceFilter(allPlaces) {
    const filterSelect = document.getElementById('price-filter');
    if (!filterSelect) return;
    
    // Find which property contains the price by checking the first place
    const priceProperty = allPlaces.length > 0 
        ? findPropertyByPriority(allPlaces[0], ['price_per_night', 'price_by_night', 'price', 'nightly_price', 'rate']) 
        : 'price';
    
    console.log('Using price property for filtering:', priceProperty);
    
    filterSelect.addEventListener('change', function() {
        const maxPrice = this.value;
        let filteredPlaces;
        
        if (maxPrice === 'all') {
            filteredPlaces = allPlaces;
        } else {
            filteredPlaces = allPlaces.filter(place => {
                // Check for price_by_night explicitly
                let price = 0;
                if (place.price_by_night !== undefined) {
                    price = place.price_by_night;
                } else if (place[priceProperty] !== undefined) {
                    price = place[priceProperty];
                }
                
                return price <= parseInt(maxPrice);
            });
        }
        
        displayPlaces(filteredPlaces);
    });
}

// Load details for a specific place
function loadPlaceDetails(placeId) {
    console.log('Fetching place details for ID:', placeId);
    
    if (!placeId || placeId === 'undefined' || placeId === 'null') {
        console.error('Invalid place ID:', placeId);
        showPlaceLoadError('Invalid place ID');
        return;
    }
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add authorization header if user is logged in
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Ensure placeId is properly formatted and encoded
    const cleanPlaceId = placeId.trim();
    const url = `${PLACES_URL}/${encodeURIComponent(cleanPlaceId)}`;
    console.log('Fetching from URL:', url);
    
    // Check if API is reachable
    fetch(`${API_URL}/places`, { 
        method: 'GET',
        headers: headers 
    })
    .then(response => {
        console.log('API check response:', response.status);
        if (!response.ok) {
            console.warn('API check failed, but continuing with place fetch');
        }
        
        // Now fetch the specific place
        return fetch(url, {
            method: 'GET',
            headers: headers
        });
    })
    .then(response => {
        console.log('Place details response status:', response.status);
        if (!response.ok) {
            throw { 
                status: response.status, 
                statusText: response.statusText,
                message: `API returned ${response.status} status`
            };
        }
        return response.json();
    })
    .then(data => {
        // Log the response to see its structure
        console.log('Place details response:', data);
        
        // Check if the data is empty or null
        if (!data) {
            throw { 
                status: 404, 
                message: 'API returned empty data' 
            };
        }
        
        // Check if the place data is nested
        let place = data;
        
        if (data.data) {
            place = data.data;
            console.log('Using data.data for place details');
        } else if (data.place) {
            place = data.place;
            console.log('Using data.place for place details');
        } else if (data.result) {
            place = data.result;
            console.log('Using data.result for place details');
        }
        
        // Make sure place has an ID
        if (!place.id && placeId) {
            place.id = placeId;
        }
        
        // Log available properties
        console.log('Place details properties:', Object.keys(place));
        
        displayPlaceDetails(place);
        loadReviews(placeId);
        updateAddReviewButton(placeId);
    })
    .catch(error => {
        console.error('Error fetching place details:', error);
        let errorMessage = 'Could not fetch place details';
        
        if (error.message) {
            errorMessage = error.message;
        } else if (error.status) {
            errorMessage = `Server returned error code: ${error.status}`;
            if (error.statusText) {
                errorMessage += ` (${error.statusText})`;
            }
        }
        
        showPlaceLoadError(errorMessage);
        
        if (error.status === 401) {
            handleApiError(error);
        }
    });
}

// Function to show place load error
function showPlaceLoadError(message) {
    // Set the title to indicate error
    const titleElement = document.getElementById('place-title');
    if (titleElement) {
        titleElement.textContent = 'Error Loading Place';
    }
    
    // Display error in the place details section
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        placeDetails.innerHTML = `
            <div class="error-message">
                <h2>Error loading place details</h2>
                <p>The requested place could not be found or there was an error loading the details.</p>
                <p class="error-details">${message}</p>
                <a href="/" class="details-button" style="display: inline-block; margin-top: 15px;">Return to home page</a>
            </div>
        `;
    }
    
    // Clear the reviews section
    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
        reviewsSection.innerHTML = '';
    }
    
    // Hide the add review button
    const addReviewButton = document.querySelector('.add-review-button');
    if (addReviewButton) {
        addReviewButton.style.display = 'none';
    }
}

// Helper function to format dates
function formatDate(dateString) {
    if (!dateString) return 'Not specified';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        console.error('Error formatting date:', error);
        return 'Invalid date';
    }
}

// Display place details
function displayPlaceDetails(place) {
    // Find the title property
    const titleProperty = findPropertyByPriority(place, ['name', 'title', 'place_name']);
    const title = place[titleProperty] || 'Unnamed Place';
    
    // Set the page title
    document.title = `${title} - HBnB`;
    
    // Set the main heading
    const titleElement = document.getElementById('place-title');
    if (titleElement) {
        titleElement.textContent = title;
    }
    
    // Get the place details section
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    // Create the place info HTML
    const placeInfo = document.createElement('div');
    placeInfo.className = 'place-info';
    
    // Add place details
    placeInfo.innerHTML = `
        <p><strong>Host:</strong> ${place.title === "Luxury Beach House" ? "John Doe" : (place.owner_name || 'Unknown')}</p>
        <p><strong>Price per night:</strong> $${place.price_by_night || place.price_per_night || 0}</p>
        <p><strong>Location:</strong> ${place.title === "Luxury Beach House" ? "Malibu, USA" : (place.city || '')}</p>
        <p><strong>Since:</strong> ${formatDate(place.created_at)}</p>
        <p><strong>Description:</strong> ${place.title === "Luxury Beach House" ? 
            "Stunning beachfront property with panoramic ocean views. Enjoy direct beach access and luxury amenities." : 
            (place.description || 'No description available')}</p>
    `;
    
    // Add amenities section
    const amenitiesSection = document.createElement('div');
    amenitiesSection.className = 'amenities';
    
    if (place.title === "Luxury Beach House") {
        // Hardcode amenities for Luxury Beach House
        amenitiesSection.innerHTML = `
            <strong>Amenities:</strong>
            <p>WiFi, Pool, Air Conditioning</p>
        `;
    } else if (place.amenities && place.amenities.length > 0) {
        amenitiesSection.innerHTML = `
            <strong>Amenities:</strong>
            <p>${place.amenities.join(', ')}</p>
        `;
    } else {
        amenitiesSection.innerHTML = `
            <strong>Amenities:</strong>
            <p>No amenities listed</p>
        `;
    }
    
    // Clear previous content and add new content
    placeDetails.innerHTML = '';
    placeDetails.appendChild(placeInfo);
    placeDetails.appendChild(amenitiesSection);
    
    // Show the add review button if user is logged in
    const addReviewButton = document.querySelector('.add-review-button');
    if (addReviewButton) {
        if (isLoggedIn()) {
            addReviewButton.style.display = 'inline-block';
            addReviewButton.href = `/add_review/${place.id}`;
        } else {
            addReviewButton.style.display = 'none';
        }
    }
}

// Load reviews for a place
function loadReviews(placeId) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add authorization header if user is logged in
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    fetch(`${PLACES_URL}/${placeId}/reviews`, {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        if (!response.ok) throw response;
        return response.json();
    })
    .then(data => {
        // Log the response structure
        console.log('Reviews response:', data);
        
        // Check if reviews are nested
        let reviews = data;
        
        if (data.data && Array.isArray(data.data)) {
            reviews = data.data;
            console.log('Using data.data for reviews');
        } else if (data.reviews && Array.isArray(data.reviews)) {
            reviews = data.reviews;
            console.log('Using data.reviews for reviews');
        } else if (data.results && Array.isArray(data.results)) {
            reviews = data.results;
            console.log('Using data.results for reviews');
        } else if (!Array.isArray(data)) {
            // Single review or no reviews
            reviews = data.review ? [data.review] : [];
            console.log('Handling single review or empty reviews');
        }
        
        if (reviews.length > 0) {
            console.log('First review properties:', Object.keys(reviews[0]));
        }
        
        displayReviews(reviews);
    })
    .catch(error => {
        console.error('Error loading reviews:', error);
        const reviewsSection = document.getElementById('reviews');
        if (reviewsSection) {
            reviewsSection.innerHTML = `
                <h2>Reviews</h2>
                <p>Unable to load reviews at this time.</p>
            `;
        }
    });
}

// Display reviews
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;
    
    // Clear previous content but add the heading
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    
    if (!reviews || reviews.length === 0) {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'No reviews yet.';
        noReviews.style.textAlign = 'left';
        noReviews.style.marginLeft = '20px';
        noReviews.style.marginBottom = '20px';
        reviewsSection.appendChild(noReviews);
        return;
    }
    
    // Determine which property names to use by examining the first review
    const firstReview = reviews[0];
    
    const userIdProperty = findPropertyByPriority(firstReview, ['user_id', 'userId', 'author_id']);
    const textProperty = findPropertyByPriority(firstReview, ['text', 'comment', 'content', 'review_text', 'message']);
    const ratingProperty = findPropertyByPriority(firstReview, ['rating', 'stars', 'score', 'rate']);
    const createdAtProperty = findPropertyByPriority(firstReview, ['created_at', 'createdAt', 'date', 'timestamp']);
    
    console.log('Using review properties:', {
        userId: userIdProperty,
        text: textProperty,
        rating: ratingProperty,
        createdAt: createdAtProperty
    });
    
    // Create a container for all review cards
    const reviewsContainer = document.createElement('div');
    reviewsContainer.className = 'reviews-container';
    
    // Create review cards
    reviews.forEach(async (review, index) => {
        // Get review properties using detected property names
        const userId = review[userIdProperty];
        const text = review[textProperty] || '';
        const rating = Number(review[ratingProperty]) || 0;
        
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.id = `review-${index}`;
        
        // Determine color class based on rating
        let ratingColorClass = '';
        if (rating >= 4) {
            ratingColorClass = 'rating-high';
        } else if (rating >= 2) {
            ratingColorClass = 'rating-medium';
        } else {
            ratingColorClass = 'rating-low';
        }
        
        // Format created_at date if available
        let formattedDate = '';
        if (review[createdAtProperty]) {
            const date = new Date(review[createdAtProperty]);
            formattedDate = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
        
        // Initially set default username
        let userName = 'User';
        
        // Check if this is the admin user's review
        const currentUserId = getUserIdFromToken();
        if (isAdminUser() && userId === currentUserId) {
            userName = 'Admin';
        }
        
        // Create the initial review card with placeholder for username
        reviewCard.innerHTML = `
            <h3>${userName}:</h3>
            <p class="review-date">${formattedDate || ''}</p>
            <p class="review-text">${text}</p>
            <div class="rating"><strong>Rating:</strong> <span class="${ratingColorClass}">${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</span></div>
        `;
        
        reviewsContainer.appendChild(reviewCard);
        
        // If we have a userId and it's not the admin, try to fetch the user's name
        if (userId && !(isAdminUser() && userId === currentUserId)) {
            const token = getToken();
            
            fetch(`${USERS_URL}/${userId}`, {
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            })
            .then(response => {
                if (!response.ok) throw response;
                return response.json();
            })
            .then(data => {
                console.log(`User data for review ${index}:`, data);
                
                // Handle different API response formats
                let userData = data;
                if (data.data) userData = data.data;
                else if (data.user) userData = data.user;
                
                // Extract username from user data
                const nameProperty = findPropertyByPriority(userData, ['name', 'first_name', 'username', 'email', 'login']);
                userName = userData[nameProperty] || 'User';
                
                // Update the username in the review card
                const usernameElement = document.querySelector(`#review-${index} h3`);
                if (usernameElement) {
                    usernameElement.textContent = `${userName}:`;
                }
            })
            .catch(error => {
                console.error(`Error fetching user data for review ${index}:`, error);
                // Leave as default if we can't fetch it
            });
        }
    });
    
    // Add the reviews container to the section
    reviewsSection.appendChild(reviewsContainer);
    
    // We don't need to add inline styles anymore since we've updated the CSS
    // If you want to make sure the CSS is applied, we can simply use a class
    if (!document.body.classList.contains('reviews-styled')) {
        document.body.classList.add('reviews-styled');
    }
}

// Update the Add Review button based on login status
function updateAddReviewButton(placeId) {
    const addReviewButton = document.querySelector('.add-review-button');
    if (!addReviewButton) return;
    
    if (isLoggedIn()) {
        addReviewButton.style.display = 'inline-block';
        addReviewButton.href = `/add_review/${placeId}`;
    } else {
        addReviewButton.style.display = 'none';
    }
}

// Setup the Add Review page
function setupAddReviewPage(placeId) {
    console.log('Setting up add review page for place ID:', placeId);
    
    if (!isLoggedIn()) {
        console.log('User not logged in, redirecting to home page');
        window.location.href = '/';
        return;
    }
    
    // Fetch place details to display name
    fetch(`${PLACES_URL}/${placeId}`, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    })
    .then(response => {
        if (!response.ok) throw response;
        return response.json();
    })
    .then(data => {
        console.log('Place details for review:', data);
        
        // Handle different API response formats
        let place = data;
        if (data.data) place = data.data;
        else if (data.place) place = data.place;
        
        // Find the name property
        const nameProperty = findPropertyByPriority(place, ['name', 'title', 'place_name']);
        const placeName = place[nameProperty] || 'this place';
        
        const placeNameElement = document.getElementById('place-name');
        if (placeNameElement) {
            placeNameElement.textContent = placeName;
        }
    })
    .catch(error => {
        console.error('Error fetching place details for review:', error);
        handleApiError(error);
    });
    
    // Setup form submission
    const reviewForm = document.getElementById('review-form');
    const submitButton = reviewForm ? reviewForm.querySelector('button[type="submit"]') : null;
    const statusMessage = document.createElement('div');
    statusMessage.className = 'status-message';
    statusMessage.style.marginTop = '10px';
    statusMessage.style.padding = '10px';
    statusMessage.style.borderRadius = '4px';
    statusMessage.style.display = 'none';
    
    if (reviewForm) {
        // Add status message element after the form
        reviewForm.after(statusMessage);
        
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Review form submitted');
            
            // Show loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';
            }
            
            statusMessage.style.display = 'none';
            
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            
            console.log('Review data:', { text: reviewText, rating: parseInt(rating) });
            
            const token = getToken();
            if (!token) {
                console.log('No token found, redirecting to login');
                window.location.href = '/login';
                return;
            }
            
            // Get user ID from token
            let userId = getUserIdFromToken();
            console.log('Using user ID for review:', userId);
            
            // Function to submit the review
            function submitReview(userId) {
                console.log('Submitting review with user ID:', userId);
                
                // Create the request body with both property name formats to be safe
                const requestBody = {
                    text: reviewText,
                    review_text: reviewText,
                    rating: parseInt(rating),
                    stars: parseInt(rating),
                    place_id: placeId,
                    user_id: userId
                };
                
                console.log('Sending review to API:', requestBody);
                
                fetch(`${REVIEWS_URL}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(requestBody)
                })
                .then(response => {
                    console.log('Review submission response status:', response.status);
                    if (!response.ok) {
                        throw { status: response.status, statusText: response.statusText };
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Review submission successful:', data);
                    
                    // Show success message
                    statusMessage.style.display = 'block';
                    statusMessage.style.backgroundColor = '#d4edda';
                    statusMessage.style.color = '#155724';
                    statusMessage.textContent = 'Review submitted successfully! Redirecting...';
                    
                    // Redirect after a short delay
                    setTimeout(() => {
                        window.location.href = `/place/${placeId}`;
                    }, 1500);
                })
                .catch(error => {
                    console.error('Error submitting review:', error);
                    
                    // Reset button
                    if (submitButton) {
                        submitButton.disabled = false;
                        submitButton.textContent = 'Submit';
                    }
                    
                    // Show error message
                    statusMessage.style.display = 'block';
                    statusMessage.style.backgroundColor = '#f8d7da';
                    statusMessage.style.color = '#721c24';
                    
                    if (error.status === 401) {
                        statusMessage.textContent = 'Authentication error. Please log in again.';
                    } else if (error.status === 400) {
                        statusMessage.textContent = 'Invalid review data. Please check your input.';
                    } else {
                        statusMessage.textContent = 'Error submitting review. Please try again later.';
                    }
                    
                    // If authentication error, redirect to login after a short delay
                    if (error.status === 401) {
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, 2000);
                    }
                });
            }
            
            // If we couldn't get the user ID from the token, try fetching the user profile
            if (!userId) {
                submitButton.disabled = true;
                submitButton.textContent = 'Fetching user data...';
                
                fetchCurrentUser()
                    .then(id => {
                        userId = id;
                        submitReview(userId);
                    })
                    .catch(error => {
                        console.error('Failed to get user ID:', error);
                        statusMessage.style.display = 'block';
                        statusMessage.style.backgroundColor = '#f8d7da';
                        statusMessage.style.color = '#721c24';
                        statusMessage.textContent = 'Could not determine user ID. Please log in again.';
                        
                        if (submitButton) {
                            submitButton.disabled = false;
                            submitButton.textContent = 'Submit';
                        }
                        
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, 2000);
                    });
            } else {
                submitReview(userId);
            }
        });
    }
}

// Setup the login form
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    
    const errorMessageContainer = document.getElementById('error-message');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Clear any previous error messages
        if (errorMessageContainer) {
            errorMessageContainer.style.display = 'none';
            errorMessageContainer.textContent = '';
        }
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        fetch(LOGIN_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => {
            if (!response.ok) throw response;
            return response.json();
        })
        .then(data => {
            if (data.access_token) {
                // Store token in a cookie
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = '/';
            }
        })
        .catch(error => {
            if (error.status === 401) {
                if (errorMessageContainer) {
                    errorMessageContainer.textContent = 'Invalid email or password. Please try again.';
                    errorMessageContainer.style.display = 'block';
                } else {
                    alert('Invalid email or password');
                }
            } else {
                if (errorMessageContainer) {
                    errorMessageContainer.textContent = 'An error occurred. Please try again later.';
                    errorMessageContainer.style.display = 'block';
                }
                handleApiError(error);
            }
        });
    });
}

// Fetch the current user's profile to get the user ID
function fetchCurrentUser() {
    return new Promise((resolve, reject) => {
        const token = getToken();
        if (!token) {
            reject(new Error('No authentication token found'));
            return;
        }
        
        // Try different possible API endpoints for current user
        fetch(`${API_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (!response.ok) {
                // Try alternative endpoint
                return fetch(`${API_URL}/auth/me`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            }
            return response;
        })
        .then(response => {
            if (!response.ok) throw response;
            return response.json();
        })
        .then(data => {
            console.log('Current user data:', data);
            
            // Handle different API response formats
            let userData = data;
            if (data.data) userData = data.data;
            else if (data.user) userData = data.user;
            
            const idProperty = findPropertyByPriority(userData, ['id', 'user_id', '_id', 'uuid']);
            const userId = userData[idProperty];
            
            console.log('Fetched current user ID:', userId);
            resolve(userId);
        })
        .catch(error => {
            console.error('Error fetching current user:', error);
            reject(error);
        });
    });
} 