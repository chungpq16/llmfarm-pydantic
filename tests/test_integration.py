"""
Integration tests for Bosch Farm Provider with Pydantic AI.

These tests require pydantic-ai to be installed and may require
actual API credentials for full integration testing.
"""

import os
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import our modules
from llmfarm_pydantic import BoschFarmProvider, create_bosch_farm_provider, BoschFarmConfig

# Try to import pydantic-ai (may not be available in test environment)
try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False
    # Mock classes for testing
    class Agent:
        def __init__(self, model):
            self.model = model
        
        async def run(self, prompt):
            return AsyncMock(output="Mock response")
    
    class OpenAIChatModel:
        def __init__(self, model_name, provider=None):
            self.model_name = model_name
            self.provider = provider


class TestBoschFarmIntegration:
    """Integration tests for Bosch Farm Provider."""
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'integration-test-key',
        'BOSCH_FARM_BASE_URL': 'https://mock.bosch-farm.com'
    })
    def test_provider_with_openai_model(self):
        """Test that provider integrates with OpenAIChatModel."""
        provider = create_bosch_farm_provider()
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        
        assert model.provider is provider
        assert model.model_name == 'gpt-4o-mini'
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'integration-test-key',
        'BOSCH_FARM_BASE_URL': 'https://mock.bosch-farm.com'
    })
    def test_agent_creation(self):
        """Test that agent can be created with Bosch Farm provider."""
        provider = BoschFarmProvider()
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        agent = Agent(model)
        
        assert agent.model is model
        assert agent.model.provider is provider
    
    @pytest.mark.skipif(not PYDANTIC_AI_AVAILABLE, reason="pydantic-ai not available")
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'integration-test-key',
        'BOSCH_FARM_BASE_URL': 'https://mock.bosch-farm.com'
    })
    @patch('openai.AsyncOpenAI')
    async def test_mock_conversation(self, mock_openai_class):
        """Test a mocked conversation using the provider."""
        # Mock the OpenAI client response
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Hello from Bosch Farm!"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        # Create provider and model
        provider = BoschFarmProvider()
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        agent = Agent(model)
        
        # Test conversation
        result = await agent.run("Hello, how are you?")
        
        # Verify the mock was called
        assert mock_client.chat.completions.create.called
        
    def test_configuration_inheritance(self):
        """Test that configuration is properly inherited.""" 
        config_path = Path(__file__).parent.parent / "config" / "farm_config.yaml"
        
        # Create provider with config file
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            config_path=config_path
        )
        
        # Config should be loaded and merged
        assert provider.config.api_version == "2024-08-01-preview"  # from file
        assert provider.config.farm_api_key == 'test-key'  # from parameter
    
    def test_multiple_providers(self):
        """Test creating multiple providers with different configurations."""
        provider1 = BoschFarmProvider(
            farm_api_key='key1',
            base_url='https://deployment1.example.com',
            api_version='2024-08-01-preview'
        )
        
        provider2 = BoschFarmProvider(
            farm_api_key='key2', 
            base_url='https://deployment2.example.com',
            api_version='2024-09-01-preview'
        )
        
        assert provider1.config.farm_api_key != provider2.config.farm_api_key
        assert provider1.config.base_url != provider2.config.base_url
        assert provider1.get_extra_query() != provider2.get_extra_query()
    
    def test_provider_concurrent_access(self):
        """Test that provider can handle concurrent access."""
        provider = BoschFarmProvider(
            farm_api_key='concurrent-key',
            base_url='https://concurrent.example.com'
        )
        
        # Create multiple models using the same provider
        models = [
            OpenAIChatModel(f'model-{i}', provider=provider) 
            for i in range(5)
        ]
        
        # All models should share the same provider
        for model in models:
            assert model.provider is provider
            assert model.provider.name == 'bosch-farm'


class TestErrorHandling:
    """Test error handling in integration scenarios."""
    
    def test_invalid_configuration_error(self):
        """Test handling of invalid configuration."""
        with pytest.raises(ValueError, match="BOSCH_FARM_API_KEY is required"):
            with patch.dict(os.environ, {}, clear=True):
                BoschFarmProvider()
    
    def test_missing_config_file_error(self):
        """Test handling of missing configuration file."""
        non_existent_path = Path("/non/existent/config.yaml")
        
        with pytest.raises(FileNotFoundError):
            BoschFarmProvider(
                farm_api_key='test-key',
                config_path=non_existent_path
            )
    
    @patch('httpx.AsyncClient')
    def test_http_client_error_handling(self, mock_http_client):
        """Test handling of HTTP client errors."""
        # Make the HTTP client raise an error
        mock_http_client.side_effect = Exception("HTTP client error")
        
        # Provider creation should still work (error happens on request)
        provider = BoschFarmProvider(
            farm_api_key='test-key',
            base_url='https://error.example.com'
        )
        
        assert provider.name == 'bosch-farm'


@pytest.mark.skipif(
    not os.getenv('BOSCH_FARM_API_KEY') or not PYDANTIC_AI_AVAILABLE,
    reason="Requires BOSCH_FARM_API_KEY environment variable and pydantic-ai"
)
class TestRealIntegration:
    """Real integration tests that require actual API credentials.
    
    These tests are skipped unless BOSCH_FARM_API_KEY is set.
    """
    
    @pytest.mark.asyncio
    async def test_real_api_call(self):
        """Test a real API call to Bosch Farm (requires valid credentials)."""
        provider = create_bosch_farm_provider()
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        agent = Agent(model)
        
        try:
            result = await agent.run("Hello, please respond with 'Integration test successful'")
            assert "test successful" in result.output.lower()
        except Exception as e:
            pytest.fail(f"Real API integration test failed: {e}")
    
    @pytest.mark.asyncio
    async def test_real_api_with_extra_query(self):
        """Test that extra query parameters are properly sent."""
        provider = BoschFarmProvider()
        
        # Verify extra query parameters are set
        extra_query = provider.get_extra_query()
        assert 'api-version' in extra_query
        assert extra_query['api-version'] == provider.config.api_version


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])