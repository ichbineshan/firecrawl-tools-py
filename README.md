# Firecrawl Tools

A comprehensive collection of async tools for web scraping, searching, and data extraction using the Firecrawl API. Built with LangChain for seamless integration with AI applications.

## Features

- **URL Scraping**: Extract content from single URLs with multiple format options
- **Web Search**: Search the web and optionally scrape search results
- **Website Mapping**: Discover all indexed URLs on a website
- **Structured Data Extraction**: Extract specific information using LLM capabilities
- **Deep Research**: Conduct comprehensive web research with intelligent crawling
- **Website Crawling**: Asynchronous crawling of entire websites
- **Crawl Status Monitoring**: Track and manage crawl jobs

## Installation

```bash
pip install firecrawl-tools
```

## Quick Start

```python
import asyncio
from firecrawl_tools import FirecrawlTools

# Initialize with your API key
tools = FirecrawlTools(api_key="your_firecrawl_api_key")

# Get individual tools
scrape_tool = await tools.get_scrape_tool()
search_tool = await tools.get_search_tool()

# Use the tools
content = await scrape_tool.ainvoke({
    "url": "https://example.com",
    "formats": ["markdown"],
    "only_main_content": True
})
```

## Available Tools

### 1. URL Scraping Tool
Extract content from a single URL with advanced options.

```python
scrape_tool = await tools.get_scrape_tool()
result = await scrape_tool.ainvoke({
    "url": "https://example.com",
    "formats": ["markdown", "html"],
    "only_main_content": True,
    "wait_for": 2000,
    "mobile": False
})
```

### 2. Web Search Tool
Search the web and optionally extract content from results.

```python
search_tool = await tools.get_search_tool()
results = await search_tool.ainvoke({
    "query": "Python web scraping",
    "limit": 5,
    "scrape_options": {
        "formats": ["markdown"],
        "onlyMainContent": True
    }
})
```

### 3. Website Mapping Tool
Discover all indexed URLs on a website.

```python
map_tool = await tools.get_map_tool()
urls = await map_tool.ainvoke({
    "url": "https://example.com",
    "include_subdomains": True,
    "limit": 100
})
```

### 4. Structured Data Extraction Tool
Extract specific information using LLM capabilities.

```python
extract_tool = await tools.get_extract_tool()
data = await extract_tool.ainvoke({
    "urls": ["https://example.com"],
    "prompt": "Extract all product names and prices",
    "schema": {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "string"}
                    }
                }
            }
        }
    }
})
```

### 5. Deep Research Tool
Conduct comprehensive web research.

```python
research_tool = await tools.get_research_tool()
analysis = await research_tool.ainvoke({
    "query": "Latest developments in AI",
    "max_depth": 3,
    "time_limit": 120,
    "max_urls": 50
})
```

### 6. Website Crawling Tool
Crawl entire websites asynchronously.

```python
crawl_tool = await tools.get_crawl_tool()
job_id = await crawl_tool.ainvoke({
    "url": "https://example.com",
    "max_depth": 2,
    "limit": 100,
    "allow_external_links": False
})
```

### 7. Crawl Status Tool
Check the status of crawl jobs.

```python
status_tool = await tools.get_status_tool()
status = await status_tool.ainvoke({
    "crawl_id": "your_crawl_job_id"
})
```

## ReAct Agent Integration

Firecrawl Tools work seamlessly with LangChain's ReAct agents, allowing you to build intelligent applications that automatically choose the right tool for each task.

### Basic ReAct Agent Setup

```python
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from firecrawl_tools import FirecrawlTools

async def create_react_agent():
    # Initialize Firecrawl tools
    tools = FirecrawlTools(api_key="your_firecrawl_api_key")
    tools_dict = await tools.get_tools_dict()
    tool_list = list(tools_dict.values())
    
    # Initialize OpenAI LLM
    llm = ChatOpenAI(
        openai_api_key="your_openai_api_key",
        temperature=0,
        model="gpt-4o-mini"
    )
    
    # Create ReAct agent
    agent = initialize_agent(
        tool_list,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
    
    return agent

# Use the agent
agent = await create_react_agent()
result = await agent.ainvoke(
    "Find the main topic of https://example.com and summarize it in 2 sentences."
)
```

### Example Queries

The ReAct agent can handle various natural language queries:

- **"What are the latest news headlines on cricbuzz.com?"**
- **"Extract all product names and prices from https://example.com"**
- **"Search for information about Python web scraping and provide a summary."**
- **"Map all URLs on https://example.com and list the top 5 pages."**

The agent automatically chooses the appropriate Firecrawl tool (scrape, search, extract, map, etc.) based on the query.

### Complete Example

See [examples/react_agent_example.py](examples/react_agent_example.py) for a complete working example with multiple queries and error handling.

## Configuration

You can configure the tools using environment variables or by passing configuration directly:

```python
# Using environment variable
export FIRECRAWL_API_KEY="your_api_key"

# Or pass configuration directly
tools = FirecrawlTools(api_key="your_api_key")
```

## Error Handling

All tools include comprehensive error handling and will raise `ToolException` with descriptive error messages:

```python
from langchain_core.tools import ToolException

try:
    result = await scrape_tool.ainvoke({"url": "https://example.com"})
except ToolException as e:
    print(f"Error: {e}")
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://github.com/ichbineshan/firecrawl-tools-py](https://github.com/ichbineshan/firecrawl-tools-py)
- Issues: [https://github.com/ichbineshan/firecrawl-tools-py/issues](https://github.com/ichbineshan/firecrawl-tools-py/issues)
- Discussions: [https://github.com/ichbineshan/firecrawl-tools-py/discussions](https://github.com/ichbineshan/firecrawl-tools-py/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.