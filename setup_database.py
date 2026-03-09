"""
Database Configuration for CyberSafe
Setup MySQL database and tables
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_database():
    """Create MySQL database for CyberSafe"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS cybersafe")
        print("✓ Database 'cybersafe' created successfully!")
        
        # Use the database
        cursor.execute("USE cybersafe")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Table 'users' created successfully!")
        
        # Create contacts table
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Table 'contacts' created successfully!")
        
        # Create assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                assessment_type VARCHAR(50) NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Table 'assessments' created successfully!")
        
        # Create password_checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_checks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                password_strength INT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Table 'password_checks' created successfully!")
        
        # Create url_checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS url_checks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                url VARCHAR(500),
                is_safe BOOLEAN,
                indicators TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Table 'url_checks' created successfully!")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Database setup completed successfully!")
        print("Database: cybersafe")
        print("Tables: users, contacts, assessments, password_checks, url_checks")
        
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("="*50)
    print("CyberSafe Database Setup")
    print("="*50)
    create_database()
