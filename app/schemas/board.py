from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.base import ResponseBaseModel


class RequestBoardCreateDto(BaseModel):
    name: str = Field(title="게시판 명", example="게시판")
    public: bool = Field(title="공개여부", example=True)


class BoardCreate(RequestBoardCreateDto):
    user_id: int = Field(title="유저 ID", example=1)


class RequestBoardUpdateDto(BaseModel):
    name: str | None = Field(title="게시판 명", example="게시판")
    public: bool | None = Field(title="공개여부", example=True)


class BoardUpdate(RequestBoardUpdateDto):
    id: int = Field(title="게시판 ID", example=1)
    user_id: int = Field(title="유저 ID", example=1)


class ResponseBoardDto(BaseModel):
    id: int = Field(title="게시판 ID", example=1)
    name: str = Field(title="게시판 명", example="게시판")
    public: bool = Field(title="공개여부", example=True)
    user_id: int = Field(title="유저 ID", example=1)
    created_dt: datetime = Field(title="생성일", example="2024-01-01 00:00:00")
    updated_dt: datetime = Field(title="수정일", example="2024-01-01 00:00:00")


class ResponseBoard(ResponseBaseModel):
    data: ResponseBoardDto


class ResponseBoardList(ResponseBaseModel):
    data: list[ResponseBoardDto]
