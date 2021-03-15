from typing import Optional

from fastapi import FastAPI

from models.response import Response
from long_running_task import long_running_task
import logging


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


@app.get("/task", response_model=Response)
def start_task():
    logger.info("Started loooong task")
    return long_running_task()