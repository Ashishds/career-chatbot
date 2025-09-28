"""
Function tools module for the AI Agent.

This module defines the available tools that the AI agent can use
and their corresponding handler functions.
"""

import json
from typing import Dict, Any, List
from notifications import notification_client


def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> Dict[str, str]:
    """
    Record user details when they provide contact information.
    
    Args:
        email: User's email address.
        name: User's name (optional).
        notes: Additional notes about the user (optional).
        
    Returns:
        Dict[str, str]: Confirmation of recording.
    """
    # Send notification about user registration
    notification_client.send_user_registration(name, email, notes)
    
    return {"recorded": "ok"}


def record_unknown_question(question: str) -> Dict[str, str]:
    """
    Record questions that couldn't be answered.
    
    Args:
        question: The question that couldn't be answered.
        
    Returns:
        Dict[str, str]: Confirmation of recording.
    """
    # Send notification about unknown question
    notification_client.send_unknown_question(question)
    
    return {"recorded": "ok"}


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get the tool definitions for OpenAI function calling.
    
    Returns:
        List[Dict[str, Any]]: List of tool definitions.
    """
    record_user_details_json = {
        "name": "record_user_details",
        "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address of this user"
                },
                "name": {
                    "type": "string",
                    "description": "The user's name, if they provided it"
                },
                "notes": {
                    "type": "string",
                    "description": "Any additional information about the conversation that's worth recording to give context"
                }
            },
            "required": ["email"],
            "additionalProperties": False
        }
    }
    
    record_unknown_question_json = {
        "name": "record_unknown_question",
        "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question that couldn't be answered"
                }
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }
    
    return [
        {"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}
    ]


def handle_tool_calls(tool_calls: List[Any]) -> List[Dict[str, Any]]:
    """
    Handle tool calls from the AI agent.
    
    Args:
        tool_calls: List of tool calls from OpenAI.
        
    Returns:
        List[Dict[str, Any]]: List of tool results.
    """
    results = []
    
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"Tool called: {tool_name}", flush=True)
        
        # Get the function from globals
        tool_function = globals().get(tool_name)
        
        if tool_function:
            try:
                result = tool_function(**arguments)
            except Exception as e:
                print(f"Error executing tool {tool_name}: {e}")
                result = {"error": str(e)}
        else:
            print(f"Tool function {tool_name} not found")
            result = {"error": f"Tool {tool_name} not found"}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    
    return results
