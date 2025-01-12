// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('nav');
    const container = document.querySelector('.container');
    const overlay = document.querySelector('.nav-overlay');

    if (!navToggle || !nav || !overlay) {
        console.error('Required navigation elements not found');
        return;
    }

    // Toggle navigation function
    function toggleNav() {
        navToggle.classList.toggle('open');
        nav.classList.toggle('open');
        if (container) {
            container.classList.toggle('nav-open');
        }
        overlay.classList.toggle('open');
        document.body.style.overflow = nav.classList.contains('open') ? 'hidden' : '';
    }

    // Add event listeners
    navToggle.addEventListener('click', toggleNav);
    overlay.addEventListener('click', toggleNav);

    // Close nav when clicking a link
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
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
});