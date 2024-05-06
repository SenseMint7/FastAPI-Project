from typing import Callable
from unittest.mock import AsyncMock

import pytest

import app.errors.exceptions as ex
from app.models.board import Board
from app.repositories.board import BoardRepository
from app.schemas.board import (
    BoardCreate,
    BoardUpdate,
    RequestBoardCreateDto,
    RequestBoardUpdateDto,
)
from app.services.board import BoardService


@pytest.fixture
def test_board_service() -> tuple[BoardService, AsyncMock]:
    board_repository_mock = AsyncMock(spec=BoardRepository)
    board_service = BoardService(board_repository=board_repository_mock)
    return board_service, board_repository_mock


@pytest.mark.asyncio
async def test_create_board(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    board = board_fixture()
    board_create_dto = RequestBoardCreateDto(name=board.name, public=board.public)
    board_repository_mock.add.return_value = board

    result = await board_service.create_board(board.user_id, board_create_dto)

    board_create = BoardCreate(user_id=board.user_id, **board_create_dto.dict())

    assert result.name == board.name
    assert result.public == board.public
    board_repository_mock.add.assert_called_once_with(board_create)


@pytest.mark.asyncio
async def test_get_board_not_found(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    board_repository_mock.get_board.return_value = None

    with pytest.raises(ex.BoardNotFoundError):
        await board_service.get_board(1, 1)


@pytest.mark.asyncio
async def test_list_boards(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    board_list = [board_fixture() for _ in range(2)]
    board_repository_mock.list_boards.return_value = board_list

    result = await board_service.list_boards(1, 0, 10)

    assert len(result) == len(board_list)
    for board_dto, board in zip(result, board_list):
        assert board_dto.name == board.name
        assert board_dto.public == board.public


@pytest.mark.asyncio
async def test_update_board(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    board = board_fixture()
    board_update_dto = RequestBoardUpdateDto(name=board.name, public=board.public)
    board_update = BoardUpdate(
        id=board.id, name=board.name, public=board.public, user_id=board.user_id
    )

    board_repository_mock.get_board_by_board_id.return_value = board

    await board_service.update_board(board.id, board.user_id, board_update_dto)
    board_repository_mock.update.assert_called_once_with(board_update)


@pytest.mark.asyncio
async def test_update_board_permission_error(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    my_board = board_fixture()
    not_my_board = board_fixture()
    board_update_dto = RequestBoardUpdateDto(name=my_board.name, public=my_board.public)

    board_repository_mock.get_board_by_board_id.return_value = not_my_board

    with pytest.raises(ex.PermissionUserError):
        await board_service.update_board(
            my_board.id, my_board.user_id, board_update_dto
        )


@pytest.mark.asyncio
async def test_delete_board(
    test_board_service: tuple[BoardService, AsyncMock],
    board_fixture: Callable[..., Board],
) -> None:
    board_service, board_repository_mock = test_board_service

    board = board_fixture()
    board_repository_mock.get_board_by_board_id.return_value = board

    await board_service.delete_board(board.id, board.user_id)
    board_repository_mock.delete.assert_called_once_with(board.id)
