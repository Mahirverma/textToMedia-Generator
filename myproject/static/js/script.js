// Helper function to update the progress bar
function updateProgressBar(progress) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
        progressBar.innerHTML = `${progress}%`; // Display percentage inside the bar
    }
}

// Function to show notifications
function showNotification(message, type) {
    const notificationContainer = document.createElement('div');
    notificationContainer.classList.add('notification');
    notificationContainer.classList.add(type);

    notificationContainer.innerHTML = `
        <p>${message}</p>
    `;

    document.body.appendChild(notificationContainer);

    // Automatically remove the notification after 5 seconds
    setTimeout(() => {
        notificationContainer.remove();
    }, 5000);
}

// Handle user login
document.querySelector('#login-form')?.addEventListener('submit', function (event) {
    event.preventDefault();
    const userId = document.querySelector('#user_id').value;
    if (!userId) {
        showNotification('Please enter your User ID to log in.', 'error');
    } else {
        // Perform login logic here
        // Example: Make an API call to check if user exists
        showNotification(`Welcome, ${userId}! You are logged in.`, 'success');
        window.location.href = `/user/${userId}/gallery`;  // Redirect to user's gallery
    }
});

// Handle form submission for content generation request
document.querySelector('#generate-form')?.addEventListener('submit', function (event) {
    event.preventDefault();
    const prompt = document.querySelector('#prompt').value;
    if (!prompt) {
        showNotification('Please provide a prompt for content generation.', 'error');
    } else {
        // Send a request to start content generation
        showNotification('Your content is being generated. Please wait.', 'info');

        // Mock API call - Update progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            updateProgressBar(progress);

            if (progress >= 100) {
                clearInterval(interval);
                showNotification('Content generation completed!', 'success');
            }
        }, 1000);
    }
});

// Displaying video preview
const videoItems = document.querySelectorAll('.video-item video');
videoItems.forEach(video => {
    video.addEventListener('click', function () {
        // Display the video in a larger view or play it
        video.play();
    });
});

// Handling image click for viewing in a modal
const imageItems = document.querySelectorAll('.image-item img');
imageItems.forEach(image => {
    image.addEventListener('click', function () {
        const imageSrc = image.src;
        showImageModal(imageSrc);
    });
});

// Function to show an image modal
function showImageModal(imageSrc) {
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-btn">&times;</span>
            <img src="${imageSrc}" alt="Image Preview">
        </div>
    `;
    document.body.appendChild(modal);

    // Close the modal on clicking the close button
    modal.querySelector('.close-btn').addEventListener('click', function () {
        modal.remove();
    });

    // Close the modal if the user clicks outside of the image
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.remove();
        }
    });
}

// Auto-close notifications after a timeout
setTimeout(function () {
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        notification.remove();
    });
}, 5000);

// Track user content view (for gallery page)
document.querySelector('.view-content-btn')?.addEventListener('click', function () {
    const userId = this.getAttribute('data-user-id');
    if (userId) {
        console.log(`User ${userId} is viewing their content.`);
        // Call API to log the user's content view
    }
});
