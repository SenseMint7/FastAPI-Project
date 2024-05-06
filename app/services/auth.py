from datetime import datetime, timedelta
from typing import Annotated, Optional, Union

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.jwt import ExpiredSignatureError, JWTError  # type: ignore
from passlib.context import CryptContext
from redis import asyncio as aioredis

import app.errors.exceptions as ex
from app.config import settings

oauth2_scheme = HTTPBearer()


class AuthService:
    def __init__(
        self,
        secret_key: str,
        algorithms: str,
        access_token_expire_minutes: str,
        redis: aioredis.Redis,
    ) -> None:
        self.secret_key = secret_key
        self.algorithms = algorithms
        self.access_token_expire_minutes = int(access_token_expire_minutes)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.redis = redis

    @staticmethod
    def get_current_user(
        credentials: Annotated[
            Union[HTTPAuthorizationCredentials, str], Security(oauth2_scheme)
        ],
    ) -> tuple[int, str]:
        try:
            if isinstance(credentials, str):
                token = credentials
                payload = jwt.decode(
                    token=credentials,
                    key=settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
            else:
                token = credentials.credentials
                payload = jwt.decode(
                    token=credentials.credentials,
                    key=settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
            user_id = payload.get("sub")
            if user_id is None:
                raise ex.InvalidTokenError()
        except ExpiredSignatureError:
            raise ex.ExpiredSignatureError() from ExpiredSignatureError
        except JWTError:
            raise ex.InvalidTokenError() from JWTError
        return int(user_id), token

    async def check_blacklist(self, token: str) -> None:
        if await self.redis.get(token):
            raise ex.InvalidTokenError()

    def create_access_token(
        self, data: dict[str, Union[str, datetime]], expire: Optional[datetime]
    ) -> str:
        to_encode = data.copy()
        if not expire:
            expires_delta = timedelta(minutes=self.access_token_expire_minutes)
            expire = datetime.now() + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithms
        )
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
