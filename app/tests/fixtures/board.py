from datetime import datetime
from typing import Any, Callable, Dict

import pytest

from app.models.board import Board


@pytest.fixture
def board_fixture() -> Callable[..., Board]:
    count = 0

    def _board_fixture(**kwargs: Dict[str, Any]) -> Board:
        nonlocal count
        count += 1

        board = Board(
            id=kwargs.pop("id", count),
            name=kwargs.pop("name", f"name{count}"),
            public=kwargs.pop("public", True),
            user_id=kwargs.pop("user_id", count),
            created_dt=kwargs.pop("created_dt", datetime.now()),
            updated_dt=kwargs.pop("updated_dt", datetime.now()),
            **kwargs,
        )

        return board

    return _board_fixture
