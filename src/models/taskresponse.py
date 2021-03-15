from pydantic import BaseModel, Field
from uuid import UUID


class TaskResponse(BaseModel):
    id: UUID = Field(None, example=UUID("b71b4dc3-2404-4d9e-b921-f364ccd8e6f9"))
    result_endpoint: str = Field(None, example=("/result/933e95ed-b259-4fcb-ad2d-6c8b59c037b6"))
