import app.errors.exceptions as ex
from app.models.post import Post
from app.repositories.post import PostRepository
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    RequestPostCreateDto,
    RequestPostUpdateDto,
    ResponsePostDto,
)
from app.services.board import BoardService


class PostService:
    def __init__(
        self,
        post_repository: PostRepository,
        board_service: BoardService,
    ):
        self._repository = post_repository
        self.board_service = board_service

    async def create_post(
        self, user_id: int, post_create_dto: RequestPostCreateDto
    ) -> Post:
        await self.board_service.check_board_authorized(
            post_create_dto.board_id, user_id
        )
        post_create = PostCreate(user_id=user_id, **post_create_dto.dict())
        return await self._repository.add(post_create)

    async def check_post_authorized(self, post_id: int, user_id: int) -> None:
        post = await self._repository.get_post_by_post_id(post_id)
        if post and post.user_id != user_id:
            raise ex.PermissionUserError()
        if not post:
            raise ex.PostNotFoundError()

    async def update_post(
        self, post_id: int, user_id: int, post_update_dto: RequestPostUpdateDto
    ) -> None:
        await self.check_post_authorized(post_id, user_id)
        post_update = PostUpdate(id=post_id, user_id=user_id, **post_update_dto.dict())
        await self._repository.update(post_update)

    async def delete_post(self, post_id: int, user_id: int) -> None:
        await self.check_post_authorized(post_id, user_id)
        await self._repository.delete(post_id, user_id)

    async def get_post(self, post_id: int, user_id: int) -> ResponsePostDto:
        post = await self._repository.get_post(post_id, user_id)
        if not post:
            raise ex.PostNotFoundError()
        return ResponsePostDto(**post.__dict__)

    async def list_posts(
        self, board_id: int, user_id: int, cursor_id: int, limit: int
    ) -> list[ResponsePostDto]:
        await self.board_service.check_board_authorized(board_id, user_id)
        post_list = await self._repository.list_posts(board_id, user_id, cursor_id, limit)
        return [ResponsePostDto(**post.__dict__) for post in post_list]
