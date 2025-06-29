"""
Tests for the configuration module.
"""

import os
import pytest
from unittest.mock import patch

from firecrawl_tools.config import FirecrawlConfig, get_config
from firecrawl_tools.exceptions import ConfigurationError


class TestFirecrawlConfig:
    """Test the FirecrawlConfig class."""
    
    def test_config_creation(self):
        """Test creating a config with required fields."""
        config = FirecrawlConfig(api_key="test_key")
        assert config.api_key == "test_key"
        assert config.timeout == 30
        assert config.max_retries == 3
    
    def test_config_with_all_fields(self):
        """Test creating a config with all fields."""
        config = FirecrawlConfig(
            api_key="test_key",
            base_url="https://api.example.com",
            timeout=60,
            max_retries=5
        )
        assert config.api_key == "test_key"
        assert config.base_url == "https://api.example.com"
        assert config.timeout == 60
        assert config.max_retries == 5
    
    def test_from_env_success(self):
        """Test creating config from environment variables."""
        with patch.dict(os.environ, {"FIRECRAWL_API_KEY": "env_key"}):
            config = FirecrawlConfig.from_env()
            assert config.api_key == "env_key"
            assert config.timeout == 30
    
    def test_from_env_missing_key(self):
        """Test creating config from env when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ConfigurationError, match="FIRECRAWL_API_KEY environment variable is required"):
                FirecrawlConfig.from_env()
    
    def test_from_env_with_custom_values(self):
        """Test creating config from env with custom timeout and retries."""
        with patch.dict(os.environ, {
            "FIRECRAWL_API_KEY": "env_key",
            "FIRECRAWL_TIMEOUT": "60",
            "FIRECRAWL_MAX_RETRIES": "5"
        }):
            config = FirecrawlConfig.from_env()
            assert config.api_key == "env_key"
            assert config.timeout == 60
            assert config.max_retries == 5
    
    def test_from_dict_success(self):
        """Test creating config from dictionary."""
        config_dict = {
            "firecrawl_api_key": "dict_key",
            "timeout": 45,
            "max_retries": 4
        }
        config = FirecrawlConfig.from_dict(config_dict)
        assert config.api_key == "dict_key"
        assert config.timeout == 45
        assert config.max_retries == 4
    
    def test_from_dict_with_api_key_field(self):
        """Test creating config from dictionary with api_key field."""
        config_dict = {
            "api_key": "direct_key",
            "timeout": 45
        }
        config = FirecrawlConfig.from_dict(config_dict)
        assert config.api_key == "direct_key"
        assert config.timeout == 45


class TestGetConfig:
    """Test the get_config function."""
    
    def test_get_config_with_api_key(self):
        """Test getting config with direct API key."""
        config = get_config(api_key="direct_key")
        assert config.api_key == "direct_key"
    
    def test_get_config_with_dict(self):
        """Test getting config with dictionary."""
        config_dict = {"firecrawl_api_key": "dict_key"}
        config = get_config(config_dict=config_dict)
        assert config.api_key == "dict_key"
    
    def test_get_config_from_env(self):
        """Test getting config from environment."""
        with patch.dict(os.environ, {"FIRECRAWL_API_KEY": "env_key"}):
            config = get_config()
            assert config.api_key == "env_key"
    
    def test_get_config_no_source(self):
        """Test getting config when no source is provided."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ConfigurationError, match="No valid configuration found"):
                get_config()
    
    def test_get_config_priority(self):
        """Test that direct API key takes priority over other sources."""
        with patch.dict(os.environ, {"FIRECRAWL_API_KEY": "env_key"}):
            config_dict = {"firecrawl_api_key": "dict_key"}
            config = get_config(api_key="direct_key", config_dict=config_dict)
            assert config.api_key == "direct_key"
    
    def test_get_config_dict_priority_over_env(self):
        """Test that config dict takes priority over environment."""
        with patch.dict(os.environ, {"FIRECRAWL_API_KEY": "env_key"}):
            config_dict = {"firecrawl_api_key": "dict_key"}
            config = get_config(config_dict=config_dict)
            assert config.api_key == "dict_key" 