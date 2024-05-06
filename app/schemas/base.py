from typing import Any

from pydantic import BaseModel, Field


class ResponseBaseModel(BaseModel):
    code: int = Field(title="응답 코드", example=200)
    message: str = Field(title="응답 메시지", example="")


class ResponseBase(ResponseBaseModel):
    data: dict[str, Any] = Field(title="응답 데이터", default={})
