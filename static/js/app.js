/**
 * BookSphere Vanilla JavaScript Client
 * Handles asynchronous bookmarking, modal preview reading, and DOM interactions.
 */

// CSRF Cookie Extraction for Django AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Toggle book bookmark asynchronously via REST API
 */
async function toggleBookmark(event, bookId) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    const csrftoken = getCookie('csrftoken');
    const btn = event ? event.currentTarget : document.getElementById('bookmarkToggleBtn');

    try {
        const response = await fetch(`/api/books/${bookId}/bookmark/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            window.location.href = '/login/?next=' + window.location.pathname;
            return;
        }

        const data = await response.json();
        if (data.status === 'success') {
            // Update button UI
            if (data.is_saved) {
                btn.classList.add('saved');
                if (btn.querySelector('#bookmarkIcon')) {
                    btn.querySelector('#bookmarkIcon').innerText = '❤️ Saved in Library';
                } else {
                    btn.innerText = '❤️';
                }
            } else {
                btn.classList.remove('saved');
                if (btn.querySelector('#bookmarkIcon')) {
                    btn.querySelector('#bookmarkIcon').innerText = '🤍 Save to My Reading List';
                } else {
                    btn.innerText = '🤍';
                }
            }
        }
    } catch (err) {
        console.error('Error toggling bookmark:', err);
    }
}

/**
 * Sample Excerpt Reader Modal Handlers
 */
function openReaderModal() {
    const modal = document.getElementById('readerModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeReaderModal() {
    const modal = document.getElementById('readerModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function closeReaderModalOnBackdrop(event) {
    if (event.target.id === 'readerModal') {
        closeReaderModal();
    }
}

// Global Keyboard Escape Listener
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeReaderModal();
    }
});

// Auto-dismiss Flash Alerts after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
});
