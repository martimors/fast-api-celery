from pydantic import BaseModel, Field

class Response(BaseModel):
    foo: str = Field(None, example="bar")