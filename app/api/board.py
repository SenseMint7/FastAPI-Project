from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.containers import Container
from app.schemas.base import ResponseBase
from app.schemas.board import (
    RequestBoardCreateDto,
    RequestBoardUpdateDto,
    ResponseBoard,
    ResponseBoardList,
)
from app.services.auth import AuthService
from app.services.board import BoardService

router = APIRouter(tags=["board"])

container = Container()

CurrentUser = Annotated[tuple[int, str], Depends(AuthService.get_current_user)]


@router.post(
    "/board",
    response_model=ResponseBase,
    responses={
        201: {"description": "게시판 생성이 완료되었습니다."},
        409: {"description": "이미 해당 이름의 게시판이 존재합니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_201_CREATED,
    description="게시판 생성 API",
    summary="Create Board",
)
@inject
async def create_board(
    request: RequestBoardCreateDto,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)
    await board_service.create_board(user_id, request)
    return ResponseBase(
        code=status.HTTP_201_CREATED,
        message="게시판 생성이 완료되었습니다.",
    )


@router.get(
    "/board/{id}",
    response_model=ResponseBoard,
    responses={
        200: {"description": "게시판 조회 성공."},
        404: {"description": "게시판을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시판 조회 API",
    summary="Get Board",
)
@inject
async def get_board(
    id: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
) -> ResponseBoard:
    user_id, token = current_user
    await auth_service.check_blacklist(token)
    data = await board_service.get_board(id, user_id)
    return ResponseBoard(
        code=status.HTTP_200_OK, message="게시판 조회 성공.", data=data
    )


@router.get(
    "/boards",
    response_model=ResponseBoardList,
    responses={
        200: {"description": "게시판 목록 조회 성공."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시판 목록 조회 API",
    summary="Get Board List",
)
@inject
async def list_boards(
    cursor_id: int,
    limit: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
) -> ResponseBoardList:
    user_id, token = current_user
    await auth_service.check_blacklist(token)
    data = await board_service.list_boards(user_id, cursor_id, limit)
    return ResponseBoardList(
        code=status.HTTP_200_OK, message="게시판 목록 조회 성공.", data=data
    )


@router.put(
    "/board/{id}",
    response_model=ResponseBase,
    responses={
        200: {"description": "게시판 업데이트 성공."},
        403: {"description": "권한이 없습니다."},
        404: {"description": "게시판을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시판 업데이트 API",
    summary="Update Board",
)
@inject
async def update_board(
    id: int,
    request: RequestBoardUpdateDto,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)
    await board_service.update_board(id, user_id, request)
    return ResponseBase(code=status.HTTP_200_OK, message="게시판 업데이트 성공.")


@router.delete(
    "/board/{id}",
    response_model=ResponseBase,
    responses={
        200: {"description": "게시판 삭제 성공."},
        403: {"description": "권한이 없습니다."},
        404: {"description": "게시판을 찾을 수 없습니다."},
        422: {"description": "Validation Error"},
    },
    status_code=status.HTTP_200_OK,
    description="게시판 삭제 API",
    summary="Delete Board",
)
@inject
async def delete_board(
    id: int,
    current_user: CurrentUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
) -> ResponseBase:
    user_id, token = current_user
    await auth_service.check_blacklist(token)
    await board_service.delete_board(board_id=id, user_id=user_id)
    return ResponseBase(code=status.HTTP_200_OK, message="게시판 삭제 성공.")
