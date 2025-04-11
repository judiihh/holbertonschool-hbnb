// Simple debug JavaScript to check if scripts are loading
console.log('Debug script loaded successfully!');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded!');
    
    // Add a message to the page
    const debugMessage = document.createElement('div');
    debugMessage.style.padding = '10px';
    debugMessage.style.margin = '10px';
    debugMessage.style.backgroundColor = '#f0f0f0';
    debugMessage.style.border = '1px solid #ddd';
    debugMessage.innerHTML = '<strong>Debug:</strong> JavaScript is working!';
    
    // Get the main element and prepend the message
    const main = document.querySelector('main');
    if (main) {
        main.prepend(debugMessage);
    }
}); 