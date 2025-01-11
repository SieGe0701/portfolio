// Add these elements to your HTML first
document.body.insertAdjacentHTML('beforeend', '<div class="nav-overlay"></div>');
document.body.insertAdjacentHTML('afterbegin', `
    <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span>
        <span></span>
        <span></span>
    </button>
`);

// Get elements
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('nav');
const container = document.querySelector('.container');
const overlay = document.querySelector('.nav-overlay');

// Toggle navigation
function toggleNav() {
    navToggle.classList.toggle('open');
    nav.classList.toggle('open');
    container.classList.toggle('nav-open');
    overlay.classList.toggle('open');
    document.body.style.overflow = nav.classList.contains('open') ? 'hidden' : '';
}

// Event listeners
navToggle.addEventListener('click', toggleNav);
overlay.addEventListener('click', toggleNav);

// Close nav when clicking a link
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', () => {
        if (nav.classList.contains('open')) {
            toggleNav();
        }
    });
});

// Close nav when screen is resized above mobile breakpoint
window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && nav.classList.contains('open')) {
        toggleNav();
    }
});