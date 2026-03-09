"""
Configuration file for CyberSafe application
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Change if you have a password
    MYSQL_DB = 'cybersafe'
    MYSQL_CURSORCLASS = 'DictCursor'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Update these with your production database credentials
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'cybersafe')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'cybersafe_test'

# Default configuration
config = DevelopmentConfig()
