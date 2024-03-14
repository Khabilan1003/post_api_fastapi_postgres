from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_name: str
    database_user: str
    database_host: str
    database_password: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()