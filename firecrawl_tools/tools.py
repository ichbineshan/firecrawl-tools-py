"""
Individual tool classes for Firecrawl operations.
"""

import json
from typing import Dict, List, Optional, Any
from langchain_core.tools import tool, ToolException
from firecrawl import AsyncFirecrawlApp

from .config import get_config
from .exceptions import FirecrawlToolsError, ConfigurationError


class BaseFirecrawlTool:
    """Base class for all Firecrawl tools."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        """Initialize the tool with configuration."""
        self.config = get_config(api_key, config_dict)
        self._client: Optional[AsyncFirecrawlApp] = None
    
    @property
    def client(self) -> AsyncFirecrawlApp:
        """Get or create the Firecrawl client."""
        if self._client is None:
            self._client = AsyncFirecrawlApp(api_key=self.config.api_key)
        return self._client


class ScrapeUrlTool(BaseFirecrawlTool):
    """Tool for scraping content from a single URL."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def scrape_url_tool(
            url: str,
            formats: List[str] = None,
            only_main_content: bool = True,
            wait_for: int = None,
            timeout: int = None,
            mobile: bool = False
        ) -> str:
            """
            Scrape content from a single URL with advanced options using Firecrawl.
            
            Best for: Single page content extraction, when you know exactly which page contains the information.
            Not recommended for: Multiple pages (use batch_scrape), unknown page (use search), structured data (use extract).
            
            Args:
                url: The URL to scrape
                formats: Content formats to extract. Defaults to ['markdown'].
                    Options: ['markdown', 'html', 'rawHtml', 'screenshot', 'links', 'screenshot@fullPage', 'extract']
                only_main_content: Extract only the main content, filtering out navigation, footers, etc.
                wait_for: Time in milliseconds to wait for dynamic content to load
                timeout: Maximum time in milliseconds to wait for the page to load
                mobile: Use mobile viewport
            
            Returns:
                The scraped content in the requested format(s)
            
            Raises:
                ToolException: If there's an error during scraping
            """
            try:
                if formats is None:
                    formats = ['markdown']
                
                response = await self.client.scrape_url(
                    url=url,
                    formats=formats,
                    only_main_content=only_main_content,
                    wait_for=wait_for,
                    timeout=timeout,
                    mobile=mobile
                )
                
                if not response.success:
                    raise ToolException(f"Scraping failed: {response.error}")
                
                # Format content based on requested formats
                content_parts = []
                
                if 'markdown' in formats and response.markdown:
                    content_parts.append(f"## Markdown Content:\n{response.markdown}")
                
                if 'html' in formats and response.html:
                    content_parts.append(f"## HTML Content:\n{response.html}")
                
                if 'rawHtml' in formats and response.raw_html:
                    content_parts.append(f"## Raw HTML Content:\n{response.raw_html}")
                
                if 'links' in formats and response.links:
                    content_parts.append(f"## Links Found:\n{chr(10).join(response.links)}")
                
                if 'screenshot' in formats and response.screenshot:
                    content_parts.append(f"## Screenshot (Base64):\n{response.screenshot}")
                
                if 'extract' in formats and response.extract:
                    content_parts.append(f"## Extracted Data:\n{json.dumps(response.extract, indent=2)}")
                
                return chr(10).join(content_parts) if content_parts else "No content available"
                
            except Exception as e:
                raise ToolException(f"Error scraping URL: {str(e)}")
        
        return scrape_url_tool


class SearchWebTool(BaseFirecrawlTool):
    """Tool for searching the web using Firecrawl."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def search_web_tool(
            query: str,
            limit: int = 5,
            lang: str = "en",
            country: str = "us",
            scrape_options: Dict = None
        ) -> str:
            """
            Search the web and optionally extract content from search results using Firecrawl.
            
            Best for: Finding specific information across multiple websites, when you don't know which website has the information.
            Not recommended for: When you already know which website to scrape (use scrape).
            
            Args:
                query: Search query string
                limit: Maximum number of results to return. Defaults to 5.
                lang: Language code for search results. Defaults to "en".
                country: Country code for search results. Defaults to "us".
                scrape_options: Options for scraping search results.
                    Can include: formats, onlyMainContent, waitFor
            
            Returns:
                Formatted search results with optional scraped content
            
            Raises:
                ToolException: If there's an error during search
            """
            try:
                response = await self.client.search(
                    query=query,
                    limit=limit,
                    lang=lang,
                    country=country,
                    scrape_options=scrape_options
                )
                
                success = response.get('success', True)
                data = response.get('data', [])
                error = response.get('error', None)
                
                if not success:
                    raise ToolException(f"Search failed: {error}")
                
                # Format the results
                results = []
                for i, result in enumerate(data, 1):
                    result_text = f"Result {i}:\n"
                    result_text += f"URL: {result.get('url', 'No URL')}\n"
                    result_text += f"Title: {result.get('title', 'No title')}\n"
                    result_text += f"Description: {result.get('description', 'No description')}\n"
                    
                    if result.get('markdown'):
                        result_text += f"Content:\n{result['markdown']}\n"
                    
                    results.append(result_text)
                
                return chr(10).join(results) if results else "No search results found"
                
            except Exception as e:
                raise ToolException(f"Error searching web: {str(e)}")
        
        return search_web_tool


class MapUrlTool(BaseFirecrawlTool):
    """Tool for mapping a website to discover URLs."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def map_url_tool(
            url: str,
            search: str = None,
            ignore_sitemap: bool = False,
            sitemap_only: bool = False,
            include_subdomains: bool = False,
            limit: int = None
        ) -> str:
            """
            Map a website to discover all indexed URLs on the site using Firecrawl.
            
            Best for: Discovering URLs on a website before deciding what to scrape.
            Not recommended for: When you already know which specific URL you need (use scrape).
            
            Args:
                url: Starting URL for URL discovery
                search: Optional search term to filter URLs
                ignore_sitemap: Skip sitemap.xml discovery and only use HTML links
                sitemap_only: Only use sitemap.xml for discovery, ignore HTML links
                include_subdomains: Include URLs from subdomains in results
                limit: Maximum number of URLs to return
            
            Returns:
                List of discovered URLs
            
            Raises:
                ToolException: If there's an error during mapping
            """
            try:
                response = await self.client.map_url(
                    url=url,
                    search=search,
                    ignore_sitemap=ignore_sitemap,
                    sitemap_only=sitemap_only,
                    include_subdomains=include_subdomains,
                    limit=limit
                )
                
                if not response.success:
                    raise ToolException(f"Mapping failed: {response.error}")
                
                links = response.links
                if not links:
                    return "No URLs found on the website"
                
                return f"Found {len(links)} URLs:\n" + chr(10).join(links)
                
            except Exception as e:
                raise ToolException(f"Error mapping URL: {str(e)}")
        
        return map_url_tool


class ExtractStructuredTool(BaseFirecrawlTool):
    """Tool for extracting structured information from web pages."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def extract_structured_tool(
            urls: List[str],
            prompt: str = None,
            system_prompt: str = None,
            schema: Dict = None,
            allow_external_links: bool = False,
            enable_web_search: bool = False,
            include_subdomains: bool = False
        ) -> str:
            """
            Extract structured information from web pages using LLM capabilities with Firecrawl.
            
            Best for: Extracting specific structured data like prices, names, details.
            Not recommended for: When you need the full content of a page (use scrape).
            
            Args:
                urls: List of URLs to extract information from
                prompt: Custom prompt for the LLM extraction
                system_prompt: System prompt to guide the LLM
                schema: JSON schema for structured data extraction
                allow_external_links: Allow extraction from external links
                enable_web_search: Enable web search for additional context
                include_subdomains: Include subdomains in extraction
            
            Returns:
                Extracted structured data as defined by your schema
            
            Raises:
                ToolException: If there's an error during extraction
            """
            try:
                response = await self.client.extract(
                    urls=urls,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    schema=schema,
                    allow_external_links=allow_external_links,
                    enable_web_search=enable_web_search
                )
                
                if not response.success:
                    raise ToolException(f"Extraction failed: {response.error}")
                
                return json.dumps(response.data, indent=2)
                
            except Exception as e:
                raise ToolException(f"Error extracting structured data: {str(e)}")
        
        return extract_structured_tool


class DeepResearchTool(BaseFirecrawlTool):
    """Tool for conducting deep web research."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def deep_research_tool(
            query: str,
            max_depth: int = 3,
            time_limit: int = 120,
            max_urls: int = 50
        ) -> str:
            """
            Conduct deep web research on a query using intelligent crawling, search, and LLM analysis.
            
            Best for: Complex research questions requiring multiple sources, in-depth analysis.
            Not recommended for: Simple questions that can be answered with a single search.
            
            Args:
                query: The research question or topic to explore
                max_depth: Maximum recursive depth for crawling/search. Defaults to 3.
                time_limit: Time limit in seconds for the research session. Defaults to 120.
                max_urls: Maximum number of URLs to analyze. Defaults to 50.
            
            Returns:
                Final analysis generated by an LLM based on research
            
            Raises:
                ToolException: If there's an error during research
            """
            try:
                response = await self.client.deep_research(
                    query=query,
                    max_depth=max_depth,
                    time_limit=time_limit,
                    max_urls=max_urls
                )
                
                if not response.success:
                    raise ToolException(f"Deep research failed: {response.error}")
                
                return response.data.final_analysis if response.data else 'No analysis available'
                
            except Exception as e:
                raise ToolException(f"Error conducting deep research: {str(e)}")
        
        return deep_research_tool


class CrawlUrlTool(BaseFirecrawlTool):
    """Tool for crawling websites."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def crawl_url_tool(
            url: str,
            max_depth: int = 2,
            limit: int = 100,
            allow_external_links: bool = False,
            deduplicate_similar_urls: bool = True,
            exclude_paths: List[str] = None,
            include_paths: List[str] = None
        ) -> str:
            """
            Starts an asynchronous crawl job on a website and extracts content from all pages.
            
            Best for: Extracting content from multiple related pages, when you need comprehensive coverage.
            Not recommended for: Extracting content from a single page (use scrape).
            
            Args:
                url: Starting URL for the crawl
                max_depth: Maximum link depth to crawl. Defaults to 2.
                limit: Maximum number of pages to crawl. Defaults to 100.
                allow_external_links: Allow crawling links to external domains
                deduplicate_similar_urls: Remove similar URLs during crawl
                exclude_paths: URL paths to exclude from crawling
                include_paths: Only crawl these URL paths
            
            Returns:
                Crawl job ID and instructions for checking status
            
            Raises:
                ToolException: If there's an error during crawl initiation
            """
            try:
                response = await self.client.async_crawl_url(
                    url=url,
                    max_depth=max_depth,
                    limit=limit,
                    allow_external_links=allow_external_links,
                    deduplicate_similar_urls=deduplicate_similar_urls,
                    exclude_paths=exclude_paths,
                    include_paths=include_paths
                )
                
                if not response.success:
                    raise ToolException(f"Crawl failed: {response.error}")
                
                return f"Started crawl for {url} with job ID: {response.id}. Use check_crawl_status to check progress."
                
            except Exception as e:
                raise ToolException(f"Error starting crawl: {str(e)}")
        
        return crawl_url_tool


class CheckCrawlStatusTool(BaseFirecrawlTool):
    """Tool for checking crawl job status."""
    
    def __init__(self, api_key: Optional[str] = None, config_dict: Optional[dict] = None):
        super().__init__(api_key, config_dict)
        self.tool = self._create_tool()
    
    def _create_tool(self):
        @tool
        async def check_crawl_status_tool(crawl_id: str) -> str:
            """
            Check the status of a crawl job.
            
            Args:
                crawl_id: Crawl job ID to check
            
            Returns:
                Status and progress of the crawl job, including results if available
            
            Raises:
                ToolException: If there's an error checking crawl status
            """
            try:
                response = await self.client.check_crawl_status(id=crawl_id)
                
                if not response.success:
                    raise ToolException(f"Status check failed: {response.error}")
                
                status_info = f"Crawl Status:\n"
                status_info += f"Status: {response.status}\n"
                status_info += f"Progress: {response.completed}/{response.total}\n"
                status_info += f"Credits Used: {response.creditsUsed}\n"
                status_info += f"Expires At: {response.expiresAt}\n"
                
                if response.data:
                    status_info += f"\nResults:\n"
                    for i, doc in enumerate(response.data[:5], 1):  # Show first 5 results
                        content = doc.markdown or doc.html or 'No content'
                        status_info += f"Result {i}:\n"
                        status_info += f"URL: {doc.url}\n"
                        status_info += f"Content: {content[:100]}{'...' if len(content) > 100 else ''}\n\n"
                    
                    if len(response.data) > 5:
                        status_info += f"... and {len(response.data) - 5} more results\n"
                
                return status_info
                
            except Exception as e:
                raise ToolException(f"Error checking crawl status: {str(e)}")
        
        return check_crawl_status_tool 