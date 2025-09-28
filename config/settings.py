"""
Configuration management module for the AI Agent application.

This module handles environment variables, settings, and configuration
for the application.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class to manage application settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv(override=True)
        self._load_settings()
    
    def _load_settings(self) -> None:
        """Load all configuration settings from environment variables."""
        # OpenAI Configuration
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Pushover Notification Configuration
        self.pushover_token: Optional[str] = os.getenv("PUSHOVER_TOKEN")
        self.pushover_user: Optional[str] = os.getenv("PUSHOVER_USER")
        
        # Application Configuration
        self.agent_name: str = os.getenv("AGENT_NAME", "Ankur Warikoo")
        self.linkedin_pdf_path: str = os.getenv("LINKEDIN_PDF_PATH", "me/Ankur Warikoo.pdf")
        self.summary_file_path: str = os.getenv("SUMMARY_FILE_PATH", "me/summary.txt")
        
        # Web Interface Configuration
        self.app_title: str = os.getenv("APP_TITLE", "AI Agent Chat Interface")
        self.app_description: str = os.getenv("APP_DESCRIPTION", "Chat with an AI agent")
    
    def validate_config(self) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        required_vars = [
            self.openai_api_key
        ]
        
        return all(var is not None for var in required_vars)
    
    def get_missing_config(self) -> list[str]:
        """
        Get list of missing configuration variables.
        
        Returns:
            list[str]: List of missing configuration variable names.
        """
        missing = []
        
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        # Note: Pushover credentials are optional
            
        return missing
    
    def has_notifications(self) -> bool:
        """
        Check if notification system is configured.
        
        Returns:
            bool: True if both Pushover credentials are available.
        """
        return self.pushover_token is not None and self.pushover_user is not None


# Global configuration instance
config = Config()
