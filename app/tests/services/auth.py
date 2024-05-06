from datetime import datetime, timedelta
from typing import Callable
from unittest.mock import AsyncMock

import pytest

import app.errors.exceptions as ex
from app.config import settings
from app.models.user import User
from app.services.auth import AuthService


@pytest.fixture
def test_auth_service() -> AuthService:
    auth_service = AuthService(
        secret_key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        redis=AsyncMock(),
    )
    return auth_service


def test_get_current_user(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    user_id = user_fixture().id
    token = test_auth_service.create_access_token(
        {"sub": str(user_id)},
        None,
    )
    test_auth_service.redis.get = AsyncMock(return_value=None)

    result_user_id, result_token = test_auth_service.get_current_user(token)

    assert user_id == result_user_id
    assert token == result_token


def test_get_current_user_not_match(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    user_id = user_fixture().id
    not_match_user_id = user_fixture().id
    token = test_auth_service.create_access_token(
        {"sub": str(user_id)},
        None,
    )
    result_user_id, _ = test_auth_service.get_current_user(token)

    assert not_match_user_id != result_user_id


@pytest.mark.asyncio
async def test_check_blacklist(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    test_auth_service.redis.get = AsyncMock(return_value="token")
    with pytest.raises(ex.InvalidTokenError):
        await test_auth_service.check_blacklist("token")


@pytest.mark.asyncio
async def test_check_not_blacklist(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    test_auth_service.redis.get = AsyncMock(return_value=None)
    await test_auth_service.check_blacklist("token")


def test_get_current_user_expired(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    expire = datetime.utcnow() - timedelta(minutes=30)
    mock_access_token = test_auth_service.create_access_token(
        {"sub": user_fixture().email},
        expire,
    )
    with pytest.raises(ex.ExpiredSignatureError):
        test_auth_service.get_current_user(mock_access_token)


def test_verify_password(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    password = user_fixture().password
    hashed_password = test_auth_service.get_password_hash(password)
    assert True is test_auth_service.verify_password(password, hashed_password)


def test_verify_password_failed(
    test_auth_service: AuthService, user_fixture: Callable[..., User]
) -> None:
    password = user_fixture().password
    failed_password = user_fixture().password
    hashed_password = test_auth_service.get_password_hash(password)
    assert False is test_auth_service.verify_password(failed_password, hashed_password)
