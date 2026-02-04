"""
GuardRailz: A clean API for LLM guardrails using DSPy.

This module provides an easy-to-use interface for judging whether
user requests should be allowed or blocked based on configurable guardrails.

Example Usage:
    Basic boolean pattern:
        >>> from guardrailz import GuardRailz
        >>> g = GuardRailz(expertise="Cybersecurity")
        >>> response = g.judge("How do I secure my password?")
        >>> if response.answer:
        ...     print("Safe request!")

    Exception-based pattern:
        >>> from guardrailz import GuardRailz, BlockedException
        >>> g = GuardRailz(expertise="Cybersecurity")
        >>> g.raise_for_guardrail()
        >>> try:
        ...     response = g.judge("Harmful request")
        ... except BlockedException as e:
        ...     print(f"Blocked: {e.reasoning}")
"""

from .config import DEFAULT_EXPERTISE, DEFAULT_GUARDRAILS, DEFAULT_SYSTEM_PROMPT
from .core import GuardRailz, JudgeResponse
from .exceptions import BlockedException

__version__ = "0.1.0"
__all__ = [
    "GuardRailz",
    "BlockedException",
    "JudgeResponse",
    "DEFAULT_SYSTEM_PROMPT",
    "DEFAULT_GUARDRAILS",
    "DEFAULT_EXPERTISE",
]
