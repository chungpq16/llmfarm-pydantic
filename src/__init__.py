"""
Pydantic AI integration for Bosch Corporate LLM Farm.

This package provides a seamless integration between Pydantic AI and Bosch's
corporate LLM Farm, offering secure configuration management and OpenAI-compatible
API access.

Usage:
    from llmfarm_pydantic import BoschFarmProvider, create_bosch_farm_provider
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    
    # Simple usage with environment variables
    provider = create_bosch_farm_provider()
    model = OpenAIChatModel('gpt-4o-mini', provider=provider)
    agent = Agent(model)
    
    # Advanced usage with config file
    provider = BoschFarmProvider(config_path='config/farm_config.yaml')
    model = OpenAIChatModel('gpt-4o-mini', provider=provider)
    agent = Agent(model)
"""

from .providers.bosch_farm import BoschFarmProvider, create_bosch_farm_provider
from .config.settings import BoschFarmConfig

__version__ = "0.1.0"
__all__ = ["BoschFarmProvider", "BoschFarmConfig", "create_bosch_farm_provider"]

from .providers.bosch_farm import BoschFarmProvider, create_bosch_farm_provider
from .config.settings import BoschFarmConfig, load_config, get_global_config

__version__ = "0.1.0"
__author__ = "Bosch LLM Farm Integration Team"

__all__ = [
    "BoschFarmProvider",
    "create_bosch_farm_provider", 
    "BoschFarmConfig",
    "load_config",
    "get_global_config",
]