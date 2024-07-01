import os
# Use set SECRET_KEY='your-very-secret-key' on Windows to set environment secret-key
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///workout-tracker.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
