from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.board import Board
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

    async def add(self, post_create: PostCreate) -> Post:
        async with self.session_factory() as session:
            post = Post(**post_create.dict())
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    async def get_post_by_post_id(self, post_id: int) -> Post | None:
        async with self.session_factory() as session:
            stmt = select(Post).where(Post.id == post_id)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def update(self, post: PostUpdate) -> None:
        async with self.session_factory() as session:
            stmt = (
                update(Post)
                .where(Post.id == post.id, Post.user_id == post.user_id)
                .values(title=post.title, content=post.content)
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, post_id: int, user_id: int) -> None:
        async with self.session_factory() as session:
            stmt = delete(Post).where(Post.id == post_id, Post.user_id == user_id)
            await session.execute(stmt)
            await session.commit()

    async def get_post(self, post_id: int, user_id: int) -> Post | None:
        async with self.session_factory() as session:
            stmt = (
                select(Post)
                .join(Board)
                .where(
                    Post.id == post_id,
                    or_(Post.user_id == user_id, Board.public.is_(True)),
                )
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def list_posts(
        self, board_id: int, user_id: int, cursor_id: int, limit: int
    ) -> list[Post]:
        async with self.session_factory() as session:
            stmt = (
                select(Post)
                .where(
                    Post.id > cursor_id,
                    Post.board_id == board_id,
                    Post.user_id == user_id)
                .limit(limit)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
