import os

class Config:
    SECRET_KEY = os.urandom(24)  # секретный ключ для Flask
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://flask_user:your_password@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
