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