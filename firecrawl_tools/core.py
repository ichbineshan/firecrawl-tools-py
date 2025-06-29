"""
Main FirecrawlTools class that provides a unified interface to all tools.
"""

from typing import Optional, Dict, List
from langchain_core.tools import BaseTool

from .config import get_config
from .exceptions import ConfigurationError
from .tools import (
    ScrapeUrlTool,
    SearchWebTool,
    MapUrlTool,
    ExtractStructuredTool,
    DeepResearchTool,
    CrawlUrlTool,
    CheckCrawlStatusTool,
)


class FirecrawlTools:
    """
    Main class for Firecrawl Tools that provides access to all available tools.
    
    This class serves as a unified interface to all Firecrawl tools, making it easy
    to initialize and use multiple tools with the same configuration.
    """
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        """
        Initialize FirecrawlTools with configuration.
        
        Args:
            api_key: Direct API key string
            config_dict: Configuration dictionary containing firecrawl_api_key and other settings
        """
        self.config = get_config(api_key, config_dict)
        self._tools: Dict[str, BaseTool] = {}
    
    async def get_scrape_tool(self) -> BaseTool:
        """Get the URL scraping tool."""
        if "scrape" not in self._tools:
            tool_instance = ScrapeUrlTool(api_key=self.config.api_key)
            self._tools["scrape"] = tool_instance.tool
        return self._tools["scrape"]
    
    async def get_search_tool(self) -> BaseTool:
        """Get the web search tool."""
        if "search" not in self._tools:
            tool_instance = SearchWebTool(api_key=self.config.api_key)
            self._tools["search"] = tool_instance.tool
        return self._tools["search"]
    
    async def get_map_tool(self) -> BaseTool:
        """Get the website mapping tool."""
        if "map" not in self._tools:
            tool_instance = MapUrlTool(api_key=self.config.api_key)
            self._tools["map"] = tool_instance.tool
        return self._tools["map"]
    
    async def get_extract_tool(self) -> BaseTool:
        """Get the structured data extraction tool."""
        if "extract" not in self._tools:
            tool_instance = ExtractStructuredTool(api_key=self.config.api_key)
            self._tools["extract"] = tool_instance.tool
        return self._tools["extract"]
    
    async def get_research_tool(self) -> BaseTool:
        """Get the deep research tool."""
        if "research" not in self._tools:
            tool_instance = DeepResearchTool(api_key=self.config.api_key)
            self._tools["research"] = tool_instance.tool
        return self._tools["research"]
    
    async def get_crawl_tool(self) -> BaseTool:
        """Get the website crawling tool."""
        if "crawl" not in self._tools:
            tool_instance = CrawlUrlTool(api_key=self.config.api_key)
            self._tools["crawl"] = tool_instance.tool
        return self._tools["crawl"]
    
    async def get_status_tool(self) -> BaseTool:
        """Get the crawl status checking tool."""
        if "status" not in self._tools:
            tool_instance = CheckCrawlStatusTool(api_key=self.config.api_key)
            self._tools["status"] = tool_instance.tool
        return self._tools["status"]
    
    async def get_all_tools(self) -> List[BaseTool]:
        """Get all available tools as a list."""
        tools = [
            await self.get_scrape_tool(),
            await self.get_search_tool(),
            await self.get_map_tool(),
            await self.get_extract_tool(),
            await self.get_research_tool(),
            await self.get_crawl_tool(),
            await self.get_status_tool(),
        ]
        return tools
    
    async def get_tools_dict(self) -> Dict[str, BaseTool]:
        """Get all tools as a dictionary with descriptive names."""
        return {
            "scrape_url": await self.get_scrape_tool(),
            "search_web": await self.get_search_tool(),
            "map_website": await self.get_map_tool(),
            "extract_structured": await self.get_extract_tool(),
            "deep_research": await self.get_research_tool(),
            "crawl_website": await self.get_crawl_tool(),
            "check_crawl_status": await self.get_status_tool(),
        }
    
    def get_available_tools(self) -> List[str]:
        """Get a list of available tool names."""
        return [
            "scrape_url",
            "search_web", 
            "map_website",
            "extract_structured",
            "deep_research",
            "crawl_website",
            "check_crawl_status",
        ]
    
    async def get_tool_by_name(self, tool_name: str) -> BaseTool:
        """
        Get a specific tool by name.
        
        Args:
            tool_name: Name of the tool to retrieve
            
        Returns:
            The requested tool
            
        Raises:
            ValueError: If the tool name is not recognized
        """
        tool_mapping = {
            "scrape_url": self.get_scrape_tool,
            "search_web": self.get_search_tool,
            "map_website": self.get_map_tool,
            "extract_structured": self.get_extract_tool,
            "deep_research": self.get_research_tool,
            "crawl_website": self.get_crawl_tool,
            "check_crawl_status": self.get_status_tool,
        }
        
        if tool_name not in tool_mapping:
            available = ", ".join(tool_mapping.keys())
            raise ValueError(f"Unknown tool '{tool_name}'. Available tools: {available}")
        
        return await tool_mapping[tool_name]() 