from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    user_secret_key: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf8',
)
