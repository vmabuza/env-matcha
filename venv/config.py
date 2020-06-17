class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'the waters'

    DB_NAME = 'production-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
    # IMAGE_UPLOADS="/home/zakhele/Documents/app/app/static/img"
    
    UPLOADS="/home/zakhele/Desktop/Matcha-version2/app/static/img"
    SESSION_COOKIE_SECURE = True



class ProductionConfig(Config):
    SECRET_KEY = 'the waters'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'the waters'

    DB_NAME="develpment-db"
    DB_USERNAME="root"
    DB_PASSWORD=""
    IMAGE_UPLOADS = "/home/zakhele/Desktop/Matcha-version2/app/static/img"
    ALLOWED_IMAGE_EXTENSIONS = ["PNG","JPG","JPEG","GIF"]

    UPLOADS="/home/zakhele/Documents/app/app/static/img"
    SESSION_COOKIE_SECURE=False

class TestingConfig(Config):
    TESTING=True

    DB_NAME="production-db"
    DB_USERNAME="root"
    DB_PASSWORD=""
    SECRET_KEY = 'the waters'

    UPLOADS ="/home/zakhele/Documents/app/app/static/img"
    SESSION_COOKIE_SECURE=False
