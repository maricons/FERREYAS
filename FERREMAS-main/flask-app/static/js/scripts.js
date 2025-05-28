// Back to Top Button Functionality
document.addEventListener('DOMContentLoaded', () => {
    const backToTopButton = document.createElement('button');
    backToTopButton.id = 'back-to-top';
    backToTopButton.textContent = 'Back to Top';
    document.body.appendChild(backToTopButton);

    // Show/hide button on scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });

    // Scroll smoothly to top when button clicked
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Fade-in effect for product details
    const productInfo = document.querySelector('.product-info');
    if (productInfo) {
        setTimeout(() => {
            productInfo.style.transition = 'opacity 0.5s ease-in-out';
            productInfo.style.opacity = 1;
        }, 100);
    }
});