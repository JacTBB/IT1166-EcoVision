class Config:
    SECRET_KEY = "1234567890"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False