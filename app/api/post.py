from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.containers import Container
from app.schemas.base import ResponseBase
from app.schemas.post import (
    RequestPostCreateDto,
    RequestPostUpdateDto,
    ResponsePost,
    ResponsePostList,
)
from app.services.auth import AuthService
from app.services.post import PostService

router = APIRouter(tags=["post"])

container = Container()

CurrentUser = Annotated[tuple[int, str], Depends(AuthService.get_current_user)]


@router.post(
    "/post",
    response_model=ResponseBase,
    responses={
        201: {"description": "게시글 생성이 완료되었습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_201_CREATED,
    description="게시글 생성 API",
    summary="Create Post",
)
@inject
async def create_post(
    request: RequestPostCreateDto,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)

    await post_service.create_post(user_id, request)
    return ResponseBase(
        code=status.HTTP_201_CREATED, message="게시글 생성이 완되었습니다."
    )


@router.get(
    "/post/{id}",
    response_model=ResponsePost,
    responses={
        200: {"description": "게시글 조회 성공."},
        404: {"description": "게시글을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시글 조회 API",
    summary="Get Board",
)
@inject
async def get_post(
    id: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> ResponsePost:
    user_id, token = current_user
    await auth_service.check_blacklist(token)

    data = await post_service.get_post(id, user_id)
    return ResponsePost(code=status.HTTP_200_OK, message="게시글 조회 성공", data=data)


@router.put(
    "/post/{id}",
    response_model=ResponseBase,
    responses={
        200: {"description": "게시글 업데이트 성공."},
        403: {"description": "권한이 없습니다."},
        404: {"description": "게시글을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시글 업데이트 API",
    summary="Update Post",
)
@inject
async def update_post(
    id: int,
    request: RequestPostUpdateDto,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)

    await post_service.update_post(id, user_id, request)
    return ResponseBase(code=status.HTTP_200_OK, message="게시글 업데이트 성공.")


@router.delete(
    "/post/{id}",
    response_model=ResponseBase,
    responses={
        200: {"description": "게시글 삭제 성공."},
        403: {"description": "권한이 없습니다."},
        404: {"description": "게시글을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시글 삭제 API",
    summary="Delete Post",
)
@inject
async def delete_post(
    id: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)

    await post_service.delete_post(id, user_id)
    return ResponseBase(code=status.HTTP_200_OK, message="게시글 삭제 성공.")


@router.get(
    "/posts/{board_id}",
    response_model=ResponsePostList,
    responses={
        200: {"description": "게시글 목록 조회 성공."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시글 목록 조회 API",
    summary="Get Post List",
)
@inject
async def list_posts(
    board_id: int,
    cursor_id: int,
    limit: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> ResponsePostList:
    user_id, token = current_user
    await auth_service.check_blacklist(token)

    data = await post_service.list_posts(board_id, user_id, cursor_id, limit)
    return ResponsePostList(
        code=status.HTTP_200_OK, message="게시글 목록 조회 성공", data=data
    )
