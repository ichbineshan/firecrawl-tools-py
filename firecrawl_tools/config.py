"""
Configuration management for Firecrawl Tools.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field

from .exceptions import ConfigurationError


class FirecrawlConfig(BaseModel):
    """Configuration for Firecrawl Tools."""
    
    api_key: str = Field(..., description="Firecrawl API key")
    base_url: Optional[str] = Field(
        default=None, 
        description="Base URL for Firecrawl API (optional)"
    )
    timeout: int = Field(
        default=30, 
        description="Default timeout in seconds for API calls"
    )
    max_retries: int = Field(
        default=3, 
        description="Maximum number of retries for failed requests"
    )
    
    @classmethod
    def from_env(cls) -> "FirecrawlConfig":
        """Create configuration from environment variables."""
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "FIRECRAWL_API_KEY environment variable is required"
            )
        
        return cls(
            api_key=api_key,
            base_url=os.getenv("FIRECRAWL_BASE_URL"),
            timeout=int(os.getenv("FIRECRAWL_TIMEOUT", "30")),
            max_retries=int(os.getenv("FIRECRAWL_MAX_RETRIES", "3")),
        )
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "FirecrawlConfig":
        """Create configuration from a dictionary."""
        if "firecrawl_api_key" in config_dict:
            config_dict["api_key"] = config_dict.pop("firecrawl_api_key")
        
        return cls(**config_dict)


def get_config(api_key: Optional[str] = None, config_dict: Optional[dict] = None) -> FirecrawlConfig:
    """
    Get Firecrawl configuration from various sources.
    
    Priority order:
    1. Direct api_key parameter
    2. config_dict parameter
    3. Environment variables
    
    Args:
        api_key: Direct API key string
        config_dict: Configuration dictionary
        
    Returns:
        FirecrawlConfig instance
        
    Raises:
        ConfigurationError: If no valid configuration is found
    """
    if api_key:
        return FirecrawlConfig(api_key=api_key)
    
    if config_dict:
        return FirecrawlConfig.from_dict(config_dict)
    
    try:
        return FirecrawlConfig.from_env()
    except ConfigurationError:
        raise ConfigurationError(
            "No valid configuration found. Please provide api_key, config_dict, "
            "or set FIRECRAWL_API_KEY environment variable."
        ) 