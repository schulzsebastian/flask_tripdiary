class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = '\x91\xc74+\x94|c\x01\x86\xf3\x8bz\n\xf52\xc7eI\x9ev\xcc)\xa9d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/tripdiary'
    SQLALCHEMY_TRACK_MODIFICATIONS = False