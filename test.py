from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

class LLMFarmPydantic:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        
        # Create AsyncOpenAI client with the full URL including api-version
        client = AsyncOpenAI(
            api_key="dummy",
            base_url="https://llm-test.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/chat/completions?api-version=2024-08-01-preview",
            default_headers={"genaiplatform-farm-subscription-key": "my-farm-key"}
        )
        
        # Create provider with the custom client
        provider = OpenAIProvider(openai_client=client)
        
        # Create the model
        self.model_instance = OpenAIChatModel(self.model, provider=provider)
        
        # Create the agent
        self.agent = Agent(self.model_instance)
    
    def completion(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Generate completion using PydanticAI Agent
        """
        # Use system prompt if provided
        if sysprompt != "You are a helpful assistant":
            # Create agent with custom system prompt
            agent_with_prompt = Agent(
                self.model_instance, 
                system_prompt=sysprompt
            )
            result = agent_with_prompt.run_sync(usertext)
        else:
            result = self.agent.run_sync(usertext)
        
        return result.output
    
    async def completion_async(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Async version of completion
        """
        if sysprompt != "You are a helpful assistant":
            agent_with_prompt = Agent(
                self.model_instance, 
                system_prompt=sysprompt
            )
            result = await agent_with_prompt.run(usertext)
        else:
            result = await self.agent.run(usertext)
        
        return result.output

if __name__ == "__main__":
    # Create instance
    llm_farm = LLMFarmPydantic()
    
    # Use it the same way as before
    prompt = "Tell me about Bosch group"
    response = llm_farm.completion(prompt, "You are a helpful assistant")
    print(response)
    
    # Or use async version
    import asyncio
    
    async def test_async():
        response = await llm_farm.completion_async(prompt, "You are a helpful assistant")
        print(f"Async response: {response}")
    
    asyncio.run(test_async())