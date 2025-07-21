import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "108")  # Use environment variables for security
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://admin:KGPDV@108@db/voice_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


