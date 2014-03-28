import os

class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY = 'datarec_jercoh'
    SECRET_KEY = '\xc7\xb7.}\xf0Oe\xafGNFF\xe6\x18mT'

class ProductionConfig(Config):
    MONGO_URL = os.environ.get('MONGOHQ_URL')

class DevelopmentConfig(Config):
	MONGODB_SETTINGS = {'DB': 'test_database'}
	DEBUG = True

class TestingConfig(Config):
    TESTING = True