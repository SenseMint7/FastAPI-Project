from datetime import datetime
from typing import Any, Callable, Dict

import pytest

from app.models.user import User


@pytest.fixture
def user_fixture() -> Callable[..., User]:
    count = 0

    def _user_fixture(**kwargs: Dict[str, Any]) -> User:
        nonlocal count
        count += 1

        user = User(
            id=kwargs.pop("id", count),
            fullname=kwargs.pop("fullname", f"fullname{count}"),
            email=kwargs.pop("email", f"email{count}@test.com"),
            password=kwargs.pop("password", f"password{count}"),
            created_dt=kwargs.pop("created_dt", datetime.now()),
            updated_dt=kwargs.pop("updated_dt", datetime.now()),
            **kwargs,
        )

        return user

    return _user_fixture
