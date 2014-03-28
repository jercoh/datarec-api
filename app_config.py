import os

class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY = 'datarec_jercoh'
    SECRET_KEY = '\xc7\xb7.}\xf0Oe\xafGNFF\xe6\x18mT'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = 'test_database'
    MONGODB_USERNAME = 'user'
    MONGODB_PASSWORD = 'password'

class ProductionConfig(Config):
    MONGO_URL = os.environ.get('MONGOHQ_URL')

class DevelopmentConfig(Config):
	DB_NAME = 'test_database'
	MONGO_URL = 'mongodb://localhost:27017/'+DB_NAME
	DEBUG = True

class TestingConfig(Config):
    TESTING = True