# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Firecrawl Tools
- Comprehensive set of async tools for web scraping and data extraction
- Support for URL scraping with multiple formats
- Web search functionality with optional content extraction
- Website mapping and URL discovery
- Structured data extraction using LLM capabilities
- Deep web research with intelligent crawling
- Asynchronous website crawling with status monitoring
- Command-line interface for all tools
- Configuration management with environment variables
- Comprehensive error handling and custom exceptions
- Type hints throughout the codebase
- Extensive test coverage
- Documentation and examples

### Features
- **ScrapeUrlTool**: Extract content from single URLs with advanced options
- **SearchWebTool**: Search the web and optionally scrape results
- **MapUrlTool**: Discover all indexed URLs on a website
- **ExtractStructuredTool**: Extract structured information using LLM capabilities
- **DeepResearchTool**: Conduct comprehensive web research
- **CrawlUrlTool**: Start asynchronous website crawling
- **CheckCrawlStatusTool**: Monitor crawl job progress

### Technical
- Built with LangChain for seamless AI integration
- Async/await support throughout
- Modern Python packaging with pyproject.toml
- Comprehensive test suite with pytest
- Code quality tools: Black, isort, flake8, mypy
- Pre-commit hooks for code quality
- MIT license for open source use

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Core FirecrawlTools class with unified interface
- Individual tool classes for each operation
- Configuration management system
- Custom exception hierarchy
- Command-line interface
- Basic and advanced usage examples
- Comprehensive test suite
- Documentation and contributing guidelines

### Features
- URL scraping with multiple format support
- Web search with optional content extraction
- Website mapping and URL discovery
- Structured data extraction
- Deep web research capabilities
- Asynchronous website crawling
- Crawl status monitoring

### Technical
- Python 3.8+ support
- Async/await patterns
- Type hints throughout
- LangChain integration
- Modern packaging standards
- Comprehensive error handling 