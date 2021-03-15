from typing import Optional
import uuid

from fastapi import FastAPI

from models.response import Response
from tasks import run_long_task_in_background
import logging

from starlette.status import HTTP_202_ACCEPTED


# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project.
# This will get the root logger since no logger in the configuration has this name.
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task", response_model=Response, status_code=HTTP_202_ACCEPTED)
def start_task():
    logger.info("Started loooong task")
    result = run_long_task_in_background.delay()
    return {"id": uuid.uuid4()}