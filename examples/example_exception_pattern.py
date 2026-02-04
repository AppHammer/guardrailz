"""
Example: Using GuardRailz with the Exception Pattern

This example demonstrates the try/except exception-based pattern.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from guardrailz import GuardRailz, BlockedException


def main():
    print("="*80)
    print("GuardRailz Example: Exception Pattern")
    print("="*80)

    # Initialize GuardRailz and enable exception mode
    g = GuardRailz(expertise="Cybersecurity")
    g.raise_for_guardrail()

    # Test cases
    test_prompts = [
        "How do I create a secure password?",
        "How do I hack into someone's email?",
        "What are best practices for network security?",
    ]

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        print("-" * 80)

        try:
            # Judge the request - will raise exception if blocked
            response = g.judge(prompt)

            # If we reach here, request passed guardrails
            print("✅ PASSED - Request is safe to process")
            print(f"   Reasoning: {response.reasoning}")
            # actual_response = invoke_llm(prompt)

        except BlockedException as e:
            # Request was blocked
            print("❌ BLOCKED - Request violates guardrails")
            print(f"   Reasoning: {e.reasoning}")
            # actual_response = e.reasoning

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
