import glob

import pytest
from dependency_injector import providers
from fastapi import FastAPI

from app.application import app
from app.config import settings
from app.containers import Container
from app.databases.rdb import RDBDatabase


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


# load all fixtures
pytest_plugins = [
    refactor(fixture)
    for fixture in glob.glob("app/tests/fixtures/*.py")
    if "__" not in fixture
]


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    container = Container()

    container.db.override(
        providers.Singleton(
            RDBDatabase,
            db_url=settings.db.db_url,
            echo=False,
        )
    )

    app.container = container  # type: ignore
    return app
