"""
Tests for the main FirecrawlTools class.
"""

import pytest
from unittest.mock import AsyncMock, patch

from firecrawl_tools.core import FirecrawlTools
from firecrawl_tools.exceptions import ConfigurationError


class TestFirecrawlTools:
    """Test the FirecrawlTools class."""
    
    @pytest.fixture
    def tools(self):
        """Create a FirecrawlTools instance for testing."""
        return FirecrawlTools(api_key="test_key")
    
    def test_initialization_with_api_key(self):
        """Test initialization with API key."""
        tools = FirecrawlTools(api_key="test_key")
        assert tools.config.api_key == "test_key"
    
    def test_initialization_with_config_dict(self):
        """Test initialization with config dictionary."""
        config_dict = {"firecrawl_api_key": "dict_key"}
        tools = FirecrawlTools(config_dict=config_dict)
        assert tools.config.api_key == "dict_key"
    
    def test_initialization_without_config(self):
        """Test initialization without config (should use environment)."""
        with patch('firecrawl_tools.config.get_config') as mock_get_config:
            mock_get_config.return_value.api_key = "env_key"
            tools = FirecrawlTools()
            assert tools.config.api_key == "env_key"
    
    @pytest.mark.asyncio
    async def test_get_scrape_tool(self, tools):
        """Test getting the scrape tool."""
        tool = await tools.get_scrape_tool()
        assert tool is not None
        assert "scrape" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_search_tool(self, tools):
        """Test getting the search tool."""
        tool = await tools.get_search_tool()
        assert tool is not None
        assert "search" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_map_tool(self, tools):
        """Test getting the map tool."""
        tool = await tools.get_map_tool()
        assert tool is not None
        assert "map" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_extract_tool(self, tools):
        """Test getting the extract tool."""
        tool = await tools.get_extract_tool()
        assert tool is not None
        assert "extract" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_research_tool(self, tools):
        """Test getting the research tool."""
        tool = await tools.get_research_tool()
        assert tool is not None
        assert "research" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_crawl_tool(self, tools):
        """Test getting the crawl tool."""
        tool = await tools.get_crawl_tool()
        assert tool is not None
        assert "crawl" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_status_tool(self, tools):
        """Test getting the status tool."""
        tool = await tools.get_status_tool()
        assert tool is not None
        assert "status" in tools._tools
    
    @pytest.mark.asyncio
    async def test_get_all_tools(self, tools):
        """Test getting all tools."""
        all_tools = await tools.get_all_tools()
        assert len(all_tools) == 7  # All 7 tools
        assert all(tool is not None for tool in all_tools)
    
    @pytest.mark.asyncio
    async def test_get_tools_dict(self, tools):
        """Test getting tools as dictionary."""
        tools_dict = await tools.get_tools_dict()
        expected_keys = [
            "scrape_url",
            "search_web",
            "map_website", 
            "extract_structured",
            "deep_research",
            "crawl_website",
            "check_crawl_status"
        ]
        assert set(tools_dict.keys()) == set(expected_keys)
        assert all(tool is not None for tool in tools_dict.values())
    
    def test_get_available_tools(self, tools):
        """Test getting available tool names."""
        available_tools = tools.get_available_tools()
        expected_tools = [
            "scrape_url",
            "search_web",
            "map_website",
            "extract_structured", 
            "deep_research",
            "crawl_website",
            "check_crawl_status"
        ]
        assert available_tools == expected_tools
    
    @pytest.mark.asyncio
    async def test_get_tool_by_name_valid(self, tools):
        """Test getting a tool by valid name."""
        tool = await tools.get_tool_by_name("scrape_url")
        assert tool is not None
    
    @pytest.mark.asyncio
    async def test_get_tool_by_name_invalid(self, tools):
        """Test getting a tool by invalid name."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await tools.get_tool_by_name("invalid_tool")
    
    @pytest.mark.asyncio
    async def test_tool_caching(self, tools):
        """Test that tools are cached after first creation."""
        # Get the same tool twice
        tool1 = await tools.get_scrape_tool()
        tool2 = await tools.get_scrape_tool()
        
        # Should be the same object (cached)
        assert tool1 is tool2
        assert len(tools._tools) == 1  # Only one tool cached
    
    @pytest.mark.asyncio
    async def test_multiple_tools_caching(self, tools):
        """Test that multiple tools are cached independently."""
        # Get different tools
        scrape_tool = await tools.get_scrape_tool()
        search_tool = await tools.get_search_tool()
        
        # Should be different objects
        assert scrape_tool is not search_tool
        assert len(tools._tools) == 2  # Two tools cached
        assert "scrape" in tools._tools
        assert "search" in tools._tools 