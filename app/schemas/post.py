from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.base import ResponseBaseModel


class RequestPostCreateDto(BaseModel):
    board_id: int = Field(title="게시판 ID", example=1)
    title: str = Field(title="게시글 제목", example="새 게시글")
    content: str = Field(title="게시글 내용", example="게시글 내용")


class PostCreate(RequestPostCreateDto):
    user_id: int = Field(title="유저 ID", example=1)


class RequestPostUpdateDto(BaseModel):
    title: str | None = Field(title="게시글 제목", example="수정된 게시글 제목")
    content: str | None = Field(title="게시글 내용", example="수정된 게시글 내용")


class PostUpdate(RequestPostUpdateDto):
    id: int = Field(title="게시글 ID", example=1)
    user_id: int = Field(title="유저 ID", example=1)


class ResponsePostDto(BaseModel):
    id: int = Field(title="게시글 ID", example=1)
    title: str | None = Field(title="게시글 제목", example="수정된 게시글 제목")
    content: str | None = Field(title="게시글 내용", example="수정된 게시글 내용")
    user_id: int = Field(title="유저 ID", example=1)
    board_id: int = Field(title="게시판 ID", example=1)
    created_dt: datetime = Field(title="생성일", example="2024-01-01 00:00:00")
    updated_dt: datetime = Field(title="수정일", example="2024-01-01 00:00:00")


class ResponsePost(ResponseBaseModel):
    data: ResponsePostDto


class ResponsePostList(ResponseBaseModel):
    data: list[ResponsePostDto]
