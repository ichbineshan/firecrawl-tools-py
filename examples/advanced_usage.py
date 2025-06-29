"""
Advanced usage example for Firecrawl Tools.

This example demonstrates more complex scenarios including:
- Error handling and retries
- Custom configuration
- Batch operations
- Integration with LangChain agents
"""

import asyncio
import json
import os
from typing import List, Dict, Any
from firecrawl_tools import FirecrawlTools, FirecrawlToolsError, ConfigurationError


async def scrape_multiple_urls(tools: FirecrawlTools, urls: List[str]) -> Dict[str, Any]:
    """Scrape multiple URLs with error handling."""
    results = {}
    scrape_tool = await tools.get_scrape_tool()
    
    for url in urls:
        try:
            print(f"Scraping {url}...")
            result = await scrape_tool.invoke({
                "url": url,
                "formats": ["markdown", "links"],
                "only_main_content": True,
                "wait_for": 2000
            })
            results[url] = {"success": True, "data": result}
            print(f"✅ Success: {len(result)} characters")
        except Exception as e:
            results[url] = {"success": False, "error": str(e)}
            print(f"❌ Failed: {e}")
    
    return results


async def research_topic(tools: FirecrawlTools, topic: str) -> str:
    """Conduct deep research on a topic."""
    print(f"🔍 Researching: {topic}")
    
    research_tool = await tools.get_research_tool()
    result = await research_tool.invoke({
        "query": topic,
        "max_depth": 2,
        "time_limit": 60,
        "max_urls": 20
    })
    
    return result


async def extract_product_data(tools: FirecrawlTools, urls: List[str]) -> List[Dict]:
    """Extract product information from e-commerce pages."""
    extract_tool = await tools.get_extract_tool()
    
    schema = {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "string"},
                        "description": {"type": "string"},
                        "availability": {"type": "string"}
                    }
                }
            }
        }
    }
    
    prompt = """
    Extract all product information from this page. Look for:
    - Product names
    - Prices (including currency)
    - Product descriptions
    - Availability status
    
    Return the data in a structured format.
    """
    
    result = await extract_tool.invoke({
        "urls": urls,
        "prompt": prompt,
        "schema": schema,
        "allow_external_links": False
    })
    
    return json.loads(result)


async def crawl_and_monitor(tools: FirecrawlTools, url: str) -> Dict[str, Any]:
    """Start a crawl and monitor its progress."""
    print(f"🕷️ Starting crawl for: {url}")
    
    # Start the crawl
    crawl_tool = await tools.get_crawl_tool()
    crawl_result = await crawl_tool.invoke({
        "url": url,
        "max_depth": 2,
        "limit": 50,
        "allow_external_links": False,
        "deduplicate_similar_urls": True
    })
    
    # Extract crawl ID from result
    # Assuming the result contains the crawl ID
    crawl_id = "your_crawl_id"  # You'd extract this from crawl_result
    
    # Monitor progress
    status_tool = await tools.get_status_tool()
    max_checks = 10
    check_interval = 30  # seconds
    
    for i in range(max_checks):
        await asyncio.sleep(check_interval)
        
        try:
            status = await status_tool.invoke({"crawl_id": crawl_id})
            print(f"📊 Check {i+1}: {status}")
            
            # Check if completed
            if "completed" in status and "total" in status:
                completed = int(status.split("completed: ")[1].split("/")[0])
                total = int(status.split("total: ")[1].split("\n")[0])
                if completed >= total:
                    print("✅ Crawl completed!")
                    break
        except Exception as e:
            print(f"❌ Status check failed: {e}")
    
    return {"crawl_id": crawl_id, "status": "monitored"}


async def search_and_analyze(tools: FirecrawlTools, query: str) -> Dict[str, Any]:
    """Search for information and analyze the results."""
    print(f"🔎 Searching for: {query}")
    
    search_tool = await tools.get_search_tool()
    results = await search_tool.invoke({
        "query": query,
        "limit": 5,
        "scrape_options": {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    })
    
    # Analyze the results
    analysis = {
        "query": query,
        "results_count": len(results.split("Result")) - 1,
        "total_length": len(results),
        "sources": []
    }
    
    # Extract URLs from results
    lines = results.split("\n")
    for line in lines:
        if line.startswith("URL: "):
            analysis["sources"].append(line.replace("URL: ", ""))
    
    return analysis


async def main():
    """Demonstrate advanced usage scenarios."""
    
    # Custom configuration
    config = {
        "firecrawl_api_key": os.getenv("FIRECRAWL_API_KEY", "your_api_key_here"),
        "timeout": 60,
        "max_retries": 3
    }
    
    tools = FirecrawlTools(config_dict=config)
    
    print("🚀 Firecrawl Tools Advanced Usage Example\n")
    
    # Scenario 1: Batch URL scraping with error handling
    print("1. Batch URL Scraping")
    urls_to_scrape = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://httpbin.org/json"
    ]
    
    batch_results = await scrape_multiple_urls(tools, urls_to_scrape)
    successful_scrapes = sum(1 for result in batch_results.values() if result["success"])
    print(f"📊 Batch scraping completed: {successful_scrapes}/{len(urls_to_scrape)} successful\n")
    
    # Scenario 2: Deep research
    print("2. Deep Research")
    try:
        research_result = await research_topic(tools, "Latest developments in AI")
        print(f"📄 Research completed: {len(research_result)} characters")
        print(f"🔍 First 300 characters: {research_result[:300]}...\n")
    except Exception as e:
        print(f"❌ Research failed: {e}\n")
    
    # Scenario 3: Product data extraction
    print("3. Product Data Extraction")
    try:
        product_urls = ["https://example.com/products"]
        product_data = await extract_product_data(tools, product_urls)
        print(f"📦 Extracted product data: {json.dumps(product_data, indent=2)[:200]}...\n")
    except Exception as e:
        print(f"❌ Product extraction failed: {e}\n")
    
    # Scenario 4: Search and analyze
    print("4. Search and Analyze")
    try:
        search_analysis = await search_and_analyze(tools, "Python async programming")
        print(f"📊 Search analysis: {search_analysis}")
        print(f"🔗 Found {len(search_analysis['sources'])} sources\n")
    except Exception as e:
        print(f"❌ Search analysis failed: {e}\n")
    
    # Scenario 5: Error handling demonstration
    print("5. Error Handling Demonstration")
    try:
        # Try to use tools without API key
        invalid_tools = FirecrawlTools(api_key="invalid_key")
        scrape_tool = await invalid_tools.get_scrape_tool()
        await scrape_tool.invoke({"url": "https://example.com"})
    except (FirecrawlToolsError, ConfigurationError) as e:
        print(f"✅ Properly caught error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n🎉 Advanced usage example completed!")


if __name__ == "__main__":
    asyncio.run(main()) 