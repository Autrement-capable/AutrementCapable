"""
Configuration module for image handling.
"""
from typing import Dict, List, Any, Set
from pydantic import BaseModel

from .config import Config

class PictureConfig(BaseModel):
    """Image handling configuration"""
    max_size: int
    chunk_size: int
    max_width: int
    max_height: int
    min_width: int
    min_height: int
    allowed_types: List[str]
    avif_quality: int = 70  # Default value if not specified in config

    @classmethod
    def from_config(cls) -> 'PictureConfig':
        """
        Load picture configuration from the config file.

        Returns:
            PictureConfig: Configuration for image handling
        """
        # Load from config file
        try:
            config = Config.get_property(None, "picture", [
                "max_size", "chunk_size", "max_width", "max_height", 
                "min_width", "min_height", "allowed_types", "avif_quality"
            ])
        except KeyError:
            # Fallback to defaults if some keys are missing
            config = Config.get_property(None, "picture", [])

        # Default values
        defaults = {
            "max_size": 5 * 1024 * 1024,  # 5MB
            "chunk_size": 512 * 1024,  # 512KB
            "max_width": 1920,
            "max_height": 1080,
            "min_width": 100,
            "min_height": 100,
            "allowed_types": ["image/jpeg", "image/png", "image/avif", "image/webp"],
            "avif_quality": 70
        }

        # Merge config with defaults
        merged_config = {**defaults, **config}

        return cls(**merged_config)

# Global instance
picture_config = PictureConfig.from_config()

# MIME type mapping
MIME_TYPE_TO_PIL_FORMAT = {
    "image/jpeg": "JPEG",
    "image/png": "PNG",
    "image/webp": "WEBP",
    "image/avif": "AVIF",
}

def get_allowed_mime_types() -> Set[str]:
    """
    Get the set of allowed MIME types.

    Returns:
        Set[str]: Allowed MIME types
    """
    return set(picture_config.allowed_types)

def is_mime_type_allowed(mime_type: str) -> bool:
    """
    Check if a MIME type is allowed.

    Args:
        mime_type: MIME type to check

    Returns:
        bool: True if allowed, False otherwise
    """
    return mime_type in get_allowed_mime_types()

def get_pil_format(mime_type: str) -> str:
    """
    Get the PIL format for a MIME type.

    Args:
        mime_type: MIME type

    Returns:
        str: PIL format

    Raises:
        ValueError: If the MIME type is not supported
    """
    if mime_type not in MIME_TYPE_TO_PIL_FORMAT:
        raise ValueError(f"Unsupported MIME type: {mime_type}")

    return MIME_TYPE_TO_PIL_FORMAT[mime_type]