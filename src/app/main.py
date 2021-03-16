from uuid import UUID
from celery import Celery
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from celery.result import AsyncResult

from .models.taskresponse import TaskResponse
from .models.taskresult import TaskResult
import logging


# setup loggers
# logging.config.fileConfig(Path.cwd() / "logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()
celeryapp = Celery("tasks", broker="redis://redis", backend="redis://redis")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def start_task():
    logger.info("Started loooong task")
    result = celeryapp.send_task("long_task_in_background")
    return TaskResponse(id=result.id, result_endpoint=f"/status/{result.id}")


@app.get("/result/{task_id}", response_model=TaskResult, status_code=status.HTTP_200_OK)
def get_result(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)
    if task.ready():
        return task.get(timeout=1)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return


@app.get("/status/{task_id}")
def get_status(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)

    if task.ready():
        return RedirectResponse(app.url_path_for("get_result", task_id=task_id))
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return
