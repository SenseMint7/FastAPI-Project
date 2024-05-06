from dependency_injector import containers, providers

from app.config import ApplicationSettings
from app.databases.rdb import RDBDatabase
from app.databases.redis import get_redis
from app.repositories.board import BoardRepository
from app.repositories.post import PostRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.board import BoardService
from app.services.post import PostService
from app.services.user import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.user",
            "app.api.board",
            "app.api.post",
        ]
    )

    config = providers.Configuration()
    config.from_pydantic(ApplicationSettings())

    db = providers.Singleton(
        RDBDatabase,
        db_url=config.db.db_url,
        echo=False,
    )

    redis = providers.Resource(
        get_redis,
        redis_url=config.db.redis_url,
    )

    auth_service = providers.Factory(
        AuthService,
        secret_key=config.SECRET_KEY,
        algorithms=config.ALGORITHM,
        access_token_expire_minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        redis=redis,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
        redis=redis,
    )

    user_service = providers.Factory(
        UserService,
        auth_service=auth_service,
        user_repository=user_repository,
    )

    board_repository = providers.Factory(
        BoardRepository,
        session_factory=db.provided.session,
    )

    board_service = providers.Factory(
        BoardService,
        board_repository=board_repository,
    )

    post_repository = providers.Factory(
        PostRepository,
        session_factory=db.provided.session,
    )

    post_service = providers.Factory(
        PostService,
        post_repository=post_repository,
        board_service=board_service,
    )
