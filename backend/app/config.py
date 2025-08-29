# AiInternTask/chatbot_theme_identifier/backend/app/config.py
"""
This module defines the configuration settings for the Document Research & Theme Identification API.
It uses Pydantic for settings management and loads environment variables.
"""
import os
from pathlib import Path
from typing import Set
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# # Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """
    Settings class for the Document Research & Theme Identification API.

    Parameters
    ----------
    BaseSettings : pydantic_settings.BaseSettings
        This class inherits from BaseSettings to manage configuration settings for the API.
    """
    # API Configuration
    PROJECT_NAME: str = "Document Research & Theme Identification API"
    API_V1_STR: str = "/api/v1"

    # Security
    GEMINI_API_KEY: str | None = os.environ.get("GEMINI_API_KEY")

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_FOLDER: Path = DATA_DIR / "uploads"
    CHROMA_PERSIST_DIR: Path = DATA_DIR / "chroma"

    # Document settings
    ALLOWED_EXTENSIONS: Set[str] = {"pdf", "txt", "png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH: int = 200 * 1024 * 1024  # 200MB

    # Vector store settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Model settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GEMINI_MODEL: str = "gemini-pro"

    def init_folders(self):
        """Create necessary folders if they don't exist"""
        folders = [self.UPLOAD_FOLDER, self.CHROMA_PERSIST_DIR]
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

    class Config:
        env_file = ".env"


# Create global Config instance that matches the import in services
Config = Settings()

# Initialize folders on import
Config.init_folders()
