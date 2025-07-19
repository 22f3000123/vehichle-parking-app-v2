import os
from celery.schedules import crontab

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'a-secret-salt'
    SECURITY_URL_PREFIX = '/api' # Add this line
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_PROTECT = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    CELERY_IMPORTS = ('app.celery_utils',)
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'app.celery_utils.send_daily_reminders',
            'schedule': crontab(hour=20, minute=0), # Every day at 8 PM
        },
        'generate-monthly-reports': {
            'task': 'app.celery_utils.generate_monthly_report',
            'schedule': crontab(day_of_month=1, hour=0, minute=0), # First day of every month at midnight
            'args': (1,) # Example: user_id for admin
        },
    }

    # Email configuration for monthly reports
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your_email_password'

    # Flask-Security-Too config
    SECURITY_LOGIN_URL = "/fs_login"
