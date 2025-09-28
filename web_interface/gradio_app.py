"""
Gradio web interface module for the AI Agent application.

This module provides the web interface using Gradio for user interactions.
"""

import gradio as gr
from typing import List, Tuple, Optional
from ai_agent import AIAgent
from config import config


class GradioWebInterface:
    """
    Gradio web interface for the AI Agent application.
    
    This class handles the web interface setup and user interactions.
    """
    
    def __init__(self, agent: Optional[AIAgent] = None):
        """
        Initialize the Gradio web interface.
        
        Args:
            agent: Optional AI agent instance. If None, creates a new one.
        """
        self.agent = agent or AIAgent()
        self.app = None
    
    def create_interface(self) -> gr.ChatInterface:
        """
        Create the Gradio chat interface.
        
        Returns:
            gr.ChatInterface: The configured chat interface.
        """
        return gr.ChatInterface(
            fn=self.agent.chat,
            title=config.app_title,
            description=config.app_description,
            examples=[
                "Tell me about your background",
                "What are your skills?",
                "How can I contact you?",
                "What projects have you worked on?"
            ],
            cache_examples=False
        )
    
    def launch(self, 
               share: bool = False, 
               server_name: str = "0.0.0.0", 
               server_port: int = 7860,
               debug: bool = False) -> None:
        """
        Launch the Gradio application.
        
        Args:
            share: Whether to create a public link.
            server_name: Server hostname.
            server_port: Server port.
            debug: Whether to run in debug mode.
        """
        if self.app is None:
            self.app = self.create_interface()
        
        self.app.launch(
            share=share,
            server_name=server_name,
            server_port=server_port,
            debug=debug
        )


def create_web_app() -> GradioWebInterface:
    """
    Create and configure the web application.
    
    Returns:
        GradioWebInterface: The configured web interface.
    """
    return GradioWebInterface()


def launch_web_app(share: bool = False, debug: bool = False) -> None:
    """
    Launch the web application.
    
    Args:
        share: Whether to create a public link.
        debug: Whether to run in debug mode.
    """
    app = create_web_app()
    app.launch(share=share, debug=debug)
