// Main JavaScript for IIC Website

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - initializing members functionality');
    
    // Initialize all functions
    initMembersViewMore();
    initMemberSearch();
    
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navSection = document.getElementById('nav-section');
    
    if (mobileMenuBtn && navSection) {
        mobileMenuBtn.addEventListener('click', function() {
            navSection.classList.toggle('active');
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.replace('fa-bars', 'fa-times');
            } else {
                icon.classList.replace('fa-times', 'fa-bars');
            }
        });
    }

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 1024) {
                navSection.classList.remove('active');
                mobileMenuBtn.querySelector('i').classList.replace('fa-times', 'fa-bars');
            }
        });
    });

    // Close flash messages
    document.querySelectorAll('.flash-close').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash-message').forEach(message => {
            message.style.display = 'none';
        });
    }, 5000);

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });

    // Back to top button
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Initialize testimonials carousel
    initTestimonialsCarousel();

    // Initialize scroll animations
    initScrollAnimations();

    // Initialize header scroll effect
    initHeaderScroll();

    // Initialize tabs
    initTabs();
});

// Members View More/Less Functionality
function initMembersViewMore() {
    const viewMoreBtn = document.getElementById('view-more-btn');
    const viewLessBtn = document.getElementById('view-less-btn');
    const additionalMembers = document.querySelectorAll('.additional-member');
    
    console.log('View More Button:', viewMoreBtn);
    console.log('View Less Button:', viewLessBtn);
    console.log('Additional Members found:', additionalMembers.length);
    
    // If no additional members, hide both buttons
    if (additionalMembers.length === 0) {
        if (viewMoreBtn) viewMoreBtn.style.display = 'none';
        if (viewLessBtn) viewLessBtn.style.display = 'none';
        console.log('No additional members - hiding both buttons');
        return;
    }
    
    if (viewMoreBtn) {
        viewMoreBtn.addEventListener('click', function() {
            console.log('View More clicked - showing additional members');
            // Show all additional members
            additionalMembers.forEach(member => {
                member.style.display = '';
            });
            
            // Hide view more button, show view less button
            viewMoreBtn.style.display = 'none';
            if (viewLessBtn) viewLessBtn.style.display = 'inline-block';
        });
    }
    
    if (viewLessBtn) {
        viewLessBtn.addEventListener('click', function() {
            console.log('View Less clicked - hiding additional members');
            // Hide additional members
            additionalMembers.forEach(member => {
                member.style.display = 'none';
            });
            
            // Show view more button, hide view less button
            if (viewMoreBtn) viewMoreBtn.style.display = 'inline-block';
            viewLessBtn.style.display = 'none';
        });
    }
}

// Member Search and Filter
function initMemberSearch() {
    const searchInput = document.getElementById('member-search');
    const roleFilter = document.getElementById('role-filter');
    const memberRows = document.querySelectorAll('.member-row');
    const viewMoreBtn = document.getElementById('view-more-btn');
    const viewLessBtn = document.getElementById('view-less-btn');

    console.log('Search input:', searchInput);
    console.log('Role filter:', roleFilter);
    console.log('Member rows for search:', memberRows.length);

    if (!searchInput || !roleFilter || !memberRows.length) {
        console.log('Search/filter initialization failed - missing elements');
        return;
    }

    function filterMembers() {
        const searchTerm = searchInput.value.toLowerCase();
        const roleValue = roleFilter.value;
        let visibleCount = 0;
        let hasAdditionalMembers = false;

        console.log('Filtering - Search term:', searchTerm, 'Role:', roleValue);

        memberRows.forEach(row => {
            const name = row.cells[0].textContent.toLowerCase();
            const role = row.cells[1].textContent;
            const branch = row.cells[2].textContent.toLowerCase();
            const email = row.cells[4].textContent.toLowerCase();

            const matchesSearch = name.includes(searchTerm) || 
                                branch.includes(searchTerm) || 
                                email.includes(searchTerm);
            const matchesRole = !roleValue || role === roleValue;

            if (matchesSearch && matchesRole) {
                row.style.display = '';
                visibleCount++;
                
                // Check if this is an additional member
                if (row.classList.contains('additional-member')) {
                    hasAdditionalMembers = true;
                }
            } else {
                row.style.display = 'none';
            }
        });

        console.log('Visible members after filtering:', visibleCount);
        console.log('Has additional members in results:', hasAdditionalMembers);

        // Handle view more/less buttons during search
        if (searchTerm || roleValue) {
            // When searching/filtering, show all matching results and hide view buttons
            console.log('Search/filter active - hiding view buttons');
            if (viewMoreBtn) viewMoreBtn.style.display = 'none';
            if (viewLessBtn) viewLessBtn.style.display = 'none';
        } else {
            // When no search/filter, show view more button if there are additional members
            if (hasAdditionalMembers && viewMoreBtn) {
                console.log('No search/filter - showing view more button');
                viewMoreBtn.style.display = 'inline-block';
                if (viewLessBtn) viewLessBtn.style.display = 'none';
                
                // Hide additional members by default
                document.querySelectorAll('.additional-member').forEach(member => {
                    member.style.display = 'none';
                });
            } else {
                console.log('No search/filter - hiding view buttons');
                if (viewMoreBtn) viewMoreBtn.style.display = 'none';
                if (viewLessBtn) viewLessBtn.style.display = 'none';
            }
        }
    }

    searchInput.addEventListener('input', filterMembers);
    roleFilter.addEventListener('change', filterMembers);
    
    // Initial filter to set up the correct state
    filterMembers();
}

// Testimonials Carousel
function initTestimonialsCarousel() {
    const slider = document.getElementById('testimonialsSlider');
    const dots = document.querySelectorAll('.testimonial-dot');
    const prevBtn = document.getElementById('testimonialPrev');
    const nextBtn = document.getElementById('testimonialNext');
    
    if (!slider || !dots.length) return;

    let currentSlide = 0;
    const slides = document.querySelectorAll('.testimonial-slide');
    const totalSlides = slides.length;

    function goToSlide(index) {
        currentSlide = (index + totalSlides) % totalSlides;
        slider.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Auto-play
    let autoPlay = setInterval(() => goToSlide(currentSlide + 1), 5000);

    // Pause on hover
    const testimonialsContainer = document.querySelector('.testimonials-container');
    if (testimonialsContainer) {
        testimonialsContainer.addEventListener('mouseenter', () => clearInterval(autoPlay));
        testimonialsContainer.addEventListener('mouseleave', () => {
            autoPlay = setInterval(() => goToSlide(currentSlide + 1), 5000);
        });
    }
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .zoom-in').forEach(el => {
        observer.observe(el);
    });
}

// Header Scroll Effect
function initHeaderScroll() {
    const header = document.getElementById('main-header');
    if (!header) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    });
}

// Tabs Functionality
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to current tab and content
            this.classList.add('active');
            document.getElementById(`${tabId}-content`).classList.add('active');
        });
    });
}

// Handle window resize for mobile menu
window.addEventListener('resize', function() {
    const navSection = document.getElementById('nav-section');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (window.innerWidth > 1024) {
        navSection.classList.remove('active');
        if (mobileMenuBtn) {
            mobileMenuBtn.querySelector('i').classList.replace('fa-times', 'fa-bars');
        }
    }
});