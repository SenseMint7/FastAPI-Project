from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from app.containers import Container
from app.schemas.base import ResponseBase
from app.schemas.user import (
    RequestUserLoginDto,
    RequestUserRegisterDto,
    ResponseUserLogin,
)
from app.services.user import UserService

router = APIRouter(tags=["user"])


@router.post(
    "/user/register",
    response_model=ResponseBase,
    responses={
        201: {"description": "계정 생성이 완료되었습니다."},
        409: {"description": "이미 계정이 존재합니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_201_CREATED,
    description="회원가입 API",
    summary="Register User",
)
@inject
async def register(
    request: RequestUserRegisterDto,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> ResponseBase:
    await user_service.check_register_user(request.email)
    await user_service.register(request)
    return ResponseBase(
        code=status.HTTP_201_CREATED,
        message="계정 생성이 완료되었습니다.",
    )


@router.post(
    "/auth/login",
    response_model=ResponseUserLogin,
    responses={
        200: {"description": "로그인이 완료되었습니다."},
        401: {"description": "비밀번호가 일치하지 않습니다."},
        404: {"description": "계정이 없습니다. 계정을 생성해 주세요."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="로그인 API",
    summary="Login User",
)
@inject
async def login(
    request: RequestUserLoginDto,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> ResponseUserLogin:
    data = await user_service.login(request.email, request.password)
    return ResponseUserLogin(
        code=status.HTTP_200_OK, message="로그인이 완료되었습니다.", data=data
    )


@router.post(
    "/auth/logout",
    response_model=ResponseBase,
    responses={
        200: {"description": "로그아웃이 완료되었습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="로그인 API",
    summary="Login User",
)
@inject
async def logout(
    token: Annotated[str, Body(description="토큰", embed=True)],
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> ResponseBase:
    await user_service.logout(token)
    return ResponseBase(
        code=status.HTTP_200_OK,
        message="로그아웃이 완료되었습니다.",
    )
