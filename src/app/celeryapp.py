from celery import Celery


def create_celery_app():
    return Celery("tasks", broker="redis://redis", backend="redis://redis")


celeryapp = create_celery_app()