// Form validation
function validateForm() {
    const form = document.forms["applicationForm"];
    const requiredFields = ["surname", "first_name", "email", "phone_no"];
    
    for (let field of requiredFields) {
        if (!form[field].value) {
            alert(`${field.replace('_', ' ')} is required.`);
            form[field].focus();
            return false;
        }
    }

    const email = form["email"].value;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert("Please enter a valid email address.");
        form["email"].focus();
        return false;
    }

    const phone = form["phone_no"].value;
    if (phone.length < 10) {
        alert("Phone number must be at least 10 digits.");
        form["phone_no"].focus();
        return false;
    }

    return true;
}

// Carousel functionality
document.addEventListener('DOMContentLoaded', () => {
    const carouselItems = document.querySelectorAll('.carousel-item');
    const prevButton = document.querySelector('.carousel-prev');
    const nextButton = document.querySelector('.carousel-next');
    let currentIndex = 0;

    function showSlide(index) {
        carouselItems.forEach((item, i) => {
            item.classList.toggle('active', i === index);
            item.classList.toggle('hidden', i !== index);
        });
    }

    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex === 0) ? carouselItems.length - 1 : currentIndex - 1;
        showSlide(currentIndex);
    });

    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex === carouselItems.length - 1) ? 0 : currentIndex + 1;
        showSlide(currentIndex);
    });

    // Auto-rotate every 5 seconds
    setInterval(() => {
        currentIndex = (currentIndex === carouselItems.length - 1) ? 0 : currentIndex + 1;
        showSlide(currentIndex);
    }, 5000);
});