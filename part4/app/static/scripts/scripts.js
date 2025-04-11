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
    
    if (path === '/' || path === '/index') {
        loadPlaces();
    } else if (path.includes('/place/')) {
        const placeId = path.split('/').pop();
        loadPlaceDetails(placeId);
    } else if (path.includes('/add_review/')) {
        const placeId = path.split('/').pop();
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
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add authorization header if user is logged in
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    fetch(PLACES_URL, {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        if (!response.ok) throw response;
        return response.json();
    })
    .then(data => {
        // Log the full response to see its structure
        console.log('API Response:', data);
        
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
        }
        
        displayPlaces(places);
        setupPriceFilter(places);
    })
    .catch(handleApiError);
}

// Display places in the places-list section
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
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
        
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h2>${name}</h2>
            <p class="price">$${price} per night</p>
            <a href="/place/${id}" class="details-button">View Details</a>
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
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add authorization header if user is logged in
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    fetch(`${PLACES_URL}/${placeId}`, {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        if (!response.ok) throw response;
        return response.json();
    })
    .then(data => {
        // Log the response to see its structure
        console.log('Place details response:', data);
        
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
        
        // Log available properties
        console.log('Place details properties:', Object.keys(place));
        
        displayPlaceDetails(place);
        loadReviews(placeId);
        updateAddReviewButton(placeId);
    })
    .catch(error => {
        console.error('Error fetching place details:', error);
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = `
                <div class="error-message">
                    <h2>Error loading place details</h2>
                    <p>The requested place could not be found or there was an error loading the details.</p>
                    <a href="/" class="details-button">Return to home page</a>
                </div>
            `;
        }
        handleApiError(error);
    });
}

// Display place details
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    // Log the complete place object to see all available properties and values
    console.log('Complete place object:', place);
    
    // Determine which property names to use
    const nameProperty = findPropertyByPriority(place, ['name', 'title', 'place_name']);
    const hostProperty = findPropertyByPriority(place, ['host_name', 'host', 'owner']);
    const priceProperty = findPropertyByPriority(place, ['price_per_night', 'price_by_night', 'price', 'nightly_price', 'rate']);
    const cityProperty = findPropertyByPriority(place, ['city', 'location_city', 'address_city']);
    const countryProperty = findPropertyByPriority(place, ['country', 'location_country', 'address_country']);
    const descriptionProperty = findPropertyByPriority(place, ['description', 'desc', 'about']);
    const amenitiesProperty = findPropertyByPriority(place, ['amenities', 'facilities', 'features']);
    const imageProperty = findPropertyByPriority(place, ['image_url', 'image', 'photo', 'picture_url']);
    const createdAtProperty = findPropertyByPriority(place, ['created_at', 'createdAt', 'creation_date']);
    
    console.log('Using place detail properties:', {
        name: nameProperty,
        host: hostProperty,
        price: priceProperty,
        city: cityProperty,
        country: countryProperty,
        desc: descriptionProperty,
        amenities: amenitiesProperty,
        image: imageProperty,
        createdAt: createdAtProperty
    });
    
    // Get values using detected property names
    const name = place[nameProperty] || 'Unnamed Place';
    const hostName = place[hostProperty] || 'Unknown';
    
    // Get price - explicitly check for price_by_night since this seems to be what the API is using
    let price = 0;
    if (place.price_by_night) {
        price = place.price_by_night;
    } else if (place[priceProperty]) {
        price = place[priceProperty];
    }
    
    const city = place[cityProperty] || '';
    const country = place[countryProperty] || '';
    const description = place[descriptionProperty] || 'No description available';
    const amenities = place[amenitiesProperty] || [];
    const imageUrl = place[imageProperty] || '';
    
    // Format created_at date if available
    let formattedDate = '';
    if (place[createdAtProperty]) {
        const date = new Date(place[createdAtProperty]);
        formattedDate = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    // Display image if available
    const imageHtml = imageUrl 
        ? `<img src="${imageUrl}" alt="${name}" class="place-image">`
        : '';
    
    placeDetails.innerHTML = `
        <h1>${name}</h1>
        ${imageHtml}
        <div class="place-info">
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Price:</strong> $${price} per night</p>
            <p><strong>Location:</strong> ${city}${city && country ? ', ' : ''}${country}</p>
            <p><strong>Since:</strong> ${formattedDate || 'Not specified'}</p>
            <p><strong>Description:</strong> ${description}</p>
            
            <div class="amenities">
                <h3>Amenities:</h3>
                <ul>
                    ${Array.isArray(amenities) && amenities.length 
                        ? amenities.map(amenity => `<li>${amenity}</li>`).join('') 
                        : '<li>No amenities listed</li>'}
                </ul>
            </div>
        </div>
    `;
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
    
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    
    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
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
        
        // Initially set username as 'Anonymous' while we fetch the actual name
        let userName = 'Anonymous';
        
        // Create the initial review card with placeholder for username
        reviewCard.innerHTML = `
            <h3>${userName}</h3>
            <p class="review-date">${formattedDate || ''}</p>
            <p>${text}</p>
            <div class="rating ${ratingColorClass}">${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</div>
        `;
        
        reviewsSection.appendChild(reviewCard);
        
        // If we have a userId, try to fetch the user's name
        if (userId) {
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
                const nameProperty = findPropertyByPriority(userData, ['name', 'first_name', 'username', 'email']);
                userName = userData[nameProperty] || 'Anonymous';
                
                // Update the username in the review card
                const usernameElement = document.querySelector(`#review-${index} h3`);
                if (usernameElement) {
                    usernameElement.textContent = userName;
                }
            })
            .catch(error => {
                console.error(`Error fetching user data for review ${index}:`, error);
                // Leave username as Anonymous if we can't fetch it
            });
        }
    });
    
    // Add CSS for rating colors
    if (!document.getElementById('rating-styles')) {
        const style = document.createElement('style');
        style.id = 'rating-styles';
        style.textContent = `
            .rating-high { color: #28a745; }
            .rating-medium { color: #ffc107; }
            .rating-low { color: #dc3545; }
            .review-date { color: #6c757d; font-size: 0.9em; margin-top: -0.5em; }
        `;
        document.head.appendChild(style);
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