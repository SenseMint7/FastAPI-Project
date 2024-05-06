from contextlib import AbstractAsyncContextManager
from datetime import timedelta
from typing import Callable

from redis import asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import RequestUserRegisterDto


class UserRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        redis: aioredis.Redis,
    ) -> None:
        self.session_factory = session_factory
        self.redis = redis

    async def add(self, user_dto: RequestUserRegisterDto) -> User:
        async with self.session_factory() as session:
            user = User(**user_dto.dict())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.session_factory() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def blacklist_token(self, token: str, expire_delta: timedelta) -> None:
        await self.redis.set(token, "blacklist", ex=expire_delta)
