"""
Bosch Farm Provider for Pydantic AI

This package provides two interfaces:
1. Simple direct interface (BoschFarmLLM) - easy to use, no Pydantic AI required
2. Pydantic AI integration (BoschFarmProvider) - for advanced AI agent workflows

Simple Usage:
    from llmfarm_pydantic import BoschFarmLLM
    
    # Direct usage (like llmfarminf)
    llm = BoschFarmLLM()
    response = llm.ask("Tell me about Bosch Group")
    
Pydantic AI Usage:
    from llmfarm_pydantic import create_bosch_farm_provider
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    
    # Advanced Pydantic AI integration
    provider = create_bosch_farm_provider()
    model = OpenAIChatModel(provider.deployment_name, provider=provider)
    agent = Agent(model)
"""

from .providers.bosch_farm import BoschFarmProvider, create_bosch_farm_provider
from .config.settings import BoschFarmConfig, load_config, get_global_config
from .bosch_farm_simple import BoschFarmLLM, llmfarminf

__version__ = "0.1.1"
__author__ = "Bosch LLM Farm Integration Team"

__all__ = [
    # Pydantic AI integration
    "BoschFarmProvider",
    "create_bosch_farm_provider", 
    "BoschFarmConfig",
    "load_config",
    "get_global_config",
    
    # Simple direct interface
    "BoschFarmLLM",
    "llmfarminf",  # Alias for backward compatibility
]