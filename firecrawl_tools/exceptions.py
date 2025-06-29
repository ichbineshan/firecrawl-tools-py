"""
Custom exceptions for the Firecrawl Tools package.
"""


class FirecrawlToolsError(Exception):
    """Base exception for all Firecrawl Tools errors."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ConfigurationError(FirecrawlToolsError):
    """Raised when there's an issue with configuration."""
    pass


class AuthenticationError(FirecrawlToolsError):
    """Raised when authentication fails."""
    pass


class ValidationError(FirecrawlToolsError):
    """Raised when input validation fails."""
    pass


class RateLimitError(FirecrawlToolsError):
    """Raised when rate limits are exceeded."""
    pass


class NetworkError(FirecrawlToolsError):
    """Raised when network-related errors occur."""
    pass 