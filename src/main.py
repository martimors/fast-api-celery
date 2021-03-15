from uuid import UUID
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from celery.result import AsyncResult
from starlette.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_404_NOT_FOUND
from tasks import app as celeryapp

from models.taskresponse import TaskResponse
from models.taskresult import TaskResult
from tasks import run_long_task_in_background
import logging


# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def start_task():
    logger.info("Started loooong task")
    result = run_long_task_in_background.delay()
    return TaskResponse(id=result.id, result_endpoint=f"/result/{result.id}")


@app.get("/result/{task_id}", response_model=TaskResult, status_code=status.HTTP_200_OK)
def get_result(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)
    if task.ready():
        return task.get(timeout=1)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return


@app.get("/status/{task_id}", status_code=status.HTTP_302_FOUND)
def get_status(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)

    if task.ready():
        return RedirectResponse(app.url_path_for("get_result", task_id=task_id))
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return
