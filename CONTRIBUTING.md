# Contributing to Firecrawl Tools

Thank you for your interest in contributing to Firecrawl Tools! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate of others in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following the guidelines below
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Installation

1. Clone your fork:
   ```bash
   git clone https://github.com/ichbineshan/firecrawl-tools-py.git
   cd firecrawl-tools
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Environment Variables

Create a `.env` file in the project root for local development:

```bash
FIRECRAWL_API_KEY=your_test_api_key_here
```

## Making Changes

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run the formatters before committing:

```bash
black firecrawl_tools tests examples
isort firecrawl_tools tests examples
```

### Type Hints

All new code should include type hints:

```python
from typing import List, Optional, Dict

def process_data(data: List[str], config: Optional[Dict] = None) -> str:
    """Process the given data with optional configuration."""
    pass
```

### Documentation

- All public functions and classes must have docstrings
- Use Google-style docstrings
- Include type information in docstrings

Example:

```python
def scrape_url(url: str, formats: List[str] = None) -> str:
    """Scrape content from a URL.
    
    Args:
        url: The URL to scrape
        formats: Content formats to extract. Defaults to ['markdown'].
        
    Returns:
        The scraped content
        
    Raises:
        ToolException: If scraping fails
    """
    pass
```

### Error Handling

- Use custom exceptions from `firecrawl_tools.exceptions`
- Provide meaningful error messages
- Include context when possible

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=firecrawl_tools
```

Run specific test files:
```bash
pytest tests/test_config.py
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for common setup

Example test:

```python
import pytest
from firecrawl_tools.config import FirecrawlConfig

def test_config_creation():
    """Test creating a config with required fields."""
    config = FirecrawlConfig(api_key="test_key")
    assert config.api_key == "test_key"
    assert config.timeout == 30
```

### Test Structure

- Unit tests in `tests/`
- Integration tests in `tests/integration/`
- Example tests in `tests/examples/`

## Documentation

### Code Documentation

- Keep docstrings up to date
- Include examples in docstrings
- Document all public APIs

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Update CLI help text

### API Documentation

- Document all tool parameters
- Include usage examples
- Explain error conditions

## Submitting Changes

### Pull Request Process

1. **Create a descriptive title** for your PR
2. **Write a detailed description** explaining:
   - What the change does
   - Why it's needed
   - How it works
3. **Reference related issues** using keywords like "Fixes #123"
4. **Include tests** for new functionality
5. **Update documentation** as needed

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass
- [ ] Updated existing tests

## Documentation
- [ ] Updated docstrings
- [ ] Updated README if needed
- [ ] Updated examples if needed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No new warnings
- [ ] Added type hints
```

### Review Process

- All PRs require review
- Address review comments promptly
- Maintainers may request changes
- Tests must pass before merging

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with changes
3. **Create release tag** on GitHub
4. **Build and publish** to PyPI

### Changelog Format

```markdown
## [1.2.0] - 2024-01-15

### Added
- New feature X
- Support for Y

### Changed
- Improved performance of Z

### Fixed
- Bug in A
- Issue with B
```

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check the README and examples

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors list

Thank you for contributing to Firecrawl Tools! 🚀 