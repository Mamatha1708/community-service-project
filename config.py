import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env if present
load_dotenv(BASE_DIR / '.env')

class Config:
    # 1. Secret Key for session signing
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kalamkari-csp-secret-key-2026-safe-dev')
    
    # 2. Environment & Debug flag
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1')

    # 3. Database configuration (SQLite default, PostgreSQL ready for Render)
    _raw_db_url = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "kalamkari.db"}')
    # Normalize postgres:// to postgresql:// for modern SQLAlchemy
    if _raw_db_url.startswith('postgres://'):
        _raw_db_url = _raw_db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 4. Session & Cookie Security
    is_render = bool(os.environ.get('RENDER'))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Enable secure cookie over HTTPS on Render, while allowing local HTTP dev testing
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'true' if is_render else 'false').lower() in ('true', '1')
    
    # 5. Upload settings
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)) # 5MB limit
    
    # 6. Optional Gemini AI API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
