"""
Core GuardRailz class implementation.
"""

import os
from dataclasses import dataclass
from typing import Optional

import dspy
from dotenv import load_dotenv

from .config import (
    DEFAULT_API_BASE,
    DEFAULT_EXPERTISE,
    DEFAULT_GUARDRAILS,
    DEFAULT_MODEL,
    DEFAULT_SYSTEM_PROMPT,
)
from .exceptions import BlockedException
from .signatures import GuardrailsJudgeSignature


@dataclass
class JudgeResponse:
    """
    Response from the guardrails judge.

    Attributes:
        answer: True if request passes, False if blocked
        reasoning: Explanation for the decision
        original_text: The text that was judged
    """

    answer: bool
    reasoning: str
    original_text: str

    @property
    def passed(self) -> bool:
        """Alias for answer. Returns True if request passed guardrails."""
        return self.answer

    @property
    def blocked(self) -> bool:
        """Inverse of answer. Returns True if request was blocked."""
        return not self.answer

    def __str__(self):
        status = "PASSED" if self.answer else "BLOCKED"
        return f"JudgeResponse({status}): {self.reasoning}"


class _GuardrailsJudgeAssistant(dspy.Module):
    """Internal DSPy module for guardrails judging."""

    def __init__(self, system_prompt: str = ""):
        super().__init__()
        self.signature = GuardrailsJudgeSignature.with_instructions(system_prompt)
        self.generate_answer = dspy.ChainOfThought(self.signature)

    def forward(self, text, guardrails, expertise):
        prediction = self.generate_answer(
            text=text, guardrails=guardrails, expertise=expertise
        )

        # Parse the outputs
        answer = str(prediction.answer).lower() in [
            "true",
            "1",
            "yes",
        ]
        reasoning = prediction.reasoning

        # Return a structured response
        return dspy.Prediction(answer=answer, reasoning=reasoning)


class GuardRailz:
    """
    Main GuardRailz class for judging requests against guardrails.

    This class provides a clean API for checking whether user requests
    should be allowed or blocked based on configurable guardrails.

    Example (Boolean Pattern):
        >>> g = GuardRailz(expertise="Cybersecurity")
        >>> response = g.judge("How do I secure my password?")
        >>> if response.answer:
        ...     print("Safe request!")
        ... else:
        ...     print(f"Blocked: {response.reasoning}")

    Example (Exception Pattern):
        >>> g = GuardRailz(expertise="Cybersecurity")
        >>> g.raise_for_guardrail()
        >>> try:
        ...     response = g.judge("How do I hack a system?")
        ...     # Process safe request
        ... except BlockedException as e:
        ...     print(f"Blocked: {e.reasoning}")
    """

    def __init__(
        self,
        expertise: str = DEFAULT_EXPERTISE,
        guardrails: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        api_base: str = DEFAULT_API_BASE,
        raise_on_block: bool = False,
    ):
        """
        Initialize GuardRailz.

        Args:
            expertise: Area of expertise for the assistant (e.g., "Cybersecurity")
            guardrails: Custom guardrails rules (uses DEFAULT_GUARDRAILS if None)
            system_prompt: Custom system prompt (uses DEFAULT_SYSTEM_PROMPT if None)
            model: Model identifier (default: "openrouter/openai/gpt-4o-mini")
            api_key: API key (loads from LLM_API_KEY env var if None)
            api_base: API base URL for OpenRouter
            raise_on_block: If True, raise BlockedException when requests are blocked
        """
        # Load environment variables
        load_dotenv(override=True)

        # Set configuration
        self.expertise = expertise
        self.guardrails = guardrails or DEFAULT_GUARDRAILS
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.raise_on_block = raise_on_block

        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Provide via api_key parameter or LLM_API_KEY environment variable."
            )

        # Initialize DSPy language model
        self.lm = dspy.LM(
            model=model,
            api_base=api_base,
            api_key=self.api_key,
        )
        dspy.configure(lm=self.lm)
        dspy.settings.configure(lm=self.lm)

        # Initialize the guardrails judge assistant
        self._assistant = _GuardrailsJudgeAssistant(system_prompt=self.system_prompt)

    def judge(self, text: str) -> JudgeResponse:
        """
        Judge whether a text request should be allowed or blocked.

        Args:
            text: The user's request/instruction to evaluate

        Returns:
            JudgeResponse with answer (bool) and reasoning (str)

        Raises:
            BlockedException: If raise_on_block is True and request is blocked

        Example:
            >>> g = GuardRailz(expertise="Math")
            >>> response = g.judge("What is 2+2?")
            >>> print(response.answer)  # True or False
            >>> print(response.reasoning)
        """
        # Call the internal assistant
        prediction = self._assistant(
            text=text, guardrails=self.guardrails, expertise=self.expertise
        )

        # Create response object
        response = JudgeResponse(
            answer=prediction.answer, reasoning=prediction.reasoning, original_text=text
        )

        # Raise exception if configured and request is blocked
        if self.raise_on_block and response.blocked:
            raise BlockedException(reasoning=response.reasoning, original_text=text)

        return response

    def check(self, text: str) -> bool:
        """
        Quick boolean check if text passes guardrails.

        Args:
            text: The user's request to evaluate

        Returns:
            True if request passes, False if blocked

        Example:
            >>> g = GuardRailz(expertise="Cooking")
            >>> if g.check("How do I bake cookies?"):
            ...     print("Safe question!")
        """
        try:
            response = self.judge(text)
            return response.answer
        except BlockedException:
            return False

    def raise_for_guardrail(self):
        """
        Enable exception-based mode.

        After calling this, judge() will raise BlockedException
        when requests are blocked instead of returning a response.

        Returns:
            self (for method chaining)

        Example:
            >>> g = GuardRailz()
            >>> g.raise_for_guardrail()
            >>> try:
            ...     response = g.judge("malicious request")
            ... except BlockedException as e:
            ...     print(f"Blocked: {e.reasoning}")
        """
        self.raise_on_block = True
        return self

    # Alias for the exception class (accessible as GuardRailz.BlockedException)
    BlockedException = BlockedException
