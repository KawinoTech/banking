from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_host : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expiration : int

    class Config:
        env_file=".env"

settings = Settings()