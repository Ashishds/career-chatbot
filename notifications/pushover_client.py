"""
Pushover notification client module.

This module handles sending notifications via Pushover API.
"""

import requests
from typing import Optional
from config import config


class PushoverClient:
    """Client for sending notifications via Pushover API."""
    
    def __init__(self, token: Optional[str] = None, user: Optional[str] = None):
        """
        Initialize Pushover client.
        
        Args:
            token: Pushover application token. If None, uses config value.
            user: Pushover user key. If None, uses config value.
        """
        self.token = token or config.pushover_token
        self.user = user or config.pushover_user
        self.api_url = "https://api.pushover.net/1/messages.json"
    
    def send_notification(self, message: str, title: Optional[str] = None) -> bool:
        """
        Send a notification via Pushover.
        
        Args:
            message: The message content to send.
            title: Optional title for the notification.
            
        Returns:
            bool: True if notification was sent successfully, False otherwise.
        """
        if not self.token or not self.user:
            print("Info: Pushover notifications not configured (optional feature)")
            return True  # Return True to indicate "success" even when not configured
        
        try:
            data = {
                "token": self.token,
                "user": self.user,
                "message": message,
            }
            
            if title:
                data["title"] = title
            
            response = requests.post(self.api_url, data=data, timeout=10)
            response.raise_for_status()
            return True
            
        except requests.RequestException as e:
            print(f"Failed to send Pushover notification: {e}")
            return False
    
    def send_user_registration(self, name: str, email: str, notes: str = "") -> bool:
        """
        Send a user registration notification.
        
        Args:
            name: User's name.
            email: User's email address.
            notes: Additional notes about the user.
            
        Returns:
            bool: True if notification was sent successfully, False otherwise.
        """
        message = f"New user registration: {name} ({email})"
        if notes:
            message += f" - Notes: {notes}"
        
        return self.send_notification(message, "User Registration")
    
    def send_unknown_question(self, question: str) -> bool:
        """
        Send a notification about an unknown question.
        
        Args:
            question: The question that couldn't be answered.
            
        Returns:
            bool: True if notification was sent successfully, False otherwise.
        """
        message = f"Unknown question recorded: {question}"
        return self.send_notification(message, "Unknown Question")


# Global notification client instance
notification_client = PushoverClient()
