// Landing Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and interactions
    initScrollAnimations();
    initNavbarEffects();
    initParallaxEffects();
    initInteractiveElements();
    initTypewriterEffect();
});

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Staggered animation for feature cards
                if (entry.target.classList.contains('feature-card')) {
                    const cards = document.querySelectorAll('.feature-card');
                    const index = Array.from(cards).indexOf(entry.target);
                    setTimeout(() => {
                        entry.target.style.transform = 'translateY(0) scale(1)';
                        entry.target.style.opacity = '1';
                    }, index * 100);
                }
            }
        });
    }, observerOptions);

    // Observe all elements that need animation
    document.querySelectorAll('.feature-card, .step').forEach(el => {
        observer.observe(el);
    });

    // Only animate floating cards opacity on scroll
    window.addEventListener('scroll', () => {
        const windowHeight = window.innerHeight;
        // Opacity effect for floating cards
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            const cardRect = card.getBoundingClientRect();
            const opacity = Math.max(0, Math.min(1, (windowHeight - cardRect.top) / windowHeight));
            card.style.opacity = opacity;
        });
    });
}

// Navbar Effects
function initNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        // Add/remove scrolled class for styling
        if (currentScrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        // Hide/show navbar on scroll
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        lastScrollY = currentScrollY;
    });
}

// Parallax Effects
function initParallaxEffects() {
    const orbs = document.querySelectorAll('.gradient-orb');
    const parallaxLayers = document.querySelectorAll('.parallax-layer');
    const floatingCards = document.querySelectorAll('.card');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        // Animate gradient orbs
        orbs.forEach((orb, index) => {
            const speed = 0.5 + (index * 0.1);
            orb.style.transform = `translateY(${rate * speed}px)`;
        });
        // Animate parallax layers
        parallaxLayers.forEach((layer, index) => {
            const speed = (index + 1) * 0.1;
            const yPos = scrolled * speed;
            layer.style.transform = `translateY(${yPos}px) translateZ(-${(index + 1) * 5}px) scale(${1 + index * 0.2})`;
        });
        // Animate floating cards with different speeds
        floatingCards.forEach((card, index) => {
            const speed = 0.3 + (index * 0.1);
            const yPos = scrolled * speed;
            const xPos = scrolled * (speed * 0.5);
            card.style.transform = `translateY(${yPos}px) translateX(${xPos}px)`;
        });
    });
}

// Interactive Elements
function initInteractiveElements() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    // Button hover effects
    document.querySelectorAll('.primary-button, .secondary-button').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    // Card hover effects
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Typewriter Effect for Hero Title
function initTypewriterEffect() {
    const titleLines = document.querySelectorAll('.title-line');
    titleLines.forEach((line, index) => {
        const text = line.textContent;
        line.textContent = '';
        line.style.opacity = '1';
        setTimeout(() => {
            typeWriter(line, text, 0, 50);
        }, index * 800);
    });
}
function typeWriter(element, text, i, speed) {
    if (i < text.length) {
        element.textContent += text.charAt(i);
        setTimeout(() => typeWriter(element, text, i + 1, speed), speed);
    }
}
// Scroll to Features Function
function scrollToFeatures() {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
        featuresSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}
// Mouse Movement Effects
document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    // Subtle parallax effect on floating cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        const speed = 0.02 + (index * 0.01);
        const x = (mouseX - 0.5) * speed * 100;
        const y = (mouseY - 0.5) * speed * 100;
        card.style.transform += ` translate(${x}px, ${y}px)`;
    });
});
// Loading Animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    // Animate hero elements sequentially
    const heroElements = document.querySelectorAll('.hero-title, .hero-subtitle, .hero-actions');
    heroElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
});
// Particle System Enhancement
function createParticles() {
    const particlesContainer = document.querySelector('.particles');
    const particleCount = 50;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: particleFloat ${5 + Math.random() * 10}s linear infinite;
        `;
        particlesContainer.appendChild(particle);
    }
}
// Enhanced floating animation for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes particleFloat {
        0% {
            transform: translateY(0px) translateX(0px);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) translateX(100px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
// Initialize particles
createParticles();
// Performance optimization
let ticking = false;
function updateAnimations() {
    if (!ticking) {
        requestAnimationFrame(() => {
            // Update any performance-critical animations here
            ticking = false;
        });
        ticking = true;
    }
}
// Throttled scroll listener for performance
let scrollTimeout;
window.addEventListener('scroll', () => {
    if (scrollTimeout) {
        clearTimeout(scrollTimeout);
    }
    scrollTimeout = setTimeout(updateAnimations, 16);
});
// Add CSS for navbar scrolled state
const navbarStyle = document.createElement('style');
navbarStyle.textContent = `
    .navbar.scrolled {
        background: rgba(10, 10, 10, 0.95);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .navbar {
        transition: all 0.3s ease;
    }
    
    body.loaded .hero-title,
    body.loaded .hero-subtitle,
    body.loaded .hero-actions {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease;
    }
`;
document.head.appendChild(navbarStyle); 