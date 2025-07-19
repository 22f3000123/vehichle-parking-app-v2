from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# This is needed for tasks to run within the Flask app context
# It will be called from __init__.py after app creation
def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
