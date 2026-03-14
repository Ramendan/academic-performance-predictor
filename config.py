"""
Configuration settings for the Academic Performance Monitoring & Prediction System.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "apms-dev-secret-key-2026")
    DATA_FILE = os.path.join(BASE_DIR, "app", "data", "students.csv")
    SAMPLE_DATA_FILE = os.path.join(BASE_DIR, "app", "data", "sample_students.csv")
    MODEL_DIR = os.path.join(BASE_DIR, "app", "ml", "saved_models")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
