# Firecrawl Tools - Project Structure

This document provides an overview of the project structure and organization.

## Directory Structure

```
firecrawl_tools/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT license
├── pyproject.toml              # Modern Python packaging configuration
├── CHANGELOG.md                # Version history and changes
├── CONTRIBUTING.md             # Contributing guidelines
├── PROJECT_STRUCTURE.md        # This file
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
│
├── firecrawl_tools/            # Main package directory
│   ├── __init__.py             # Package initialization and exports
│   ├── core.py                 # Main FirecrawlTools class
│   ├── config.py               # Configuration management
│   ├── exceptions.py           # Custom exception classes
│   ├── tools.py                # Individual tool implementations
│   └── cli.py                  # Command-line interface
│
├── examples/                   # Usage examples
│   └── react_agent_example.py  # ReAct agent demonstration
│
└── tests/                      # Test suite
    ├── __init__.py             # Test package initialization
    ├── test_config.py          # Configuration tests
    └── test_core.py            # Core functionality tests
```

## Package Organization

### Core Package (`firecrawl_tools/`)

#### `__init__.py`
- Package initialization
- Main exports and version information
- Public API definition

#### `core.py`
- `FirecrawlTools` class - main interface
- Tool management and caching
- Unified access to all tools

#### `config.py`
- `FirecrawlConfig` class for configuration
- Environment variable handling
- Configuration validation

#### `exceptions.py`
- Custom exception hierarchy
- `FirecrawlToolsError` base class
- Specific exception types for different error scenarios

#### `tools.py`
- Individual tool classes:
  - `ScrapeUrlTool` - URL content scraping
  - `SearchWebTool` - Web search functionality
  - `MapUrlTool` - Website URL discovery
  - `ExtractStructuredTool` - Structured data extraction
  - `DeepResearchTool` - Deep web research
  - `CrawlUrlTool` - Website crawling
  - `CheckCrawlStatusTool` - Crawl status monitoring
- Base class `BaseFirecrawlTool` for common functionality

#### `cli.py`
- Command-line interface implementation
- Argument parsing and validation
- Tool execution and output formatting

### Examples (`examples/`)

#### `react_agent_example.py`
- Modern, comprehensive usage example
- Demonstrates intelligent agent integration
- Covers scraping, searching, extraction, mapping, and more

### Tests (`tests/`)

#### `test_config.py`
- Configuration management tests
- Environment variable handling
- Validation tests

#### `test_core.py`
- Main class functionality tests
- Tool management tests
- Caching behavior tests

## Key Design Principles

### 1. Modularity
- Each tool is implemented as a separate class
- Common functionality in base classes
- Clear separation of concerns

### 2. Configuration Management
- Multiple configuration sources (env vars, dict, direct)
- Priority-based configuration resolution
- Validation and error handling

### 3. Error Handling
- Custom exception hierarchy
- Meaningful error messages
- Proper error propagation

### 4. Type Safety
- Comprehensive type hints
- MyPy configuration
- Type validation

### 5. Testing
- Unit tests for all components
- Mock external dependencies
- Coverage reporting

### 6. Documentation
- Comprehensive docstrings
- Usage examples
- API documentation

## Development Workflow

### Setup
1. Clone repository
2. Create virtual environment
3. Install development dependencies: `pip install -e ".[dev]"`
4. Install pre-commit hooks: `pre-commit install`

### Development
1. Create feature branch
2. Make changes following style guidelines
3. Write tests for new functionality
4. Update documentation
5. Run tests and quality checks

### Quality Assurance
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing
- **pre-commit**: Automated checks

### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Build and publish to PyPI

## Dependencies

### Core Dependencies
- `firecrawl` - Firecrawl API client
- `langchain-core` - LangChain tool framework
- `pydantic` - Data validation

### Development Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking
- `pre-commit` - Git hooks

## API Design

### Main Interface
```python
from firecrawl_tools import FirecrawlTools

# Initialize
tools = FirecrawlTools(api_key="your_key")

# Get individual tools
scrape_tool = await tools.get_scrape_tool()
search_tool = await tools.get_search_tool()

# Use tools
result = await scrape_tool.ainvoke({"url": "https://example.com"})
```

### Tool Interface
All tools follow the LangChain tool interface:
- Async `ainvoke()` method
- Structured input/output
- Error handling with `ToolException`
- Comprehensive documentation

## Configuration Options

### Environment Variables
- `FIRECRAWL_API_KEY` - Required API key
- `FIRECRAWL_BASE_URL` - Optional custom base URL
- `FIRECRAWL_TIMEOUT` - Request timeout (default: 30)
- `FIRECRAWL_MAX_RETRIES` - Max retries (default: 3)

### Direct Configuration
```python
config = {
    "firecrawl_api_key": "your_key",
    "timeout": 60,
    "max_retries": 5
}
tools = FirecrawlTools(config_dict=config)
```

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Edge case coverage

### Integration Tests
- End-to-end functionality
- Real API interaction (with test keys)
- Error scenario testing

### Test Coverage
- Aim for >90% code coverage
- Critical path coverage
- Error handling coverage

## Documentation Strategy

### Code Documentation
- Google-style docstrings
- Type hints
- Usage examples in docstrings

### User Documentation
- Comprehensive README
- Usage examples
- API reference

### Developer Documentation
- Contributing guidelines
- Development setup
- Release process

This structure provides a solid foundation for an open-source project with clear organization, comprehensive testing, and excellent developer experience. 