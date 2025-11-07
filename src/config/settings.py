"""
Configuration management for Bosch LLM Farm integration.

This module handles configuration loading from environment variables
and configuration files, ensuring secure credential management.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class BoschFarmConfig:
    """Configuration settings for Bosch LLM Farm integration."""
    
    # Core settings
    farm_api_key: Optional[str] = None
    base_url: Optional[str] = None
    api_version: str = "2024-08-01-preview"
    
    # Default deployment settings
    default_model: str = "gpt-4o-mini"
    
    # HTTP settings
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> "BoschFarmConfig":
        """Load configuration from environment variables."""
        return cls(
            farm_api_key=os.getenv("BOSCH_FARM_API_KEY"),
            base_url=os.getenv(
                "BOSCH_FARM_BASE_URL",
                "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18"
            ),
            api_version=os.getenv("BOSCH_FARM_API_VERSION", "2024-08-01-preview"),
            default_model=os.getenv("BOSCH_FARM_DEFAULT_MODEL", "gpt-4o-mini"),
            timeout=int(os.getenv("BOSCH_FARM_TIMEOUT", "30")),
            max_retries=int(os.getenv("BOSCH_FARM_MAX_RETRIES", "3"))
        )
    
    @classmethod
    def from_file(cls, config_path: str | Path) -> "BoschFarmConfig":
        """Load configuration from a JSON or YAML file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                config_data = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                config_data = json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        
        return cls(**config_data.get('bosch_farm', config_data))
    
    @classmethod
    def from_mixed(cls, config_path: Optional[str | Path] = None) -> "BoschFarmConfig":
        """
        Load configuration from both environment variables and config file.
        Environment variables take precedence over config file values.
        """
        # Start with environment variables
        config = cls.from_env()
        
        # Override with config file if provided
        if config_path:
            try:
                file_config = cls.from_file(config_path)
                
                # Merge configurations (env vars take precedence)
                if config.farm_api_key is None:
                    config.farm_api_key = file_config.farm_api_key
                if config.base_url == cls().base_url:  # Using default
                    config.base_url = file_config.base_url
                    
                # Override non-sensitive settings from file
                config.timeout = file_config.timeout
                config.max_retries = file_config.max_retries
                config.api_version = file_config.api_version
                config.default_model = file_config.default_model
                
            except Exception as e:
                logger.warning(f"Failed to load config file {config_path}: {e}")
        
        return config
    
    def validate(self) -> None:
        """Validate that required configuration values are present."""
        if not self.farm_api_key:
            raise ValueError(
                "BOSCH_FARM_API_KEY is required. Set it as an environment variable "
                "or provide it in the configuration file."
            )
        
        if not self.base_url:
            raise ValueError("base_url is required")
        
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
    
    def get_headers(self) -> Dict[str, str]:
        """Get the headers required for Bosch Farm API."""
        if not self.farm_api_key:
            raise ValueError("farm_api_key is required for headers")
        
        return {
            "Content-Type": "application/json",
            "genaiplatform-farm-subscription-key": self.farm_api_key
        }
    
    def get_extra_query(self) -> Dict[str, str]:
        """Get the extra query parameters for API requests."""
        return {
            "api-version": self.api_version
        }


def load_config(config_path: Optional[str | Path] = None) -> BoschFarmConfig:
    """
    Convenience function to load and validate configuration.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Validated BoschFarmConfig instance
        
    Raises:
        ValueError: If required configuration is missing
    """
    config = BoschFarmConfig.from_mixed(config_path)
    config.validate()
    return config


# Global configuration instance (lazy loading)
_global_config: Optional[BoschFarmConfig] = None


def get_global_config(config_path: Optional[str | Path] = None) -> BoschFarmConfig:
    """Get or create the global configuration instance."""
    global _global_config
    
    if _global_config is None:
        _global_config = load_config(config_path)
    
    return _global_config


def reset_global_config():
    """Reset the global configuration (useful for testing)."""
    global _global_config
    _global_config = None