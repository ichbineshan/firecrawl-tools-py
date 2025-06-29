"""
Basic usage example for Firecrawl Tools.

This example demonstrates how to use the main FirecrawlTools class
to perform common web scraping and data extraction tasks.
"""

import asyncio
import os
from firecrawl_tools import FirecrawlTools


async def main():
    """Demonstrate basic usage of Firecrawl Tools."""
    
    # Initialize tools with API key
    # You can set FIRECRAWL_API_KEY environment variable or pass it directly
    api_key = os.getenv("FIRECRAWL_API_KEY", "your_api_key_here")
    tools = FirecrawlTools(api_key=api_key)
    
    print("🚀 Firecrawl Tools Basic Usage Example\n")
    
    # Example 1: Scrape a single URL
    print("1. Scraping a URL...")
    try:
        scrape_tool = await tools.get_scrape_tool()
        result = await scrape_tool.invoke({
            "url": "https://example.com",
            "formats": ["markdown"],
            "only_main_content": True
        })
        print(f"✅ Scraped content length: {len(result)} characters")
        print(f"📄 First 200 characters: {result[:200]}...\n")
    except Exception as e:
        print(f"❌ Scraping failed: {e}\n")
    
    # Example 2: Search the web
    print("2. Searching the web...")
    try:
        search_tool = await tools.get_search_tool()
        results = await search_tool.invoke({
            "query": "Python web scraping",
            "limit": 3,
            "scrape_options": {
                "formats": ["markdown"],
                "onlyMainContent": True
            }
        })
        print(f"✅ Found search results: {len(results.split('Result')) - 1} results")
        print(f"📄 First 200 characters: {results[:200]}...\n")
    except Exception as e:
        print(f"❌ Search failed: {e}\n")
    
    # Example 3: Map a website
    print("3. Mapping a website...")
    try:
        map_tool = await tools.get_map_tool()
        urls = await map_tool.invoke({
            "url": "https://example.com",
            "limit": 10
        })
        print(f"✅ Found URLs: {urls.count('http')} URLs")
        print(f"📄 First 200 characters: {urls[:200]}...\n")
    except Exception as e:
        print(f"❌ Mapping failed: {e}\n")
    
    # Example 4: Extract structured data
    print("4. Extracting structured data...")
    try:
        extract_tool = await tools.get_extract_tool()
        data = await extract_tool.invoke({
            "urls": ["https://example.com"],
            "prompt": "Extract the main heading and any links found on this page",
            "schema": {
                "type": "object",
                "properties": {
                    "main_heading": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        })
        print(f"✅ Extracted structured data: {len(data)} characters")
        print(f"📄 Data: {data[:200]}...\n")
    except Exception as e:
        print(f"❌ Extraction failed: {e}\n")
    
    # Example 5: Get all tools at once
    print("5. Getting all available tools...")
    try:
        all_tools = await tools.get_all_tools()
        print(f"✅ Available tools: {len(all_tools)} tools")
        for i, tool in enumerate(all_tools, 1):
            print(f"   {i}. {tool.name}")
        print()
    except Exception as e:
        print(f"❌ Failed to get tools: {e}\n")
    
    print("🎉 Basic usage example completed!")


if __name__ == "__main__":
    asyncio.run(main()) 