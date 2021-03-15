from celery import Celery
from long_running_task import long_running_task


app = Celery("tasks", broker="redis://redis", backend="redis://redis")


@app.task
def run_long_task_in_background():
    return long_running_task()