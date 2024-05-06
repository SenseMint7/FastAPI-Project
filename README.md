# FastAPI-Project
### FastAPI 를 사용한 게시판 프로젝트입니다. 현재 코딩 스타일을 알 수 있습니다.

## 설명
- Application, Service, Repository 계층 구조로 나누어 개발하였습니다.
- Dependency Injection 을 사용하여 DI 를 적용하였습니다.
- Alembic 을 사용하여 DB migration 을 적용하였습니다.
- SQLAlchemy 를 사용하여 ORM 을 적용하였습니다.
- mypy, ruff, pytest 를 사용하여 코드 품질을 관리하였습니다.

## 개발 환경
- MacBook Pro M1
- macOS Monterey 12.3.1

## Skill
- python > 3.11
- FastAPI
- Dependency Injector
- SQLAlchemy
- psycopg2-binary
- alembic

## 실행 방법
### docker compose 를 통한 실행
```sh
$ docker compose up -d
```

### 로컬에서의 실행
```sh
$ docker compose up -d postgres redis
$ pip install poetry
$ poetry install
$ sh -c make migrate # db migration
$ uvicorn app.application:app --host 0.0.0.0 --port 8000
```

### 테스트
```sh
# root folder 에서 실행하여야합니다.
$ pytest
```
