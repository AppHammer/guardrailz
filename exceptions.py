"""
Custom exceptions for the guardrailz module.
"""


class BlockedException(Exception):
    """
    Raised when a request is blocked by guardrails.

    This exception is thrown when raise_on_block is enabled and
    a request fails the guardrails check.

    Attributes:
        reasoning (str): Explanation for why the request was blocked
        original_text (str): The original text that was judged
    """

    def __init__(self, reasoning: str, original_text: str):
        """
        Initialize BlockedException.

        Args:
            reasoning: Explanation for the block decision
            original_text: The text that triggered the block
        """
        self.reasoning = reasoning
        self.original_text = original_text
        super().__init__(reasoning)

    def __str__(self):
        return f"Request blocked: {self.reasoning}"

    def __repr__(self):
        return f"BlockedException(reasoning={self.reasoning!r}, original_text={self.original_text!r})"
