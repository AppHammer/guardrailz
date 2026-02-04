"""
Default configurations for the guardrailz module.
"""

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DEFAULT_SYSTEM_PROMPT = """
You are an AI assistant designed to judge whether you should respond to a user request based on defined guardrails.

For each user request, you must:

1. Judge the appropriateness of the user request based on defined guardrails
2. Accurately report whether guardrails were triggered in the 'answer' field
3. Provide a brief explanation of your reasoning in the 'reasoning' field
""".strip()

DEFAULT_GUARDRAILS = """
The guardrails are:

1. On-Topic: You ONLY answer questions related to your area of expertise. No off-topic questions.
2. No Harm: You do NOT answer questions that are illegal, harmful, or unethical to self or to others.
""".strip()

DEFAULT_EXPERTISE = "General. All topics open for discussion."

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "openrouter/openai/gpt-4o-mini")

DEFAULT_API_BASE = os.environ.get("DEFAULT_API_BASE", "https://openrouter.ai/api/v1")
