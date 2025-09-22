from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "YouTube Audience Analyzer"
    debug: bool = True
    upload_dir: str = "./uploads/"
    max_file_size: int = 10 * 1024 * 1024
    allowed_extensions: list = [".csv"]

    class Config:
        env_file = ".env"

settings = Settings()