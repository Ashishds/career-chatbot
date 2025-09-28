"""
Main application entry point for the AI Agent.

This module serves as the main entry point for the application,
handling configuration validation and launching the web interface.
"""

import sys
import os
from typing import Optional
from config import config
from web_interface import launch_web_app


def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.
    
    Returns:
        bool: True if environment is valid, False otherwise.
    """
    if not config.validate_config():
        missing_vars = config.get_missing_config()
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return False
    return True


def check_required_files() -> bool:
    """
    Check that required files exist.
    
    Returns:
        bool: True if all required files exist, False otherwise.
    """
    required_files = [
        config.linkedin_pdf_path,
        config.summary_file_path
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("Error: Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("\nPlease ensure these files exist in the correct locations.")
        return False
    
    return True


def main() -> None:
    """
    Main application entry point.
    
    This function handles application initialization, validation,
    and launching the web interface.
    """
    print("Starting AI Agent Application...")
    
    # Validate environment configuration
    if not validate_environment():
        sys.exit(1)
    
    # Check required files
    if not check_required_files():
        sys.exit(1)
    
    print("Configuration validated successfully!")
    print(f"Agent Name: {config.agent_name}")
    print(f"OpenAI Model: {config.openai_model}")
    print(f"App Title: {config.app_title}")
    
    # Check notification status
    if config.has_notifications():
        print("✅ Notifications: Enabled (Pushover configured)")
    else:
        print("ℹ️  Notifications: Disabled (optional feature)")
        print("   To enable notifications, set PUSHOVER_TOKEN and PUSHOVER_USER in your .env file")
    
    # Launch the web application
    try:
        print("Launching web interface...")
        launch_web_app(share=False, debug=False)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
