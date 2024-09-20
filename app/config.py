class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # استخدام قاعدة بيانات في الذاكرة للاختبارات
    SQLALCHEMY_TRACK_MODIFICATIONS = False
