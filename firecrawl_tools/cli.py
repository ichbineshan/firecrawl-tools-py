"""
Command-line interface for Firecrawl Tools.
"""

import asyncio
import json
import sys
from typing import Optional
import argparse

from .core import FirecrawlTools
from .exceptions import FirecrawlToolsError, ConfigurationError


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Firecrawl Tools - Web scraping and data extraction tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a URL
  firecrawl-tools scrape --url https://example.com --formats markdown html

  # Search the web
  firecrawl-tools search --query "Python web scraping" --limit 5

  # Map a website
  firecrawl-tools map --url https://example.com --limit 50

  # Extract structured data
  firecrawl-tools extract --urls https://example.com --prompt "Extract all product names"

  # Start a crawl
  firecrawl-tools crawl --url https://example.com --max-depth 2

  # Check crawl status
  firecrawl-tools status --crawl-id your_crawl_id
        """
    )
    
    # Global options
    parser.add_argument(
        "--api-key",
        help="Firecrawl API key (or set FIRECRAWL_API_KEY environment variable)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape content from a URL")
    scrape_parser.add_argument("--url", required=True, help="URL to scrape")
    scrape_parser.add_argument(
        "--formats",
        nargs="+",
        default=["markdown"],
        choices=["markdown", "html", "rawHtml", "screenshot", "links", "screenshot@fullPage", "extract"],
        help="Content formats to extract"
    )
    scrape_parser.add_argument(
        "--only-main-content",
        action="store_true",
        default=True,
        help="Extract only main content"
    )
    scrape_parser.add_argument("--wait-for", type=int, help="Wait time in milliseconds")
    scrape_parser.add_argument("--timeout", type=int, help="Timeout in milliseconds")
    scrape_parser.add_argument("--mobile", action="store_true", help="Use mobile viewport")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Maximum results")
    search_parser.add_argument("--lang", default="en", help="Language code")
    search_parser.add_argument("--country", default="us", help="Country code")
    search_parser.add_argument("--scrape", action="store_true", help="Scrape search results")
    
    # Map command
    map_parser = subparsers.add_parser("map", help="Map a website")
    map_parser.add_argument("--url", required=True, help="Starting URL")
    map_parser.add_argument("--search", help="Search term to filter URLs")
    map_parser.add_argument("--ignore-sitemap", action="store_true", help="Skip sitemap.xml")
    map_parser.add_argument("--sitemap-only", action="store_true", help="Only use sitemap.xml")
    map_parser.add_argument("--include-subdomains", action="store_true", help="Include subdomains")
    map_parser.add_argument("--limit", type=int, help="Maximum URLs to return")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract structured data")
    extract_parser.add_argument("--urls", nargs="+", required=True, help="URLs to extract from")
    extract_parser.add_argument("--prompt", help="Custom extraction prompt")
    extract_parser.add_argument("--system-prompt", help="System prompt")
    extract_parser.add_argument("--schema", help="JSON schema file")
    extract_parser.add_argument("--allow-external-links", action="store_true", help="Allow external links")
    extract_parser.add_argument("--enable-web-search", action="store_true", help="Enable web search")
    
    # Research command
    research_parser = subparsers.add_parser("research", help="Conduct deep research")
    research_parser.add_argument("--query", required=True, help="Research query")
    research_parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth")
    research_parser.add_argument("--time-limit", type=int, default=120, help="Time limit in seconds")
    research_parser.add_argument("--max-urls", type=int, default=50, help="Maximum URLs")
    
    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Start a website crawl")
    crawl_parser.add_argument("--url", required=True, help="Starting URL")
    crawl_parser.add_argument("--max-depth", type=int, default=2, help="Maximum depth")
    crawl_parser.add_argument("--limit", type=int, default=100, help="Maximum pages")
    crawl_parser.add_argument("--allow-external-links", action="store_true", help="Allow external links")
    crawl_parser.add_argument("--deduplicate", action="store_true", default=True, help="Deduplicate URLs")
    crawl_parser.add_argument("--exclude-paths", nargs="+", help="Paths to exclude")
    crawl_parser.add_argument("--include-paths", nargs="+", help="Paths to include")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check crawl status")
    status_parser.add_argument("--crawl-id", required=True, help="Crawl job ID")
    
    return parser


async def run_scrape(args, tools):
    """Run the scrape command."""
    scrape_tool = await tools.get_scrape_tool()
    result = await scrape_tool.ainvoke({
        "url": args.url,
        "formats": args.formats,
        "only_main_content": args.only_main_content,
        "wait_for": args.wait_for,
        "timeout": args.timeout,
        "mobile": args.mobile
    })
    return result


async def run_search(args, tools):
    """Run the search command."""
    search_tool = await tools.get_search_tool()
    scrape_options = None
    if args.scrape:
        scrape_options = {"formats": ["markdown"], "onlyMainContent": True}
    
    result = await search_tool.ainvoke({
        "query": args.query,
        "limit": args.limit,
        "lang": args.lang,
        "country": args.country,
        "scrape_options": scrape_options
    })
    return result


async def run_map(args, tools):
    """Run the map command."""
    map_tool = await tools.get_map_tool()
    result = await map_tool.ainvoke({
        "url": args.url,
        "search": args.search,
        "ignore_sitemap": args.ignore_sitemap,
        "sitemap_only": args.sitemap_only,
        "include_subdomains": args.include_subdomains,
        "limit": args.limit
    })
    return result


async def run_extract(args, tools):
    """Run the extract command."""
    extract_tool = await tools.get_extract_tool()
    
    schema = None
    if args.schema:
        with open(args.schema, 'r') as f:
            schema = json.load(f)
    
    result = await extract_tool.ainvoke({
        "urls": args.urls,
        "prompt": args.prompt,
        "system_prompt": args.system_prompt,
        "schema": schema,
        "allow_external_links": args.allow_external_links,
        "enable_web_search": args.enable_web_search
    })
    return result


async def run_research(args, tools):
    """Run the research command."""
    research_tool = await tools.get_research_tool()
    result = await research_tool.ainvoke({
        "query": args.query,
        "max_depth": args.max_depth,
        "time_limit": args.time_limit,
        "max_urls": args.max_urls
    })
    return result


async def run_crawl(args, tools):
    """Run the crawl command."""
    crawl_tool = await tools.get_crawl_tool()
    result = await crawl_tool.ainvoke({
        "url": args.url,
        "max_depth": args.max_depth,
        "limit": args.limit,
        "allow_external_links": args.allow_external_links,
        "deduplicate_similar_urls": args.deduplicate,
        "exclude_paths": args.exclude_paths,
        "include_paths": args.include_paths
    })
    return result


async def run_status(args, tools):
    """Run the status command."""
    status_tool = await tools.get_status_tool()
    result = await status_tool.ainvoke({
        "crawl_id": args.crawl_id
    })
    return result


async def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize tools
        tools = FirecrawlTools(api_key=args.api_key)
        
        # Run the appropriate command
        command_handlers = {
            "scrape": run_scrape,
            "search": run_search,
            "map": run_map,
            "extract": run_extract,
            "research": run_research,
            "crawl": run_crawl,
            "status": run_status,
        }
        
        handler = command_handlers[args.command]
        result = await handler(args, tools)
        
        # Format and output result
        if args.format == "json":
            output_data = {"result": result}
            output_text = json.dumps(output_data, indent=2)
        else:
            output_text = str(result)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)
        else:
            print(output_text)
            
    except (FirecrawlToolsError, ConfigurationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 