class Config:
    TESTING = False
    DEBUG = False
    SECRET_KEY = "your_secret_key"


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False  # Désactive CSRF pour les tests, si nécessaire
