from pathlib import Path
from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent

class V1Config(BaseModel):
    prefix: str = Field(default='/v1')

class APIConfig(BaseModel):
    prefix: str = Field(default='/api')

    v1: V1Config = V1Config()

class DocsConfig(BaseModel):
    title: str = Field(default='Swagger UI')

class RedocConfig(BaseModel):
    title: str = Field(default='ReDoc')

class SwaggerConfig(BaseModel):
    static_path: str = Field(default='/src/swagger/static/')
    mount_path: str = Field(default='src/swagger/static')

    docs: DocsConfig = DocsConfig()
    redoc: RedocConfig = RedocConfig()

class ApplicationConfig(BaseModel):
    debug: bool = Field(default=False)
    title: str = Field(default='gomeltrans-api')
    description: str = Field(default='Unofficial API')

    swagger: SwaggerConfig = SwaggerConfig()
    api: APIConfig = APIConfig()

class GomeltransConfig(BaseModel):
    base_url: HttpUrl = Field(default='https://gomeltrans.net/')

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR/'.env',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='CONFIG__',
    )

    gomeltrans: GomeltransConfig = GomeltransConfig()
    app: ApplicationConfig = ApplicationConfig()

settings: Settings = Settings()