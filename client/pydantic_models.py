# client/pydantic_models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Request(BaseModel):
    """
    Pydantic model for a single request to the MCP server.
    """
    id: str
    method: str
    params: Optional[Dict[str, Any]] = None

class RequestPayload(BaseModel):
    """
    Pydantic model for the entire request payload sent to the MCP server.
    """
    id: str
    requests: List[Request]

class Result(BaseModel):
    """
    Pydantic model for a single result from the MCP server.
    """
    id: str
    method: str
    results: List[Any]

class ResponsePayload(BaseModel):
    """
    Pydantic model for the entire response payload received from the MCP server.
    """
    id: str
    results: List[Result]