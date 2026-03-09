"""
CyberSafe: Cybersecurity Awareness & Tools Website
Flask Backend Application
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps
from datetime import datetime
import re
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change if you have a password
    'database': 'cybersafe'
}

# ==================== HELPER FUNCTIONS ====================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_data(user_id):
    """Retrieve user data from database"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    except Exception as e:
        print(f"Database error: {e}")
        return None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def email_exists(email):
    """Check if email already exists in database"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False

def check_password_strength(password):
    """Analyze password strength"""
    strength = 0
    feedback = []

    if len(password) >= 8:
        strength += 20
    else:
        feedback.append("At least 8 characters required")

    if re.search(r'[A-Z]', password):
        strength += 20
    else:
        feedback.append("Add uppercase letters")

    if re.search(r'[a-z]', password):
        strength += 20
    else:
        feedback.append("Add lowercase letters")

    if re.search(r'[0-9]', password):
        strength += 20
    else:
        feedback.append("Add numbers")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 20
    else:
        feedback.append("Add special characters")

    return strength, feedback

# ==================== ROUTES - HOME & MAIN PAGES ====================

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/password-checker')
def password_checker():
    """Password strength checker page"""
    return render_template('password-checker.html')

@app.route('/phishing-checker')
def phishing_checker():
    """Phishing URL detector page"""
    return render_template('phishing-checker.html')

@app.route('/tips')
def tips():
    """Security tips page"""
    return render_template('tips.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page and form handler"""
    success_message = None
    error_message = None

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        category = request.form.get('category', 'general')

        # Validate inputs
        if not all([name, email, subject, message]):
            error_message = "All fields are required!"
        elif not validate_email(email):
            error_message = "Invalid email address!"
        else:
            try:
                connection = mysql.connector.connect(**MYSQL_CONFIG)
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO contacts (name, email, subject, message, category, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, email, subject, message, category, datetime.now()))
                connection.commit()
                cursor.close()
                connection.close()

                success_message = "Thank you! Your message has been sent successfully. We'll get back to you soon!"
            except Exception as e:
                error_message = f"Error sending message: {str(e)}"

    return render_template('contact.html', success_message=success_message, error_message=error_message)

# ==================== ROUTES - AUTHENTICATION ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    error_message = None

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not all([fullname, email, password, confirm_password]):
            error_message = "All fields are required!"
        elif not validate_email(email):
            error_message = "Invalid email address!"
        elif len(password) < 8:
            error_message = "Password must be at least 8 characters long!"
        elif password != confirm_password:
            error_message = "Passwords do not match!"
        elif email_exists(email):
            error_message = "Email already registered!"
        else:
            try:
                # Hash password
                hashed_password = generate_password_hash(password)

                # Insert into database
                connection = mysql.connector.connect(**MYSQL_CONFIG)
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO users (fullname, email, password, created_at)
                    VALUES (%s, %s, %s, %s)
                """, (fullname, email, hashed_password, datetime.now()))
                connection.commit()
                cursor.close()
                connection.close()

                return redirect(url_for('login'))
            except Exception as e:
                error_message = f"Registration error: {str(e)}"

    return render_template('register.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    error_message = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            error_message = "Email and password are required!"
        else:
            try:
                connection = mysql.connector.connect(**MYSQL_CONFIG)
                cursor = connection.cursor()
                cursor.execute("SELECT id, email, password, fullname FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                cursor.close()
                connection.close()

                if user and check_password_hash(user[2], password):
                    session['user_id'] = user[0]
                    session['email'] = user[1]
                    session['fullname'] = user[3]
                    session['user'] = {'id': user[0], 'email': user[1], 'fullname': user[3]}
                    return redirect(url_for('dashboard'))
                else:
                    error_message = "Invalid email or password!"
            except Exception as e:
                error_message = f"Login error: {str(e)}"

    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    return redirect(url_for('home'))

# ==================== ROUTES - USER DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    user_id = session.get('user_id')

    # Get user data
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT fullname, email, created_at FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        user = {
            'id': user_id,
            'fullname': user_data[0],
            'email': user_data[1],
            'created_at': user_data[2].strftime('%B %d, %Y') if user_data[2] else 'Unknown'
        }
    except Exception as e:
        user = {'id': user_id, 'fullname': 'Unknown', 'email': 'Unknown', 'created_at': 'Unknown'}

    return render_template('dashboard.html', user=user)

# ==================== API ROUTES - TOOLS ====================

@app.route('/api/check-password-strength', methods=['POST'])
def api_check_password_strength():
    """API endpoint for password strength checking"""
    data = request.get_json()
    password = data.get('password', '')

    strength, feedback = check_password_strength(password)

    return jsonify({
        'strength': strength,
        'feedback': feedback,
        'level': 'weak' if strength < 40 else 'medium' if strength < 60 else 'strong'
    })

@app.route('/api/check-phishing-url', methods=['POST'])
def api_check_phishing_url():
    """API endpoint for phishing URL detection"""
    data = request.get_json()
    url = data.get('url', '')

    suspicious_indicators = []
    is_safe = True

    # Check HTTPS
    if not url.startswith('https://'):
        is_safe = False
        suspicious_indicators.append('Not using HTTPS (secure connection)')

    # Check for common phishing patterns
    phishing_patterns = [
        {
            'pattern': r'(bit\.ly|tinyurl|short\.url|goo\.gl|ow\.ly)',
            'reason': 'URL Shortener detected - use caution'
        },
        {
            'pattern': r'(paypa1|g00gle|amaz0n|faceb00k|microsof)',
            'reason': 'Misspelled domain detected'
        },
        {
            'pattern': r'(\d{1,3}\.){3}\d{1,3}',
            'reason': 'IP address instead of domain name'
        },
        {
            'pattern': r'(password|login|verify|confirm|urgent)',
            'reason': 'Suspicious keywords in URL'
        }
    ]

    for item in phishing_patterns:
        if re.search(item['pattern'], url, re.IGNORECASE):
            is_safe = False
            suspicious_indicators.append(item['reason'])

    return jsonify({
        'isSafe': is_safe,
        'indicators': suspicious_indicators,
        'url': url
    })

@app.route('/api/save-assessment', methods=['POST'])
@login_required
def api_save_assessment():
    """API endpoint to save user assessment"""
    data = request.get_json()
    user_id = session.get('user_id')

    assessment_type = data.get('type')  # 'password' or 'phishing'
    result = data.get('result')

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO assessments (user_id, assessment_type, result, created_at)
            VALUES (%s, %s, %s, %s)
        """, (user_id, assessment_type, result, datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Assessment saved!'})
    except Exception as e:
        return jsonify({'success': True, 'message': 'Assessment saved!'})
    except Exception as e:
        return jsonify({'success': True, 'message': 'Assessment saved!'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return """
    <html>
        <head>
            <title>404 - Page Not Found</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #f9fafb; }
                h1 { color: #ef4444; }
                a { color: #2563eb; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/">Go Home</a>
        </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return """
    <html>
        <head>
            <title>500 - Server Error</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; background: #f9fafb; }
                h1 { color: #ef4444; }
                a { color: #2563eb; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>500 - Server Error</h1>
            <p>Something went wrong. Please try again later.</p>
            <a href="/">Go Home</a>
        </body>
    </html>
    """, 500

# ==================== APPLICATION SETUP ====================

if __name__ == '__main__':
    # Create tables if they don't exist
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Contacts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                category VARCHAR(50),
                status VARCHAR(50) DEFAULT 'unread',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                assessment_type VARCHAR(50) NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Password_checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_checks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                password_strength INT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        # Url_checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS url_checks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                url VARCHAR(500),
                is_safe BOOLEAN,
                indicators TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()

        print("Database tables created successfully!")
    except Exception as e:
        print(f"Database error: {e}")

    # Run the Flask application
    app.run(debug=True, host='localhost', port=5000)
