"""
Tests for Bosch Farm Provider.
"""

import os
import pytest
import httpx
from unittest.mock import AsyncMock, Mock, patch
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llmfarm_pydantic.providers.bosch_farm import BoschFarmProvider, create_bosch_farm_provider
from llmfarm_pydantic.config.settings import BoschFarmConfig


class TestBoschFarmProvider:
    """Test cases for BoschFarmProvider class."""
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'test-key',
        'BOSCH_FARM_BASE_URL': 'https://test.example.com'
    })
    def test_provider_creation_from_env(self):
        """Test creating provider from environment variables."""
        provider = BoschFarmProvider()
        
        assert provider.name == 'bosch-farm'
        assert 'test.example.com' in provider.base_url
        assert provider.config.farm_api_key == 'test-key'
    
    def test_provider_creation_with_params(self):
        """Test creating provider with explicit parameters."""
        provider = BoschFarmProvider(
            farm_api_key='param-key',
            base_url='https://param.example.com'
        )
        
        assert provider.name == 'bosch-farm'
        assert provider.config.farm_api_key == 'param-key'
        assert provider.config.base_url == 'https://param.example.com'
    
    def test_provider_creation_missing_credentials(self):
        """Test creating provider without credentials raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="BOSCH_FARM_API_KEY is required"):
                BoschFarmProvider()
    
    def test_provider_with_custom_http_client(self):
        """Test creating provider with custom HTTP client."""
        custom_client = httpx.AsyncClient(timeout=60)
        
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://test.example.com',
            http_client=custom_client
        )
        
        assert provider.name == 'bosch-farm'
        # The custom client should be used by the AsyncOpenAI client
        assert provider.client.http_client is custom_client
    
    @patch('openai.AsyncOpenAI')
    def test_provider_with_existing_openai_client(self, mock_openai):
        """Test creating provider with existing OpenAI client."""
        mock_client = AsyncMock()
        mock_client.base_url = 'https://existing.example.com'
        
        provider = BoschFarmProvider(openai_client=mock_client)
        
        assert provider.name == 'bosch-farm'
        assert provider.client is mock_client
    
    def test_get_extra_query(self):
        """Test getting extra query parameters."""
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://test.example.com',
            api_version='2024-12-01'
        )
        
        query = provider.get_extra_query()
        assert query == {'api-version': '2024-12-01'}
    
    def test_provider_repr(self):
        """Test string representation of provider."""
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://test.example.com'
        )
        
        repr_str = repr(provider)
        assert 'BoschFarmProvider' in repr_str
        assert 'bosch-farm' in repr_str
    
    def test_model_profile(self):
        """Test model profile method."""
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://test.example.com'
        )
        
        # Currently returns None, could be extended for Bosch-specific profiles
        profile = provider.model_profile('gpt-4o-mini')
        assert profile is None


class TestCreateBoschFarmProvider:
    """Test cases for convenience function."""
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'convenience-key',
        'BOSCH_FARM_BASE_URL': 'https://convenience.example.com'
    })
    def test_create_provider_convenience(self):
        """Test convenience function for creating provider."""
        provider = create_bosch_farm_provider()
        
        assert isinstance(provider, BoschFarmProvider)
        assert provider.name == 'bosch-farm'
        assert provider.config.farm_api_key == 'convenience-key'
    
    def test_create_provider_with_params(self):
        """Test convenience function with parameters."""
        provider = create_bosch_farm_provider(
            farm_api_key='convenience-param-key'
        )
        
        assert provider.config.farm_api_key == 'convenience-param-key'


class TestProviderIntegration:
    """Integration tests for provider functionality."""
    
    def test_provider_headers_configuration(self):
        """Test that provider correctly configures headers."""
        provider = BoschFarmProvider(
            farm_api_key='integration-key',
            base_url='https://integration.example.com'
        )
        
        # Check that the AsyncOpenAI client has correct headers
        client = provider.client
        assert hasattr(client, '_default_headers')
        
        # The headers should include the farm subscription key
        headers = provider.config.get_headers()
        assert 'genaiplatform-farm-subscription-key' in headers
        assert headers['genaiplatform-farm-subscription-key'] == 'integration-key'
    
    def test_provider_api_key_dummy(self):
        """Test that provider uses dummy API key for OpenAI client."""
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://test.example.com'
        )
        
        # The OpenAI client should use "dummy" as API key
        client = provider.client
        assert client.api_key == "dummy"
    
    @pytest.mark.asyncio
    async def test_provider_cleanup(self):
        """Test that provider can be properly cleaned up."""
        custom_client = httpx.AsyncClient()
        
        provider = BoschFarmProvider(
            farm_api_key='cleanup-key',
            base_url='https://cleanup.example.com',
            http_client=custom_client
        )
        
        # Cleanup should work without errors
        await provider.client.close()
        await custom_client.aclose()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])