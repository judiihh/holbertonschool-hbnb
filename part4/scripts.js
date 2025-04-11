// Handle login form submission
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            await loginUser(email, password);
        } catch (error) {
            showError('An error occurred during login. Please try again.');
        }
    });
}

// Handle price filter
const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
    priceFilter.addEventListener('change', async () => {
        const maxPrice = priceFilter.value;
        try {
            const response = await fetch(`http://localhost:5000/api/v1/places${maxPrice !== 'all' ? `?max_price=${maxPrice}` : ''}`);
            if (response.ok) {
                const places = await response.json();
                updatePlacesList(places);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

// Handle review form submission
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const review = document.getElementById('review').value;
        const rating = document.getElementById('rating').value;
        const placeId = new URLSearchParams(window.location.search).get('id');

        try {
            const token = getCookie('auth_token');
            if (!token) {
                window.location.href = 'login.html';
                return;
            }

            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ text: review, rating: parseInt(rating) }),
            });

            if (response.ok) {
                window.location.href = `place.html?id=${placeId}`;
            } else {
                alert('Failed to submit review');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while submitting the review');
        }
    });
}

// Helper function to get cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Helper function to update places list
function updatePlacesList(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = places.map(place => `
        <div class="place-card">
            <h2>${place.name}</h2>
            <p class="price">Price per night: $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        </div>
    `).join('');
}

// Check authentication status and update UI accordingly
function updateAuthUI() {
    const token = getCookie('auth_token');
    const loginButton = document.querySelector('.login-button');
    
    if (loginButton) {
        if (token) {
            loginButton.textContent = 'Logout';
            loginButton.href = '#';
            loginButton.addEventListener('click', (e) => {
                e.preventDefault();
                document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                window.location.reload();
            });
        } else {
            loginButton.textContent = 'Login';
            loginButton.href = 'login.html';
        }
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();

    // Check authentication and initialize index page functionality
    checkAuthentication();

    // Initialize price filter if it exists
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', handlePriceFilter);
    }

    // Initialize place details if we're on the place details page
    if (document.querySelector('.place-details')) {
        initializePlaceDetails();
    }

    // Initialize review form if we're on the add review page
    if (document.querySelector('.review-form')) {
        initializeReviewForm();
    }

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const token = checkAuthenticationAndRedirect();
            if (!token) return; // User will be redirected if not authenticated

            const placeId = getPlaceIdFromURL();
            if (!placeId) {
                showError('No place specified for review.');
                return;
            }

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText) {
                showError('Please enter your review text.');
                return;
            }

            await submitReview(token, placeId, reviewText, rating);
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5001/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Store the token in a cookie that expires in 24 hours
            const expirationDate = new Date();
            expirationDate.setTime(expirationDate.getTime() + (24 * 60 * 60 * 1000));
            document.cookie = `token=${data.access_token}; expires=${expirationDate.toUTCString()}; path=/`;
            
            // Redirect to main page
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            showError(errorData.message || 'Login failed. Please check your credentials.');
        }
    } catch (error) {
        throw new Error('Network error or server not responding');
    }
}

function showError(message) {
    // Remove any existing error message
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Create and show new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = 'red';
    errorDiv.style.marginBottom = '1rem';
    errorDiv.textContent = message;

    const form = document.getElementById('login-form');
    form.insertBefore(errorDiv, form.firstChild);
}

// Authentication check
function checkAuthentication() {
    const token = getCookie('token');
    const loginButton = document.querySelector('.login-button');

    if (loginButton) {
        if (!token) {
            loginButton.style.display = 'block';
        } else {
            loginButton.style.display = 'none';
        }
    }

    // If we're on the index page, fetch places
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }
}

// Fetch places from API
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://localhost:5001/api/v1/places', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Display places in the DOM
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = ''; // Clear existing content

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_per_night;

        placeCard.innerHTML = `
            <h2>${place.name}</h2>
            <p class="price">Price per night: $${place.price_per_night}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

// Handle price filter changes
function handlePriceFilter(event) {
    const maxPrice = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseInt(card.dataset.price);
        if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Get place ID from URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Initialize place details page
async function initializePlaceDetails() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.querySelector('.review-form');

    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }

    if (placeId) {
        await fetchPlaceDetails(token, placeId);
    }
}

// Fetch place details from API
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const placeData = await response.json();
            displayPlaceDetails(placeData);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            showError('Failed to load place details. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        showError('An error occurred while loading place details.');
    }
}

// Display place details in the DOM
function displayPlaceDetails(place) {
    // Update place name in h1
    const placeTitle = document.querySelector('h1');
    if (placeTitle) {
        placeTitle.textContent = place.name;
    }

    // Update place details section
    const placeDetails = document.querySelector('.place-details');
    if (placeDetails) {
        const detailsHTML = `
            <div class="place-info">
                <p><strong>Location:</strong> ${place.location}</p>
                <p><strong>Description:</strong> ${place.description}</p>
                <p><strong>Price per night:</strong> $${place.price_per_night}</p>
                <p><strong>Max guests:</strong> ${place.max_guests}</p>
                <p><strong>Rooms:</strong> ${place.rooms}</p>
                <p><strong>Bathrooms:</strong> ${place.bathrooms}</p>
            </div>
            <div class="amenities">
                <h2>Amenities</h2>
                <ul>
                    ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
                </ul>
            </div>
        `;
        placeDetails.innerHTML = detailsHTML;
    }

    // Update reviews section
    const reviewsSection = document.querySelector('.reviews-section');
    if (reviewsSection && place.reviews) {
        const reviewsHTML = `
            <h2>Reviews</h2>
            ${place.reviews.map(review => `
                <div class="review-card">
                    <h3>${review.user_name}</h3>
                    <p>${review.text}</p>
                    <div class="rating" aria-label="${review.rating} out of 5 stars">
                        <strong>Rating:</strong> ${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}
                    </div>
                </div>
            `).join('')}
        `;
        reviewsSection.innerHTML = reviewsHTML;
    }
}

// Initialize review form page
function initializeReviewForm() {
    const token = checkAuthenticationAndRedirect();
    if (!token) return; // User will be redirected if not authenticated

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        showError('No place specified for review.');
        window.location.href = 'index.html';
        return;
    }

    // Fetch place details to show the place name
    fetchPlaceNameForReview(token, placeId);
}

// Enhanced authentication check with redirect
function checkAuthenticationAndRedirect() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

// Fetch place name for the review form
async function fetchPlaceNameForReview(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const placeData = await response.json();
            updateReviewFormTitle(placeData.name);
        } else {
            showError('Failed to load place information.');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        showError('An error occurred while loading place information.');
    }
}

// Update the review form title with place name
function updateReviewFormTitle(placeName) {
    const titleElement = document.querySelector('h1');
    if (titleElement) {
        titleElement.textContent = `Reviewing: ${placeName}`;
    }
}

// Submit review to API
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        if (response.ok) {
            showSuccess('Review submitted successfully!');
            // Clear the form
            document.getElementById('review-form').reset();
            // Redirect back to place details after a short delay
            setTimeout(() => {
                window.location.href = `place.html?id=${placeId}`;
            }, 2000);
        } else {
            const errorData = await response.json();
            showError(errorData.message || 'Failed to submit review. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('An error occurred while submitting your review.');
    }
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.color = 'green';
    successDiv.style.marginBottom = '1rem';
    successDiv.textContent = message;

    const form = document.getElementById('review-form');
    if (form) {
        form.insertBefore(successDiv, form.firstChild);
    }
} 