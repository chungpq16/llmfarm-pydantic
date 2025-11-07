"""
Simple Bosch Farm LLM Interface
A direct, easy-to-use wrapper for Bosch Corporate LLM Farm API.
"""

import os
from openai import OpenAI
from typing import Optional, List, Dict, Any


class BoschFarmLLM:
    """
    Simple interface to Bosch Corporate LLM Farm.
    
    Based on the llmfarminf concept - direct OpenAI client wrapper
    with Bosch Farm authentication and configuration.
    """
    
    def __init__(
        self, 
        model: str = "askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18",
        farm_api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        api_version: str = "2024-08-01-preview"
    ) -> None:
        """
        Initialize Bosch Farm LLM client.
        
        Args:
            model: The Azure deployment name (default: askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18)
            farm_api_key: Your genaiplatform-farm-subscription-key (or set BOSCH_FARM_API_KEY env var)
            base_url: Base URL for deployment (or set BOSCH_FARM_BASE_URL env var)
            api_version: API version for requests
        """
        # Get configuration from environment if not provided
        self.farm_api_key = farm_api_key or os.getenv("BOSCH_FARM_API_KEY")
        configured_base_url = base_url or os.getenv(
            "BOSCH_FARM_BASE_URL",
            "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18"
        )
        self.model = model
        self.api_version = api_version
        
        # Validate required configuration
        if not self.farm_api_key:
            raise ValueError(
                "BOSCH_FARM_API_KEY is required. "
                "Set it as an environment variable or pass farm_api_key parameter."
            )
        
        # Extract deployment name and construct proper base URL for Azure OpenAI
        self.deployment_name = self._extract_deployment_name(configured_base_url)
        self.base_url = self._construct_base_url(configured_base_url)
        
        # Create OpenAI client with Bosch Farm configuration
        self.client = OpenAI(
            api_key="dummy",  # Required by OpenAI client, but we use custom headers
            base_url=self.base_url,
            default_headers={
                "genaiplatform-farm-subscription-key": self.farm_api_key
            }
        )
    
    def _gen_message(self, sysprompt: str, userprompt: str) -> List[Dict[str, str]]:
        """Generate message list for chat completion."""
        return [
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": userprompt}
        ]
    
    def _completion(self, usertext: str, sysprompt: str = "You are a helpful assistant") -> str:
        """
        Get completion from Bosch Farm LLM.
        
        Args:
            usertext: User's prompt/question
            sysprompt: System prompt (default: "You are a helpful assistant")
        
        Returns:
            The LLM's response text
        """
        messages = self._gen_message(sysprompt, usertext)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_query={"api-version": self.api_version}
        )
        
        return response.choices[0].message.content
    
    def chat(self, prompt: str, system_prompt: str = "You are a helpful assistant") -> str:
        """
        Simple chat interface.
        
        Args:
            prompt: Your question or prompt
            system_prompt: System instructions for the LLM
        
        Returns:
            The LLM's response
        """
        return self._completion(prompt, system_prompt)
    
    def ask(self, question: str) -> str:
        """
        Ask a question (convenience method).
        
        Args:
            question: Your question
        
        Returns:
            The LLM's answer
        """
        return self._completion(question, "You are a helpful assistant")
    
    def _extract_deployment_name(self, url: str) -> str:
        """
        Extract deployment name from Azure OpenAI URL.
        
        Args:
            url: Full deployment URL or API root URL
            
        Returns:
            The deployment name
        """
        try:
            if "/deployments/" in url:
                # Extract from URL like: https://aoai-farm.bosch-temp.com/api/openai/deployments/DEPLOYMENT_NAME/...
                parts = url.split("/deployments/", 1)[1]
                deployment_name = parts.split("/", 1)[0]
                return deployment_name
        except (IndexError, ValueError):
            pass
        
        # Fallback to model name if URL parsing fails
        return self.model
    
    def _construct_base_url(self, configured_url: str) -> str:
        """
        Construct the correct base URL for Azure OpenAI.
        
        The OpenAI client will append /chat/completions, so we need to provide
        the full path up to the deployment: /deployments/{deployment}
        
        Args:
            configured_url: The configured base URL (could be API root or full deployment URL)
            
        Returns:
            Proper base URL for the OpenAI client
        """
        try:
            if "/deployments/" in configured_url:
                # URL already contains deployment path
                # Extract everything up to and including the deployment name
                before_deployments, after_deployments = configured_url.split("/deployments/", 1)
                deployment_name = after_deployments.split("/", 1)[0]
                
                # Construct: https://aoai-farm.bosch-temp.com/api/openai/deployments/DEPLOYMENT_NAME
                base_url = f"{before_deployments}/deployments/{deployment_name}"
                return base_url.rstrip('/')
            else:
                # URL is just the API root, append deployment path
                api_root = configured_url.rstrip('/')
                return f"{api_root}/deployments/{self.deployment_name}"
        except Exception:
            # Fallback: assume the URL is correct as-is
            return configured_url.rstrip('/')


# Alias for the original naming convention
llmfarminf = BoschFarmLLM


def main():
    """Example usage of the Bosch Farm LLM client."""
    
    # Check if API key is set
    if not os.getenv("BOSCH_FARM_API_KEY"):
        print("❌ Please set BOSCH_FARM_API_KEY environment variable")
        print("   export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'")
        return
    
    try:
        # Create client
        print("🚀 Initializing Bosch Farm LLM client...")
        llm = BoschFarmLLM()
        
        print(f"✅ Client created successfully")
        print(f"   Model: {llm.model}")
        print(f"   Base URL: {llm.base_url}")
        print(f"   API Version: {llm.api_version}")
        
        # Test the LLM
        print("\n🤖 Testing LLM...")
        prompt = "Tell me about Bosch Group"
        print(f"Question: {prompt}")
        
        response = llm._completion(prompt, "You are a helpful assistant")
        print(f"\n📝 Response:\n{response}")
        
        # Test convenience methods
        print("\n🔄 Testing convenience methods...")
        
        answer = llm.ask("What is artificial intelligence in one sentence?")
        print(f"Answer: {answer}")
        
        chat_response = llm.chat(
            "How can AI help manufacturing?",
            "You are an expert in industrial AI applications"
        )
        print(f"Chat response: {chat_response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()