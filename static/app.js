/**
 * Modern Astrology UI - Interactive Features
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeAnimations();
    initializeTooltips();
});

/**
 * Tab Navigation System
 */
function initializeTabs() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Remove active class from all buttons and tabs
            navButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));

            // Add active class to clicked button and corresponding tab
            this.classList.add('active');
            const targetTabContent = document.getElementById(targetTab);
            if (targetTabContent) {
                targetTabContent.classList.add('active');

                // Smooth scroll to top of content
                targetTabContent.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Store active tab in localStorage for persistence
            localStorage.setItem('activeTab', targetTab);
        });
    });

    // Restore last active tab
    const savedTab = localStorage.getItem('activeTab');
    if (savedTab) {
        const savedButton = document.querySelector(`[data-tab="${savedTab}"]`);
        const savedContent = document.getElementById(savedTab);

        if (savedButton && savedContent) {
            navButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));

            savedButton.classList.add('active');
            savedContent.classList.add('active');
        }
    }
}

/**
 * Smooth Animations and Interactions
 */
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards for animation
    const animatedElements = document.querySelectorAll(
        '.summary-card, .overview-card, .planet-modern-card, .prediction-card'
    );

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add hover effects to interactive elements
    addHoverEffects();
}

/**
 * Add hover effects to cards
 */
function addHoverEffects() {
    const cards = document.querySelectorAll(
        '.summary-card, .overview-card, .planet-modern-card, .remedy-card'
    );

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
            this.style.boxShadow = '0 20px 25px -5px rgb(0 0 0 / 0.2), 0 8px 10px -6px rgb(0 0 0 / 0.2)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
        });
    });
}

/**
 * Tooltip System for Additional Information
 */
function initializeTooltips() {
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: var(--bg-tertiary);
        color: var(--text-primary);
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        box-shadow: var(--shadow-lg);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.2s ease;
        z-index: 1000;
        max-width: 250px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    `;
    document.body.appendChild(tooltip);

    // Add tooltips to elements with data-tooltip attribute
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const text = this.getAttribute('data-tooltip');
            tooltip.textContent = text;
            tooltip.style.opacity = '1';

            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        });

        element.addEventListener('mouseleave', function() {
            tooltip.style.opacity = '0';
        });
    });
}

/**
 * Keyboard Navigation Support
 */
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        // Add focus styles for keyboard navigation
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    // Remove focus styles when using mouse
    document.body.classList.remove('keyboard-navigation');
});

/**
 * Smooth Scrolling for Internal Links
 */
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Loading States and Performance
 */
function showLoadingState(element) {
    element.style.opacity = '0.6';
    element.style.pointerEvents = 'none';
}

function hideLoadingState(element) {
    element.style.opacity = '1';
    element.style.pointerEvents = 'auto';
}

/**
 * Responsive Navigation for Mobile
 */
function initializeMobileNavigation() {
    const navContainer = document.querySelector('.nav-container');
    let isScrolling = false;

    // Add smooth scrolling to navigation on mobile
    navContainer.addEventListener('scroll', function() {
        if (!isScrolling) {
            window.requestAnimationFrame(function() {
                // Add any scroll-based animations here
                isScrolling = false;
            });
            isScrolling = true;
        }
    });
}

/**
 * Theme Persistence
 */
function initializeTheme() {
    // Future: Add theme switching capability
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // The app is designed for dark theme by default
    // This function is prepared for future light theme support
}

/**
 * Performance Monitoring
 */
function initializePerformanceMonitoring() {
    // Monitor page load performance
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);

        // You could send this data to analytics
        // analytics.track('page_load_time', { duration: loadTime });
    });
}

/**
 * Error Handling
 */
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // In production, you might want to send errors to a logging service
});

/**
 * Planetary Details Toggle
 */
function togglePlanetDetails(planetName) {
    const detailsElement = document.getElementById(`details-${planetName}`);
    const button = document.querySelector(`button[onclick="togglePlanetDetails('${planetName}')"]`);

    if (detailsElement.style.display === 'none' || detailsElement.style.display === '') {
        detailsElement.style.display = 'block';
        button.textContent = '🔼 Hide Detailed Analysis';

        // Smooth scroll to the details
        setTimeout(() => {
            detailsElement.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }, 100);
    } else {
        detailsElement.style.display = 'none';
        button.textContent = '🔍 View Detailed Analysis';
    }
}

/**
 * Remedy Tab System
 */
function showRemedyTab(planetName, tabType) {
    // Hide all remedy tabs for this planet
    const allTabs = document.querySelectorAll(`[id^="remedy-${planetName}-"]`);
    allTabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons for this planet
    const allButtons = document.querySelectorAll(`button[onclick*="${planetName}"]`);
    allButtons.forEach(btn => {
        if (btn.onclick && btn.onclick.toString().includes('showRemedyTab')) {
            btn.classList.remove('active');
        }
    });

    // Show the selected tab
    const targetTab = document.getElementById(`remedy-${planetName}-${tabType}`);
    if (targetTab) {
        targetTab.classList.add('active');
    }

    // Add active class to the clicked button
    const targetButton = document.querySelector(`button[onclick="showRemedyTab('${planetName}', '${tabType}')"]`);
    if (targetButton) {
        targetButton.classList.add('active');
    }
}

/**
 * Enhanced Tab System with URL Hash Support
 */
function initializeEnhancedTabs() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Remove active class from all buttons and tabs
            navButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));

            // Add active class to clicked button and corresponding tab
            this.classList.add('active');
            const targetTabContent = document.getElementById(targetTab);
            if (targetTabContent) {
                targetTabContent.classList.add('active');

                // Update URL hash
                window.history.replaceState(null, null, `#${targetTab}`);

                // Smooth scroll to top of content
                targetTabContent.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Store active tab in localStorage for persistence
            localStorage.setItem('activeTab', targetTab);
        });
    });

    // Handle URL hash on page load
    const hash = window.location.hash.substring(1);
    if (hash) {
        const hashButton = document.querySelector(`[data-tab="${hash}"]`);
        const hashContent = document.getElementById(hash);

        if (hashButton && hashContent) {
            navButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));

            hashButton.classList.add('active');
            hashContent.classList.add('active');
            localStorage.setItem('activeTab', hash);
        }
    } else {
        // Restore last active tab
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab) {
            const savedButton = document.querySelector(`[data-tab="${savedTab}"]`);
            const savedContent = document.getElementById(savedTab);

            if (savedButton && savedContent) {
                navButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(tab => tab.classList.remove('active'));

                savedButton.classList.add('active');
                savedContent.classList.add('active');
            }
        }
    }
}

/**
 * Enhanced Animations with Intersection Observer
 */
function initializeEnhancedAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';

                // Add staggered animation for grid items
                if (entry.target.classList.contains('stagger-animation')) {
                    const children = entry.target.children;
                    Array.from(children).forEach((child, index) => {
                        setTimeout(() => {
                            child.style.opacity = '1';
                            child.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                }
            }
        });
    }, observerOptions);

    // Observe all cards and sections for animation
    const animatedElements = document.querySelectorAll(`
        .summary-card, .overview-card, .planet-modern-card, .prediction-card,
        .remedy-card, .personality-influence-card, .theme-detailed-card,
        .today-card, .house-transit-card, .yoga-transit-card
    `);

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add stagger animation class to grids
    const grids = document.querySelectorAll(`
        .summary-grid, .overview-grid, .planets-modern-grid, .remedies-grid,
        .themes-detailed-grid, .today-grid, .house-transits-grid
    `);

    grids.forEach(grid => {
        grid.classList.add('stagger-animation');
        observer.observe(grid);
    });
}

/**
 * Enhanced Hover Effects
 */
function initializeEnhancedHoverEffects() {
    const interactiveCards = document.querySelectorAll(`
        .summary-card, .overview-card, .planet-modern-card, .remedy-card,
        .personality-influence-card, .theme-detailed-card, .today-card,
        .house-transit-card, .yoga-transit-card
    `);

    interactiveCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
            this.style.boxShadow = '0 20px 25px -5px rgb(0 0 0 / 0.2), 0 8px 10px -6px rgb(0 0 0 / 0.2)';
            this.style.zIndex = '10';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
            this.style.zIndex = '1';
        });
    });

    // Special hover effects for buttons
    const buttons = document.querySelectorAll('.expand-details-btn, .remedy-tab-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
}

/**
 * Enhanced Tooltips with Rich Content
 */
function initializeEnhancedTooltips() {
    // Create enhanced tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'enhanced-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: var(--bg-tertiary);
        color: var(--text-primary);
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.875rem;
        box-shadow: var(--shadow-xl);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        z-index: 1000;
        max-width: 300px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transform: translateY(10px);
    `;
    document.body.appendChild(tooltip);

    // Add tooltips to elements with data-tooltip attribute
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const text = this.getAttribute('data-tooltip');
            tooltip.innerHTML = text;
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';

            // Position tooltip
            const rect = this.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();

            let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
            let top = rect.top - tooltipRect.height - 12;

            // Adjust if tooltip goes off screen
            if (left < 10) left = 10;
            if (left + tooltipRect.width > window.innerWidth - 10) {
                left = window.innerWidth - tooltipRect.width - 10;
            }
            if (top < 10) {
                top = rect.bottom + 12;
            }

            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';
        });

        element.addEventListener('mouseleave', function() {
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(10px)';
        });
    });
}

/**
 * Initialize all features
 */
function initializeApp() {
    initializeEnhancedTabs();
    initializeEnhancedAnimations();
    initializeEnhancedHoverEffects();
    initializeEnhancedTooltips();
    initializeSmoothScrolling();
    initializeMobileNavigation();
    initializeTheme();
    initializePerformanceMonitoring();
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
