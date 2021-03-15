from pydantic.main import BaseModel


class TaskResult(BaseModel):
    foo: str
