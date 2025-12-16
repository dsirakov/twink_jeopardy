from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/jeopardy"
    )
    OPENAI_API_KEY: str | None = None


settings = Settings()
