import os
from celery.schedules import crontab


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fdnckdhfwislehfhugdnckcks"
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "flkdklmczielkmfhwkdjiurnckxdf"
    SECURITY_URL_PREFIX = "/api"
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_PROTECT = False
    CELERY_broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"
    imports = ("app.tasks",)
    CELERY_BEAT_SCHEDULE = {
        "send-daily-reminders": {
            "task": "app.tasks.send_daily_reminders",
            "schedule": crontab(hour=20, minute=0),  # At 8:00 PM
        },
        "generate-monthly-reports": {
            "task": "app.tasks.generate_monthly_report",
            "schedule": crontab(
                day_of_month=1, hour=0, minute=0
            ),  # First day of every month at midnight
        },
    }

    # Email config
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp-relay.brevo.com"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "5e610a001@smtp-brevo.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or "BREVO_API_KEY"
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER") or "duggalpiyush0@gmail.com"
    )

    # Flask-Security-Too config
    SECURITY_LOGIN_URL = "/fs_login"
