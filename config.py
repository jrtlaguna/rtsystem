from os import environ, path

class Config(object):
    DATABASE = 'rt_system_db'
    DB_HOST = 'localhost'
    DB_PASSWORD = ''
    DB_USER = 'root'
    ROOTDIR = path.dirname(path.abspath(__file__))
    SECRET_KEY = environ.get('SECRET_KEY') or 'linti-ka'