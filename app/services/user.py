from datetime import datetime, timedelta

from passlib.context import CryptContext

import app.errors.exceptions as ex
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import RequestUserRegisterDto, ResponseUserLoginDto
from app.services.auth import AuthService


class UserService:
    def __init__(
        self,
        auth_service: AuthService,
        user_repository: UserRepository,
    ) -> None:
        self.auth_service: AuthService = auth_service
        self._repository: UserRepository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, user_dto: RequestUserRegisterDto) -> User:
        user_dto.password = self.auth_service.get_password_hash(user_dto.password)
        return await self._repository.add(user_dto)

    async def check_register_user(self, email: str) -> None:
        user = await self.get_user_by_email(email)
        if user:
            raise ex.AlreadyExistsUserError()

    async def login(self, email: str, password: str) -> ResponseUserLoginDto:
        user = await self.authenticate_user(email, password)

        expires_delta = timedelta(minutes=self.auth_service.access_token_expire_minutes)
        expire = datetime.utcnow() + expires_delta

        access_token = self.auth_service.create_access_token(
            {"sub": str(user.id)},
            expire,
        )

        return ResponseUserLoginDto(
            fullname=user.fullname,
            email=user.email,
            access_token=access_token,
        )

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user(email)
        if not self.auth_service.verify_password(password, user.password):
            raise ex.IncorrectUserError()

        return user

    async def get_user(self, email: str) -> User:
        user = await self._repository.get_user_by_email(email)
        if not user:
            raise ex.UserNotFoundError()

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self._repository.get_user_by_email(email)

    async def logout(self, token: str) -> None:
        expire = self.auth_service.access_token_expire_minutes
        expire_delta = timedelta(minutes=expire)
        await self._repository.blacklist_token(token, expire_delta)
