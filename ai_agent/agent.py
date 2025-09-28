"""
AI Agent module for handling conversations and responses.

This module contains the main AI agent class that manages conversations,
system prompts, and tool interactions.
"""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pypdf import PdfReader
from config import config
from tools import get_tool_definitions, handle_tool_calls


class AIAgent:
    """
    AI Agent class that handles conversations and tool interactions.
    
    This class manages the AI agent's personality, system prompts,
    and conversation flow with users.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize the AI agent.
        
        Args:
            name: Optional name for the agent. If None, uses config value.
        """
        self.name = name or config.agent_name
        self.openai_client = OpenAI()
        self.tools = get_tool_definitions()
        
        # Load agent's background information
        self._load_background_info()
    
    def _load_background_info(self) -> None:
        """Load the agent's background information from files."""
        try:
            # Load LinkedIn profile from PDF
            self.linkedin_content = self._extract_linkedin_content()
        except Exception as e:
            print(f"Warning: Could not load LinkedIn PDF: {e}")
            self.linkedin_content = ""
        
        try:
            # Load summary from text file
            with open(config.summary_file_path, "r", encoding="utf-8") as f:
                self.summary = f.read()
        except Exception as e:
            print(f"Warning: Could not load summary file: {e}")
            self.summary = ""
    
    def _extract_linkedin_content(self) -> str:
        """
        Extract content from LinkedIn PDF file.
        
        Returns:
            str: Extracted text content from the PDF.
        """
        linkedin_content = ""
        
        try:
            reader = PdfReader(config.linkedin_pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    linkedin_content += text
        except Exception as e:
            print(f"Error extracting LinkedIn content: {e}")
            
        return linkedin_content
    
    def get_system_prompt(self) -> str:
        """
        Generate the system prompt for the AI agent.
        
        Returns:
            str: The complete system prompt.
        """
        system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool."""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin_content}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        
        return system_prompt
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """
        Process a chat message and return a response.
        
        Args:
            message: The user's message.
            history: Previous conversation history.
            
        Returns:
            str: The agent's response.
        """
        # Build messages list with system prompt
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + history + [{"role": "user", "content": message}]
        
        # Process the conversation with tool calling support
        return self._process_conversation(messages)
    
    def _process_conversation(self, messages: List[Dict[str, str]]) -> str:
        """
        Process the conversation with support for tool calling.
        
        Args:
            messages: List of conversation messages.
            
        Returns:
            str: The final response from the agent.
        """
        done = False
        
        while not done:
            try:
                response = self.openai_client.chat.completions.create(
                    model=config.openai_model,
                    messages=messages,
                    tools=self.tools
                )
                
                if response.choices[0].finish_reason == "tool_calls":
                    # Handle tool calls
                    message = response.choices[0].message
                    tool_calls = message.tool_calls
                    
                    # Process tool calls
                    tool_results = handle_tool_calls(tool_calls)
                    
                    # Add the message and tool results to conversation
                    messages.append(message)
                    messages.extend(tool_results)
                    
                else:
                    # Conversation is complete
                    done = True
                    
            except Exception as e:
                print(f"Error in conversation processing: {e}")
                return "I apologize, but I encountered an error processing your request. Please try again."
        
        return response.choices[0].message.content
