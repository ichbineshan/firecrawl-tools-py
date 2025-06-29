"""
ReAct Agent Example with Firecrawl Tools

This example demonstrates how to use Firecrawl Tools with LangChain's ReAct agent
to intelligently analyze websites and answer questions using natural language.

The agent automatically chooses which Firecrawl tool to use based on the query,
making it easy to scrape, search, extract data, and more without manual tool selection.

Requirements:
    pip install langchain langchain-openai firecrawl-tools
"""

import asyncio
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from firecrawl_tools import FirecrawlTools


async def create_react_agent(
    firecrawl_api_key: str,
    openai_api_key: str,
    temperature: float = 0,
    max_iterations: int = 5
):
    """
    Create a ReAct agent with Firecrawl tools.
    
    Args:
        firecrawl_api_key: Your Firecrawl API key
        openai_api_key: Your OpenAI API key
        temperature: LLM temperature (0 for deterministic)
        max_iterations: Maximum agent iterations
    
    Returns:
        Configured ReAct agent
    """
    # Initialize Firecrawl tools
    tools = FirecrawlTools(api_key=firecrawl_api_key)
    tools_dict = await tools.get_tools_dict()
    tool_list = list(tools_dict.values())
    
    # Initialize OpenAI LLM
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        temperature=temperature,
        model="gpt-4o-mini"  # You can change this to other models
    )
    
    # Create ReAct agent
    agent = initialize_agent(
        tool_list,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=max_iterations,
        handle_parsing_errors=True,
    )
    
    return agent


async def analyze_website(agent, query: str):
    """
    Analyze a website using the ReAct agent.
    
    Args:
        agent: The ReAct agent
        query: Natural language query about the website
    
    Returns:
        Agent's analysis and response
    """
    try:
        result = await agent.ainvoke(query)
        return result
    except Exception as e:
        return f"Error analyzing website: {str(e)}"


async def main():
    """Main function demonstrating ReAct agent usage."""
    
    # Get API keys from environment variables
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not firecrawl_api_key:
        print("❌ FIRECRAWL_API_KEY environment variable not set")
        print("Please set it with: export FIRECRAWL_API_KEY='your_api_key'")
        return
    
    if not openai_api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your_api_key'")
        return
    
    print("🚀 Creating ReAct agent with Firecrawl tools...")
    
    try:
        # Create the agent
        agent = await create_react_agent(
            firecrawl_api_key=firecrawl_api_key,
            openai_api_key=openai_api_key
        )
        
        print("✅ Agent created successfully!")
        print("\n" + "="*60)
        
        # Example queries to demonstrate different capabilities
        example_queries = [
            "Find the main topic of https://example.com and summarize it in 2 sentences.",
            "What are the latest news headlines on cricbuzz.com?",
            "Extract all product names and prices from https://example.com",
            "Search for information about Python web scraping and provide a summary.",
            "Map all URLs on https://example.com and list the top 5 pages."
        ]
        
        for i, query in enumerate(example_queries, 1):
            print(f"\n🔍 Example {i}: {query}")
            print("-" * 60)
            
            result = await analyze_website(agent, query)
            
            print("\n📝 Agent Response:")
            print(result.get('output', result))
            print("\n" + "="*60)
            
            # Add a small delay between queries
            if i < len(example_queries):
                print("⏳ Waiting 2 seconds before next query...")
                await asyncio.sleep(2)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Make sure you have the required dependencies installed:")
        print("   pip install langchain langchain-openai firecrawl-tools")


if __name__ == "__main__":
    asyncio.run(main()) 