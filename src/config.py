from pydantic_settings import BaseSettings, EnvSettingsSource, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str

    JWT_SECRET: str
    SESSION_SECRET: str
    
    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_DB: int

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_URL: str
    MINIO_PORT: int
    MINIO_ADMIN_PORT: int
    
    ADMIN_LOGIN: str
    ADMIN_PASS: str
    
    @property
    def database_url(self):
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    
    @property
    def async_database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    
    @property
    def jwt_secret(self):
        return self.JWT_SECRET
    
    
    @property
    def origins(self):
        return [
            "http://localhost:8000",
            "http://localhost:5173",
        ]
    
    model_config = SettingsConfigDict(env_file = '../.env')
    

settings = Settings()