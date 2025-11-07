"""
Tests for Bosch Farm Provider configuration management.
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llmfarm_pydantic.config.settings import (
    BoschFarmConfig,
    load_config,
    get_global_config,
    reset_global_config
)


class TestBoschFarmConfig:
    """Test cases for BoschFarmConfig class."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        config = BoschFarmConfig()
        
        assert config.farm_api_key is None
        assert config.base_url is None
        assert config.api_version == "2024-08-01-preview"
        assert config.default_model == "gpt-4o-mini"
        assert config.timeout == 30
        assert config.max_retries == 3
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'test-key',
        'BOSCH_FARM_BASE_URL': 'https://test.example.com',
        'BOSCH_FARM_API_VERSION': '2024-09-01',
        'BOSCH_FARM_TIMEOUT': '60'
    })
    def test_from_env(self):
        """Test loading configuration from environment variables."""
        config = BoschFarmConfig.from_env()
        
        assert config.farm_api_key == 'test-key'
        assert config.base_url == 'https://test.example.com'
        assert config.api_version == '2024-09-01'
        assert config.timeout == 60
    
    def test_from_file_yaml(self):
        """Test loading configuration from YAML file."""
        yaml_content = """
bosch_farm:
  farm_api_key: "file-key"
  api_version: "2024-10-01"
  timeout: 45
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            f.flush()
            
            config = BoschFarmConfig.from_file(f.name)
            
            assert config.farm_api_key == 'file-key'
            assert config.api_version == '2024-10-01'
            assert config.timeout == 45
        
        os.unlink(f.name)
    
    def test_from_file_json(self):
        """Test loading configuration from JSON file."""
        json_content = """{
  "bosch_farm": {
    "farm_api_key": "json-key",
    "api_version": "2024-11-01",
    "max_retries": 5
  }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(json_content)
            f.flush()
            
            config = BoschFarmConfig.from_file(f.name)
            
            assert config.farm_api_key == 'json-key'
            assert config.api_version == '2024-11-01'
            assert config.max_retries == 5
        
        os.unlink(f.name)
    
    def test_validate_success(self):
        """Test successful validation."""
        config = BoschFarmConfig(
            farm_api_key="valid-key",
            base_url="https://valid.example.com"
        )
        
        # Should not raise any exception
        config.validate()
    
    def test_validate_missing_api_key(self):
        """Test validation failure with missing API key."""
        config = BoschFarmConfig(
            base_url="https://valid.example.com"
        )
        
        with pytest.raises(ValueError, match="BOSCH_FARM_API_KEY is required"):
            config.validate()
    
    def test_validate_missing_base_url(self):
        """Test validation failure with missing base URL."""
        config = BoschFarmConfig(
            farm_api_key="valid-key"
        )
        
        with pytest.raises(ValueError, match="base_url is required"):
            config.validate()
    
    def test_validate_invalid_timeout(self):
        """Test validation failure with invalid timeout."""
        config = BoschFarmConfig(
            farm_api_key="valid-key",
            base_url="https://valid.example.com",
            timeout=0
        )
        
        with pytest.raises(ValueError, match="timeout must be positive"):
            config.validate()
    
    def test_validate_invalid_retries(self):
        """Test validation failure with invalid retry count."""
        config = BoschFarmConfig(
            farm_api_key="valid-key",
            base_url="https://valid.example.com",
            max_retries=-1
        )
        
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            config.validate()
    
    def test_get_headers(self):
        """Test header generation."""
        config = BoschFarmConfig(farm_api_key="test-key")
        headers = config.get_headers()
        
        expected = {
            "Content-Type": "application/json",
            "genaiplatform-farm-subscription-key": "test-key"
        }
        
        assert headers == expected
    
    def test_get_headers_missing_key(self):
        """Test header generation with missing API key."""
        config = BoschFarmConfig()
        
        with pytest.raises(ValueError, match="farm_api_key is required"):
            config.get_headers()
    
    def test_get_extra_query(self):
        """Test extra query parameter generation."""
        config = BoschFarmConfig(api_version="2024-12-01")
        query = config.get_extra_query()
        
        expected = {"api-version": "2024-12-01"}
        assert query == expected


class TestConfigLoading:
    """Test cases for configuration loading functions."""
    
    def setup_method(self):
        """Reset global config before each test."""
        reset_global_config()
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'env-key',
        'BOSCH_FARM_BASE_URL': 'https://env.example.com'
    })
    def test_load_config_env_only(self):
        """Test loading config from environment only."""
        config = load_config()
        
        assert config.farm_api_key == 'env-key'
        assert config.base_url == 'https://env.example.com'
    
    def test_load_config_missing_credentials(self):
        """Test loading config with missing credentials."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="BOSCH_FARM_API_KEY is required"):
                load_config()
    
    @patch.dict(os.environ, {
        'BOSCH_FARM_API_KEY': 'global-key',
        'BOSCH_FARM_BASE_URL': 'https://global.example.com'
    })
    def test_get_global_config(self):
        """Test global config singleton."""
        config1 = get_global_config()
        config2 = get_global_config()
        
        # Should be the same instance
        assert config1 is config2
        assert config1.farm_api_key == 'global-key'
    
    def test_reset_global_config(self):
        """Test resetting global config."""
        with patch.dict(os.environ, {
            'BOSCH_FARM_API_KEY': 'test-key',
            'BOSCH_FARM_BASE_URL': 'https://test.example.com'
        }):
            config1 = get_global_config()
            reset_global_config()
            config2 = get_global_config()
            
            # Should be different instances after reset
            assert config1 is not config2
            # But should have same values
            assert config1.farm_api_key == config2.farm_api_key


if __name__ == "__main__":
    pytest.main([__file__, "-v"])