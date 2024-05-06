from datetime import timedelta
from typing import Callable
from unittest.mock import AsyncMock

import pytest
from pydantic import EmailStr

import app.errors.exceptions as ex
from app.config import settings
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import RequestUserRegisterDto
from app.services.auth import AuthService
from app.services.user import UserService


@pytest.fixture
def test_user_service() -> tuple[UserService, AuthService, AsyncMock]:
    user_repository_mock = AsyncMock(spec=UserRepository)
    auth_service = AuthService(
        secret_key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        redis=AsyncMock(),
    )
    user_service = UserService(
        auth_service=auth_service, user_repository=user_repository_mock
    )
    return user_service, auth_service, user_repository_mock


@pytest.mark.asyncio
async def test_register_user(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, auth_service, user_repository_mock = test_user_service

    expected_user = user_fixture(password=auth_service.get_password_hash("password1"))
    user_repository_mock.add.return_value = expected_user

    user_dto = RequestUserRegisterDto(
        fullname="fullname1",
        email=EmailStr("email1@test.com"),
        password="password1",
    )
    result = await user_service.register(user_dto)

    assert result.fullname == expected_user.fullname
    assert result.email == expected_user.email
    assert result.password == expected_user.password


@pytest.mark.asyncio
async def test_check_register_user(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, _, user_repository_mock = test_user_service
    user_repository_mock.get_user_by_email.return_value = None

    email = user_fixture().email
    await user_service.check_register_user(email)

    user_repository_mock.get_user_by_email.assert_called_once_with(email)


@pytest.mark.asyncio
async def test_check_register_user_not_found(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, _, user_repository_mock = test_user_service

    user = user_fixture()
    user_repository_mock.get_user_by_email.return_value = user

    with pytest.raises(ex.AlreadyExistsUserError):
        await user_service.check_register_user(user.email)


@pytest.mark.asyncio
async def test_login(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, auth_service, user_repository_mock = test_user_service

    user = user_fixture()
    password = user.password
    user.password = auth_service.get_password_hash(user.password)
    user_repository_mock.get_user_by_email.return_value = user

    result = await user_service.login(user.email, password)

    assert result.fullname == user.fullname
    assert result.email == user.email


@pytest.mark.asyncio
async def test_authenticate_user(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, auth_service, user_repository_mock = test_user_service

    user = user_fixture()
    password = user.password
    user.password = auth_service.get_password_hash(user.password)
    user_repository_mock.get_user_by_email.return_value = user

    result = await user_service.authenticate_user(user.email, password)

    assert result.fullname == user.fullname
    assert result.email == user.email
    assert result.password == user.password


@pytest.mark.asyncio
async def test_authenticate_user_failed(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, auth_service, user_repository_mock = test_user_service

    user = user_fixture()
    password = user.password
    incorrect_password = user_fixture().password
    user.password = auth_service.get_password_hash(incorrect_password)

    user_repository_mock.get_user_by_email.return_value = user

    with pytest.raises(ex.IncorrectUserError):
        await user_service.authenticate_user(user.email, password)


@pytest.mark.asyncio
async def test_get_user_by_email(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
    user_fixture: Callable[..., User],
) -> None:
    user_service, auth_service, user_repository_mock = test_user_service

    test_email = "test1@example.com"

    user_repository_mock.get_user_by_email.return_value = None
    result = await user_service.get_user_by_email(test_email)

    assert result is None

    user = user_fixture(email=test_email)
    user_repository_mock.get_user_by_email.return_value = user
    result = await user_service.get_user_by_email(test_email)

    assert result is not None


@pytest.mark.asyncio
async def test_logout(
    test_user_service: tuple[UserService, AuthService, AsyncMock],
) -> None:
    user_service, _, user_repository_mock = test_user_service
    await user_service.logout("token")
    user_repository_mock.blacklist_token.assert_called_once_with(
        "token", timedelta(minutes=30)
    )
