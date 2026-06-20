from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────────────────
    APP_NAME: str = "QR Library Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "production"

    # ── Server ─────────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── MongoDB ────────────────────────────────────────────────────────────
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "library_db"
    MONGO_MAX_POOL_SIZE: int = 50
    MONGO_MIN_POOL_SIZE: int = 5

    # ── JWT ────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_REFRESH_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── File Storage ───────────────────────────────────────────────────────
    UPLOAD_DIR: str = "uploads"
    QR_BOOKS_DIR: str = "uploads/qrcodes/books"
    QR_MEMBERS_DIR: str = "uploads/qrcodes/members"

    # ── Business Rules ─────────────────────────────────────────────────────
    BORROW_PERIOD_DAYS: int = 14
    FINE_PER_DAY: float = 5.00

    # ── First Super-Admin seed ─────────────────────────────────────────────
    FIRST_SUPERADMIN_USERNAME: str = "superadmin"
    FIRST_SUPERADMIN_EMAIL: str = "superadmin@library.com"
    FIRST_SUPERADMIN_PASSWORD: str = "SuperAdmin@123"

    # ── Derived helpers ────────────────────────────────────────────────────
    @property
    def qr_books_path(self) -> Path:
        p = Path(self.QR_BOOKS_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def qr_members_path(self) -> Path:
        p = Path(self.QR_MEMBERS_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def upload_path(self) -> Path:
        p = Path(self.UPLOAD_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings singleton."""
    return Settings()


settings: Settings = get_settings()