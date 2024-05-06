from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import ResponseBaseModel


class RequestUserRegisterDto(BaseModel):
    fullname: str = Field(title="이름", example="박상도")
    email: EmailStr = Field(title="이메일", example="shfkstjsanf@gmail.com")
    password: str = Field(title="비밀번호", example="devpassword")


class RequestUserLoginDto(BaseModel):
    email: EmailStr = Field(title="이메일", example="shfkstjsanf@gmail.com")
    password: str = Field(title="비밀번호", example="devpassword")


class ResponseUserLoginDto(BaseModel):
    fullname: str = Field(title="이름", example="박상도")
    email: str = Field(title="이메일", example="shfkstjsanf@gmail.com")
    access_token: str = Field(title="엑세스 토큰")


class ResponseUserLogin(ResponseBaseModel):
    data: ResponseUserLoginDto
