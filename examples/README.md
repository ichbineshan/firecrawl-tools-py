# Firecrawl Tools Examples

This directory contains practical examples demonstrating how to use Firecrawl Tools for various web scraping and data extraction tasks.

## Available Examples

### 1. Basic Usage Examples

- **`basic_usage.py`** - Simple examples of each individual tool
- **`advanced_usage.py`** - More complex scenarios and tool combinations

### 2. ReAct Agent Integration

- **`react_agent_example.py`** - Complete example of using Firecrawl Tools with LangChain's ReAct agent

This example demonstrates how to create an intelligent agent that automatically chooses the right Firecrawl tool based on natural language queries.

**Features:**
- Automatic tool selection based on query
- Multiple example queries
- Error handling and validation
- Environment variable configuration
- Comprehensive documentation

**Requirements:**
```bash
pip install langchain langchain-openai firecrawl-tools
```

**Setup:**
```bash
export FIRECRAWL_API_KEY="your_firecrawl_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

**Usage:**
```bash
python examples/react_agent_example.py
```

### 3. Individual Tool Examples

- **`run_scrape_example.py`** - URL scraping demonstration
- **`run_search_example.py`** - Web search demonstration  
- **`run_map_example.py`** - Website mapping demonstration
- **`run_extract_example.py`** - Structured data extraction demonstration
- **`run_research_example.py`** - Deep research demonstration
- **`run_crawl_example.py`** - Website crawling and status monitoring

## Running Examples

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys:**
   ```bash
   export FIRECRAWL_API_KEY="your_firecrawl_api_key"
   ```

3. **Run any example:**
   ```bash
   python examples/react_agent_example.py
   ```

## Example Outputs

Each example demonstrates different capabilities:

- **Scraping**: Extract content from websites in various formats
- **Searching**: Find information across the web
- **Mapping**: Discover website structure and URLs
- **Extraction**: Get structured data using LLM capabilities
- **Research**: Conduct comprehensive web research
- **Crawling**: Process entire websites asynchronously
- **ReAct Agent**: Intelligent tool selection and reasoning

## Contributing

Feel free to add your own examples! Please follow the existing code style and include proper documentation. 