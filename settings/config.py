from pydantic_settings import BaseSettings

class Secrets(BaseSettings):
    google_key: str
    modal_name: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

secrets = Secrets()