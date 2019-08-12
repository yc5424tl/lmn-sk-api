import os

class Config(object):
    SECRET_KEY = os.urandom(27)
    TESTING = False
    DATABASE_URI = None
    JSONIFY_PRETTYPRINT_REGULAR = False
    # EXECUTOR_TYPE = 'process'
    # EXECUTOR_MAX_WORKERS = 4

class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True

del os