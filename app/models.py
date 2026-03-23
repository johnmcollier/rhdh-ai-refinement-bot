from typing import Literal

from pydantic import BaseModel, field_validator


class AnalyzeRequest(BaseModel):
    description: str

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Description cannot be empty")
        return v


class AnalyzeResponse(BaseModel):
    story_points: float
    priority: Literal["blocker", "critical", "major", "normal", "minor"]
    justification: str
