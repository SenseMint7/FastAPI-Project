from typing import Optional


class StatusCode:
    HTTP_500 = 500
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_409 = 409


class APIException(Exception):
    status_code: int
    code: str
    message: Optional[str]

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        message: Optional[str] = "오류가 발생했습니다. 시스템 관리자에게 문의해주세요",
    ):
        self.status_code = status_code
        self.code = code
        self.message = message


class ExpiredSignatureError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'1'.zfill(3)}",
            message="세션이 만료되었습니다. 다시 로그인 해주세요.",
        )


class InvalidTokenError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'2'.zfill(3)}",
            message="유효하지 않은 토큰입니다.",
        )


class IncorrectUserError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'3'.zfill(3)}",
            message="비밀번호가 일치하지 않습니다.",
        )


class UserNotFoundError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_404,
            code=f"{StatusCode.HTTP_404}{'4'.zfill(3)}",
            message="계정이 없습니다. 계정을 생성해 주세요.",
        )


class AlreadyExistsUserError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_409,
            code=f"{StatusCode.HTTP_409}{'5'.zfill(3)}",
            message="이미 계정이 존재합니다. 다른 ID를 작성해 주세요.",
        )


class PermissionUserError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_403,
            code=f"{StatusCode.HTTP_403}{'6'.zfill(3)}",
            message="권한이 없습니다.",
        )


class BoardNotFoundError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_403,
            code=f"{StatusCode.HTTP_403}{'7'.zfill(3)}",
            message="게시판을 찾을 수 없습니다.",
        )


class AlreadyExistsBoardError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_409,
            code=f"{StatusCode.HTTP_409}{'8'.zfill(3)}",
            message="이미 해당 이름의 게시판이 존재합니다.",
        )


class PostNotFoundError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_403,
            code=f"{StatusCode.HTTP_403}{'9'.zfill(3)}",
            message="게시글을 찾을 수 없습니다.",
        )
