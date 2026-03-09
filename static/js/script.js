// ==================== PASSWORD CHECKER ==================== 
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const strengthBar = document.getElementById('strengthBar');
const strengthText = document.getElementById('strengthText');

if (passwordInput) {
    passwordInput.addEventListener('input', checkPasswordStrength);
    togglePassword.addEventListener('click', togglePasswordVisibility);
}

function togglePasswordVisibility() {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
}

function checkPasswordStrength() {
    const password = passwordInput.value;
    let strength = 0;
    let feedback = [];

    // Check length
    const lengthCriteria = document.getElementById('criteria-length');
    if (password.length >= 8) {
        strength += 20;
        lengthCriteria.classList.add('met');
        lengthCriteria.querySelector('.criterion-icon').textContent = '✓';
    } else {
        lengthCriteria.classList.remove('met');
        lengthCriteria.querySelector('.criterion-icon').textContent = '✗';
    }

    // Check uppercase
    const uppercaseCriteria = document.getElementById('criteria-uppercase');
    if (/[A-Z]/.test(password)) {
        strength += 20;
        uppercaseCriteria.classList.add('met');
        uppercaseCriteria.querySelector('.criterion-icon').textContent = '✓';
    } else {
        uppercaseCriteria.classList.remove('met');
        uppercaseCriteria.querySelector('.criterion-icon').textContent = '✗';
    }

    // Check lowercase
    const lowercaseCriteria = document.getElementById('criteria-lowercase');
    if (/[a-z]/.test(password)) {
        strength += 20;
        lowercaseCriteria.classList.add('met');
        lowercaseCriteria.querySelector('.criterion-icon').textContent = '✓';
    } else {
        lowercaseCriteria.classList.remove('met');
        lowercaseCriteria.querySelector('.criterion-icon').textContent = '✗';
    }

    // Check numbers
    const numberCriteria = document.getElementById('criteria-number');
    if (/[0-9]/.test(password)) {
        strength += 20;
        numberCriteria.classList.add('met');
        numberCriteria.querySelector('.criterion-icon').textContent = '✓';
    } else {
        numberCriteria.classList.remove('met');
        numberCriteria.querySelector('.criterion-icon').textContent = '✗';
    }

    // Check special characters
    const specialCriteria = document.getElementById('criteria-special');
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        strength += 20;
        specialCriteria.classList.add('met');
        specialCriteria.querySelector('.criterion-icon').textContent = '✓';
    } else {
        specialCriteria.classList.remove('met');
        specialCriteria.querySelector('.criterion-icon').textContent = '✗';
    }

    // Update strength bar and text
    if (strength === 0) {
        strengthText.textContent = 'Enter a password';
        strengthText.className = 'strength-text';
        strengthBar.style.width = '0%';
        strengthBar.style.backgroundColor = '#e5e7eb';
    } else if (strength < 40) {
        strengthText.textContent = '❌ Weak Password';
        strengthText.className = 'strength-text weak';
        strengthBar.style.width = strength + '%';
        strengthBar.style.backgroundColor = '#ef4444';
        feedback.push('Your password is too weak. Add more characters and special symbols.');
    } else if (strength < 60) {
        strengthText.textContent = '⚠️ Medium Password';
        strengthText.className = 'strength-text medium';
        strengthBar.style.width = strength + '%';
        strengthBar.style.backgroundColor = '#f59e0b';
        feedback.push('Your password is okay, but could be stronger. Consider adding more characters.');
    } else if (strength < 100) {
        strengthText.textContent = '✅ Strong Password';
        strengthText.className = 'strength-text strong';
        strengthBar.style.width = strength + '%';
        strengthBar.style.backgroundColor = '#10b981';
        feedback.push('Excellent! Your password is strong and secure.');
    } else {
        strengthText.textContent = '🔒 Very Strong Password';
        strengthText.className = 'strength-text strong';
        strengthBar.style.width = '100%';
        strengthBar.style.backgroundColor = '#059669';
        feedback.push('Perfect! Your password is very secure.');
    }

    // Display feedback
    const feedbackDiv = document.getElementById('passwordFeedback');
    if (feedbackDiv) {
        feedbackDiv.innerHTML = feedback.length > 0 ? `<p>${feedback[0]}</p>` : '';
    }
}

// ==================== PHISHING CHECKER ==================== 
const urlInput = document.getElementById('url');
const checkUrlBtn = document.getElementById('checkUrlBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultContainer = document.getElementById('resultContainer');

if (checkUrlBtn) {
    checkUrlBtn.addEventListener('click', checkPhishingURL);
    if (urlInput) {
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') checkPhishingURL();
        });
    }
}

function checkPhishingURL() {
    const url = urlInput.value.trim();
    
    if (!url) {
        alert('Please enter a URL');
        return;
    }

    // Show loading
    loadingSpinner.style.display = 'block';
    resultContainer.style.display = 'none';

    // Simulate checking (in real app, this would call backend)
    setTimeout(() => {
        const result = analyzeURL(url);
        displayResult(result);
        loadingSpinner.style.display = 'none';
        resultContainer.style.display = 'block';
    }, 1500);
}

function analyzeURL(url) {
    let isSafe = true;
    let reasons = [];

    // Check for HTTPS
    if (!url.startsWith('https://')) {
        isSafe = false;
        reasons.push('⚠️ Not using HTTPS (secure connection)');
    }

    // Check for suspicious patterns
    const suspiciousPatterns = [
        { pattern: /bit\.ly|tinyurl|short\.url|goo\.gl/i, reason: 'Shortened URL detected' },
        { pattern: /paypa1|g00gle|amaz0n|faceb00k/i, reason: 'Misspelled domain detected' },
        { pattern: /(\d{1,3}\.){3}\d{1,3}/i, reason: 'IP address instead of domain name' },
        { pattern: /password|login|verify|confirm|update|urgent/i, reason: 'Suspicious keywords in URL' }
    ];

    suspiciousPatterns.forEach(item => {
        if (item.pattern.test(url)) {
            isSafe = false;
            reasons.push('⚠️ ' + item.reason);
        }
    });

    // Check domain length (very long domains can be suspicious)
    const domain = url.replace(/https?:\/\//, '').split('/')[0];
    if (domain.length > 30) {
        isSafe = false;
        reasons.push('⚠️ Unusually long domain name');
    }

    // Check for special characters (except . and -)
    if (/[^a-zA-Z0-9.-]/.test(domain)) {
        isSafe = false;
        reasons.push('⚠️ Suspicious special characters in domain');
    }

    return {
        isSafe: isSafe,
        url: url,
        domain: domain,
        reasons: reasons
    };
}

function displayResult(result) {
    const resultCard = document.getElementById('resultCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const resultDetails = document.getElementById('resultDetails');

    if (result.isSafe) {
        resultCard.className = 'result-card safe';
        resultIcon.textContent = '✅';
        resultTitle.textContent = 'URL Appears Safe';
        resultMessage.textContent = 'This URL looks legitimate based on our analysis.';
        resultDetails.innerHTML = `
            <div class="result-details">
                <p><strong>Domain:</strong> ${result.domain}</p>
                <p><strong>Analysis:</strong> No suspicious patterns detected.</p>
                <p style="margin-top: 1rem; color: #059669;"><strong>Note:</strong> This is a basic analysis. Always verify you're on the official website before entering sensitive information.</p>
            </div>
        `;
    } else {
        resultCard.className = 'result-card suspicious';
        resultIcon.textContent = '🚨';
        resultTitle.textContent = 'URL Appears Suspicious';
        resultMessage.textContent = 'This URL has been flagged with potential security concerns.';
        
        let detailsHTML = `
            <div class="result-details">
                <p><strong>Domain:</strong> ${result.domain}</p>
                <p><strong>Warnings Found:</strong></p>
                <ul style="list-style-position: inside; margin: 1rem 0;">
        `;
        
        result.reasons.forEach(reason => {
            detailsHTML += `<li>${reason}</li>`;
        });
        
        detailsHTML += `
                </ul>
                <p style="margin-top: 1rem; color: #ef4444;"><strong>Recommendation:</strong> Do not click this link. Visit the official website directly instead.</p>
            </div>
        `;
        
        resultDetails.innerHTML = detailsHTML;
    }
}

// ==================== REGISTER FORM VALIDATION ==================== 
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', validateRegisterForm);
}

function validateRegisterForm(e) {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const terms = document.getElementById('terms').checked;

    if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match!');
        return false;
    }

    if (password.length < 8) {
        e.preventDefault();
        alert('Password must be at least 8 characters long!');
        return false;
    }

    if (!terms) {
        e.preventDefault();
        alert('You must agree to the Terms of Service!');
        return false;
    }

    return true;
}

// ==================== LOGIN PAGE ==================== 
const loginTogglePassword = document.getElementById('togglePassword');
if (loginTogglePassword) {
    const loginPasswordInput = document.getElementById('password');
    loginTogglePassword.addEventListener('click', () => {
        const type = loginPasswordInput.type === 'password' ? 'text' : 'password';
        loginPasswordInput.type = type;
        loginTogglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
}

// Toggle password visibility for register page
const registerTogglePassword = document.getElementById('togglePassword');
const registerToggleConfirmPassword = document.getElementById('toggleConfirmPassword');

if (registerTogglePassword) {
    const registerPasswordInput = document.getElementById('password');
    registerTogglePassword.addEventListener('click', () => {
        const type = registerPasswordInput.type === 'password' ? 'text' : 'password';
        registerPasswordInput.type = type;
        registerTogglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
}

if (registerToggleConfirmPassword) {
    const confirmPasswordInput = document.getElementById('confirm_password');
    registerToggleConfirmPassword.addEventListener('click', () => {
        const type = confirmPasswordInput.type === 'password' ? 'text' : 'password';
        confirmPasswordInput.type = type;
        registerToggleConfirmPassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
}

// ==================== SMOOTH SCROLLING & ANIMATIONS ==================== 
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .feature-card, .stat-card, .tip-card, .dashboard-card').forEach(el => {
        observer.observe(el);
    });
});

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// ==================== CONTACT FORM HANDLER ==================== 
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        // Let the form submit normally to the backend
        // Additional client-side validation can be added here if needed
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (!name || !email || !message) {
            e.preventDefault();
            alert('Please fill in all required fields!');
        }
    });
}

// ==================== UTILITY FUNCTIONS ==================== 
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Format URL function
function formatURL(url) {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
    }
    return url;
}

// ==================== NAVBAR ACTIVE LINK ==================== 
document.addEventListener('DOMContentLoaded', function() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.style.borderBottom = '2px solid white';
            link.style.paddingBottom = '0.25rem';
        }
    });
});

// ==================== MOBILE MENU TOGGLE ==================== 
// Simple responsive nav toggle (if needed)
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks.style.display === 'none') {
        navLinks.style.display = 'flex';
    } else {
        navLinks.style.display = 'none';
    }
}

console.log('CyberSafe JavaScript loaded successfully!');
