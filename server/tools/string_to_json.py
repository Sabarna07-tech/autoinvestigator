"""Utility to safely convert string representations of JSON into Python objects."""

from __future__ import annotations

import json
from typing import Any


def string_to_json(string: str) -> Any:
    """Convert a JSON string (optionally wrapped in Markdown fences) to Python.

    Parameters
    ----------
    string: str
        The string potentially containing JSON data. It may be wrapped in
        Markdown style triple backticks with or without a ``json`` hint.

    Returns
    -------
    Any
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the input cannot be parsed as valid JSON.
    """

    cleaned = string.strip()

    # Remove surrounding triple backticks and optional "json" hint
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned[3:-3].strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON string: {exc}") from exc


if __name__ == "__main__":  # pragma: no cover - simple manual test
    sample = """```json\n{\n    \"cik\": \"12345\",\n    \"ticker\": \"afd\"\n}\n```"""
    print(string_to_json(sample))

