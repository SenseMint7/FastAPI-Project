import os

from alembic import command, config

from app.config import DatabaseSettings


def main():
    db_config = DatabaseSettings()
    username = db_config.db_user
    password = db_config.db_password
    host = db_config.db_host
    port = db_config.db_port
    database = db_config.db_name
    current_dir = os.getcwd()
    alembic_config = config.Config(current_dir + "/alembic.ini")
    alembic_config.set_main_option(
        "sqlalchemy.url",
        f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}",
    )
    command.upgrade(config=alembic_config, revision="head")


if __name__ == "__main__":
    main()
