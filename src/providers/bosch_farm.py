"""
Bosch Farm Provider for Pydantic AI.

This module provides the BoschFarmProvider class that integrates with
Bosch's corporate LLM Farm using the OpenAI-compatible API.
"""

import os
import httpx
from typing import Optional, overload
from openai import AsyncOpenAI
from pathlib import Path
import logging

# Import Pydantic AI components
# Note: These imports should be adjusted based on actual pydantic-ai package structure
try:
    from pydantic_ai import Provider
    from pydantic_ai.models.openai import cached_async_http_client
except ImportError:
    # Fallback for development/testing
    logging.warning("pydantic_ai not found. Using mock imports for development.")
    from abc import ABC, abstractmethod
    from typing import Generic, TypeVar
    
    T = TypeVar('T')
    
    class Provider(ABC, Generic[T]):
        """Mock Provider class for development."""
        _client: T
        
        @property
        @abstractmethod
        def name(self) -> str:
            pass
        
        @property
        @abstractmethod
        def base_url(self) -> str:
            pass
        
        @property
        @abstractmethod
        def client(self) -> T:
            pass
    
    def cached_async_http_client(provider: str) -> httpx.AsyncClient:
        """Mock cached client for development."""
        return httpx.AsyncClient()

from ..config.settings import BoschFarmConfig, load_config

logger = logging.getLogger(__name__)


class BoschFarmProvider(Provider[AsyncOpenAI]):
    """Provider for Bosch Corporate LLM Farm API."""
    
    def __init__(
        self,
        farm_api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        config_path: Optional[str | Path] = None,
        openai_client: Optional[AsyncOpenAI] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """
        Create a new Bosch Farm provider.

        Args:
            farm_api_key: The genaiplatform-farm-subscription-key for authentication.
                If not provided, will be loaded from BOSCH_FARM_API_KEY environment variable.
            base_url: The base URL for the Bosch Farm deployment.
                If not provided, uses default deployment URL or BOSCH_FARM_BASE_URL env var.
            api_version: The API version for requests (default: "2024-08-01-preview").
            config_path: Optional path to configuration file.
            openai_client: An existing AsyncOpenAI client to use.
                If provided, other parameters must be None.
            http_client: An existing httpx.AsyncClient to use for HTTP requests.
        
        Raises:
            ValueError: If required configuration is missing or invalid parameters provided.
        """
        # Load configuration
        if openai_client is None:
            self.config = self._load_configuration(
                farm_api_key, base_url, api_version, config_path
            )
        else:
            # If using existing client, minimal config needed
            self.config = BoschFarmConfig(
                farm_api_key=farm_api_key or "dummy",
                base_url=base_url or "dummy",
                api_version=api_version or "2024-08-01-preview"
            )
        
        # Initialize the AsyncOpenAI client
        self._initialize_client(openai_client, http_client)
        
        logger.info(f"Bosch Farm provider initialized with base_url: {self.config.base_url}")
    
    @property
    def name(self) -> str:
        """The provider name."""
        return 'bosch-farm'
    
    @property
    def base_url(self) -> str:
        """The base URL for the provider API."""
        return str(self._client.base_url)
    
    @property
    def client(self) -> AsyncOpenAI:
        """The AsyncOpenAI client for the provider."""
        return self._client
    
    def get_extra_query(self) -> dict[str, str]:
        """
        Get the extra query parameters needed for Bosch Farm API.
        
        Returns:
            Dictionary with api-version parameter
        """
        return self.config.get_extra_query()
    
    def model_profile(self, model_name: str) -> None:
        """
        Model profile for Bosch Farm models.
        
        Note: Bosch Farm uses OpenAI-compatible models, so we rely on
        the default OpenAI model profiles. Override this method if
        specific model profiles are needed for Bosch Farm models.
        """
        # Could implement Bosch-specific model profiles here if needed
        return None
    
    def _load_configuration(
        self, 
        farm_api_key: Optional[str],
        base_url: Optional[str], 
        api_version: Optional[str],
        config_path: Optional[str | Path]
    ) -> BoschFarmConfig:
        """Load and validate configuration from multiple sources."""
        # Start with environment/file config
        config = load_config(config_path)
        
        # Override with explicitly provided parameters
        if farm_api_key is not None:
            config.farm_api_key = farm_api_key
        if base_url is not None:
            config.base_url = base_url
        if api_version is not None:
            config.api_version = api_version
        
        # Validate final configuration
        config.validate()
        
        return config
    
    def _initialize_client(
        self,
        openai_client: Optional[AsyncOpenAI],
        http_client: Optional[httpx.AsyncClient]
    ) -> None:
        """Initialize the AsyncOpenAI client with Bosch Farm configuration."""
        
        if openai_client is not None:
            # Use provided client directly
            self._client = openai_client
            logger.debug("Using provided AsyncOpenAI client")
            return
        
        # Set up authentication headers
        headers = self.config.get_headers()
        
        # Create HTTP client if not provided
        if http_client is None:
            try:
                http_client = cached_async_http_client(provider='bosch-farm')
            except:
                # Fallback if cached client not available
                http_client = httpx.AsyncClient(
                    timeout=self.config.timeout,
                    follow_redirects=True,
                    limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
                )
        
        # Create AsyncOpenAI client
        self._client = AsyncOpenAI(
            api_key="dummy",  # Required by OpenAI client, but auth is via headers
            base_url=self.config.base_url,
            default_headers=headers,
            http_client=http_client,
            max_retries=self.config.max_retries
        )
        
        logger.debug(f"Created AsyncOpenAI client for Bosch Farm")
    
    def __repr__(self) -> str:
        """String representation of the provider."""
        return f"BoschFarmProvider(name={self.name}, base_url={self.base_url})"


# Convenience function for easy provider creation
def create_bosch_farm_provider(
    farm_api_key: Optional[str] = None,
    config_path: Optional[str | Path] = None,
    **kwargs
) -> BoschFarmProvider:
    """
    Convenience function to create a BoschFarmProvider.
    
    Args:
        farm_api_key: The farm subscription key
        config_path: Path to config file
        **kwargs: Additional parameters passed to BoschFarmProvider
    
    Returns:
        Configured BoschFarmProvider instance
    """
    return BoschFarmProvider(
        farm_api_key=farm_api_key,
        config_path=config_path,
        **kwargs
    )