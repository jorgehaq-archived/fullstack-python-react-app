import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Información del proyecto
    PROJECT_NAME: str = "Full Stack App"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Full Stack Application with Python Backend and React Frontend"
    
    # Prefijo de API
    API_PREFIX: str = "/api"
    
    # Variables de entorno para BD
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/app_db"
    )
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 días
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend React
        "http://localhost:8000",  # Backend API
        "http://frontend:3000",   # Docker frontend
    ]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Instancia global de configuración
settings = Settings()