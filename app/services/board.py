import app.errors.exceptions as ex
from app.models.board import Board
from app.repositories.board import BoardRepository
from app.schemas.board import (
    BoardCreate,
    BoardUpdate,
    RequestBoardCreateDto,
    RequestBoardUpdateDto,
    ResponseBoardDto,
)


class BoardService:
    def __init__(self, board_repository: BoardRepository):
        self._repository: BoardRepository = board_repository

    async def create_board(
        self, user_id: int, board_create_dto: RequestBoardCreateDto
    ) -> Board:
        try:
            board_create = BoardCreate(user_id=user_id, **board_create_dto.dict())
            return await self._repository.add(board_create)
        except Exception:
            raise ex.AlreadyExistsBoardError()

    async def get_board(self, board_id: int, user_id: int) -> ResponseBoardDto:
        board = await self._repository.get_board(board_id, user_id)
        if not board:
            raise ex.BoardNotFoundError()
        return ResponseBoardDto(**board.__dict__)

    async def list_boards(
        self, user_id: int, cursor_id: int, limit: int
    ) -> list[ResponseBoardDto]:
        board_list = await self._repository.list_boards(user_id, cursor_id, limit)
        return [ResponseBoardDto(**board.__dict__) for board in board_list]

    async def check_board_authorized(self, board_id: int, user_id: int) -> None:
        board = await self._repository.get_board_by_board_id(board_id)
        if board and board.user_id != user_id:
            raise ex.PermissionUserError()
        if not board:
            raise ex.BoardNotFoundError()

    async def update_board(
        self, board_id: int, user_id: int, board_update_dto: RequestBoardUpdateDto
    ) -> None:
        await self.check_board_authorized(board_id, user_id)
        board_update = BoardUpdate(
            id=board_id, user_id=user_id, **board_update_dto.dict()
        )
        await self._repository.update(board_update)

    async def delete_board(self, board_id: int, user_id: int) -> None:
        await self.check_board_authorized(board_id, user_id)
        await self._repository.delete(board_id)
