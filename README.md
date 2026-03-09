# CyberSafe Website - Setup Instructions

## Project Structure
```
cyber-security-website/
├── app.py                  # Flask application
├── config.py              # Configuration file
├── setup_database.py      # Database setup script
├── requirements.txt       # Python dependencies
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── password-checker.html
│   ├── phishing-checker.html
│   ├── tips.html
│   ├── contact.html
│   └── dashboard.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Prerequisites

1. **Python 3.7+** - Install from https://www.python.org/
2. **MySQL** - Install from https://www.mysql.com/
3. **pip** - Python package manager (usually comes with Python)

## Installation Steps

### Step 1: Install Python Dependencies

```bash
cd cyber-security-website
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database

#### Option A: Using setup_database.py (Automated)
```bash
python setup_database.py
```

#### Option B: Manual Setup
1. Open MySQL Command Line or MySQL Workbench
2. Run the following commands:

```sql
CREATE DATABASE cybersafe;
USE cybersafe;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    category VARCHAR(50),
    status VARCHAR(50) DEFAULT 'unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE password_checks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    password_strength INT,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE url_checks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    url VARCHAR(500),
    is_safe BOOLEAN,
    indicators TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

### Step 3: Configure Database Connection

Edit `config.py` and update the MySQL credentials if needed:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'  # Leave empty if no password
MYSQL_DB = 'cybersafe'
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Features

### 🏠 Home Page
- Introduction to cybersecurity
- Cyber attack statistics
- Security features overview

### 🔑 Password Strength Checker
- Real-time password analysis
- Strength indicators (Weak/Medium/Strong)
- Security recommendations
- Check criteria: length, uppercase, lowercase, numbers, special chars

### 🌐 Phishing URL Detector
- Detect suspicious URLs
- Check for common phishing indicators
- HTTPS verification
- Domain analysis

### 📚 Security Tips
- 12 essential cybersecurity practices
- Warning signs of cyber attacks
- Best practices and recommendations

### 👤 User Authentication
- Secure registration with validation
- Password hashing for security
- Login system with session management
- User dashboard with security score

### 📧 Contact Form
- User feedback submission
- Contact information
- FAQ section

## Security Features

- ✅ Passwords are hashed using Werkzeug
- ✅ Session-based authentication
- ✅ SQL injection prevention with parameterized queries
- ✅ Input validation and sanitization
- ✅ HTTPS ready (configure in production)
- ✅ CORS protection
- ✅ Secure password recommendations

## Default Credentials

After installation, no default users exist. You need to register first using the registration page.

Test registration:
- Email: test@example.com
- Password: Test@123456 (meets all requirements)

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with all routes and logic |
| `config.py` | Configuration settings for different environments |
| `setup_database.py` | Automated database setup script |
| `requirements.txt` | Python package dependencies |
| `templates/` | HTML template files |
| `static/css/style.css` | Complete CSS styling for the website |
| `static/js/script.js` | JavaScript for interactive features |

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running
- Check your host, username, and password in `config.py`
- Verify the `cybersafe` database exists

### Module Not Found
- Run `pip install -r requirements.txt` again
- Check Python version compatibility (3.7+)

### Port 5000 Already in Use
- Change the port in `app.py`: `app.run(port=5001)`
- Or stop the process using port 5000

## Environment Variables (Production)

For production deployment, set these environment variables:

```
SECRET_KEY=your-production-secret-key
MYSQL_HOST=your-database-host
MYSQL_USER=your-database-user
MYSQL_PASSWORD=your-database-password
MYSQL_DB=cybersafe
FLASK_ENV=production
```

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Tools
- `POST /api/check-password-strength` - Check password strength
- `POST /api/check-phishing-url` - Detect phishing URLs
- `POST /api/save-assessment` - Save security assessments

### Pages
- `GET /` - Home page
- `GET /password-checker` - Password checker page
- `GET /phishing-checker` - Phishing detector page
- `GET /tips` - Security tips page
- `GET /contact` - Contact page
- `GET /dashboard` - User dashboard (protected)

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Email verification for registration
- [ ] Advanced phishing detection with ML
- [ ] Security score algorithm improvements
- [ ] User activity tracking and reporting
- [ ] Admin dashboard
- [ ] Dark mode
- [ ] Mobile app

## License

This project is for educational purposes.

## Support

For issues or questions, please contact: info@cybersafe.com

---

**Happy Coding! 🛡️🔐**
