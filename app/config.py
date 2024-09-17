from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    db_name: str = "fastapi"
    form_collection_name: str = "forms"
    counter_collection_name: str = "counters"
    form_id_prefix: str = "form-"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
