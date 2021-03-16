import logging
from fastapi import APIRouter, status, Response
from fastapi.responses import RedirectResponse
from uuid import UUID
from celery.result import AsyncResult
from app.celeryapp import celeryapp

from app.models.taskresponse import TaskResponse
from app.models.taskresult import TaskResult

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: Should be a POST request
@router.get("/task", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def start_task():
    logger.info("Started loooong task")
    result = celeryapp.send_task("long_task_in_background")
    return TaskResponse(
        id=result.id,
        result_endpoint=router.url_path_for("get_status", task_id=result.id),
    )


@router.get("/status/{task_id}")
def get_status(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)

    if task.ready():
        return RedirectResponse(router.url_path_for("get_result", task_id=task_id))
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return


@router.get(
    "/result/{task_id}", response_model=TaskResult, status_code=status.HTTP_200_OK
)
def get_result(task_id: UUID, response: Response):
    task = AsyncResult(str(task_id), app=celeryapp)
    if task.ready():
        return task.get(timeout=1)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
