import time
from models.taskresult import TaskResult


def long_running_task() -> TaskResult:
    time.sleep(60)
    return TaskResult(foo="bar")
