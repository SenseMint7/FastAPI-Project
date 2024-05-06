from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


class BoardRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

    async def add(self, board_create: BoardCreate) -> Board:
        async with self.session_factory() as session:
            board = Board(**board_create.dict())
            session.add(board)
            await session.commit()
            await session.refresh(board)
            return board

    async def get_board(self, board_id: int, user_id: int) -> Board | None:
        async with self.session_factory() as session:
            stmt = select(Board).where(
                Board.id == board_id,
                or_(Board.user_id == user_id, Board.public.is_(True)),
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def get_board_by_board_id(self, board_id: int) -> Board | None:
        async with self.session_factory() as session:
            stmt = select(Board).where(
                Board.id == board_id,
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def list_boards(self, user_id: int, cursor_id: int, limit: int) -> list[Board]:
        async with self.session_factory() as session:
            stmt = (
                select(Board)
                .where(
                    Board.id > cursor_id,
                    or_(Board.user_id == user_id, Board.public.is_(True))
                )
                .order_by(Board.id)
                .limit(limit)
            )

            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def update(self, board: BoardUpdate) -> None:
        async with self.session_factory() as session:
            stmt = (
                update(Board)
                .where(Board.id == board.id, Board.user_id == board.user_id)
                .values(name=board.name, public=board.public)
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, board_id: int) -> None:
        async with self.session_factory() as session:
            stmt = delete(Board).where(Board.id == board_id)
            await session.execute(stmt)
            await session.commit()
