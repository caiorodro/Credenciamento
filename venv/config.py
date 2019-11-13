class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xe58\xcf\x95\x91q\xde\xbf\x96lD\x1eA\x0fkC\xcaO\x10\xd6\x1a8\xf1\xfc"

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Credenciamento"
    DB_USERNAME = "root"
    DB_PASSWORD = "56Runna01"

    ZIP_UPLOADS = "/Users/caioDoran/Documents/Github/Credenciamento/csv"
    ZIP_DOWNLOADS = '/Users/caioDoran/Documents/Github/Credenciamento/csv'
    ZIP_ADDRESS = 'http://127.0.0.1:5000/csv/'

    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xe58\xcf\x95\x91q\xde\xbf\x96lD\x1eA\x0fkC\xcaO\x10\xd6\x1a8\xf1\xfc"

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Credenciamento"
    DB_USERNAME = "root"
    DB_PASSWORD = "56Runna01"

    ZIP_UPLOADS = "/Users/caioDoran/Documents/Github/Credenciamento/csv"
    ZIP_DOWNLOADS = '/Users/caioDoran/Documents/Github/Credenciamento/csv'
    ZIP_ADDRESS = 'http://127.0.0.1:5000/csv/'

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Credenciamento"
    DB_USERNAME = "root"
    DB_PASSWORD = "56Runna01"

    ZIP_UPLOADS = "/Users/caioDoran/Documents/Github/Credenciamento/csv"
    ZIP_DOWNLOADS = '/Users/caioDoran/Documents/Github/Credenciamento/csv'
    ZIP_ADDRESS = 'http://127.0.0.1:5000/csv/'

    SESSION_COOKIE_SECURE = False