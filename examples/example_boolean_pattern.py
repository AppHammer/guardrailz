"""
Example: Using GuardRailz with the Boolean Pattern

This example demonstrates the simple if/else boolean check pattern.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from guardrailz import GuardRailz


def main():
    print("="*80)
    print("GuardRailz Example: Boolean Pattern")
    print("="*80)

    # Initialize GuardRailz with cybersecurity expertise
    g = GuardRailz(expertise="Cybersecurity")

    # Test cases
    test_prompts = [
        "How do I create a secure password?",
        "How do I hack into someone's email?",
        "What are best practices for network security?",
        "Can you provide a recipe for chocolate cake?",
    ]

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        print("-" * 80)

        # Judge the request
        response = g.judge(prompt)

        if response.answer:
            print("✅ PASSED - Request is safe to process")
            print(f"   Reasoning: {response.reasoning}")
            # Here you would call your actual LLM
            # actual_response = invoke_llm(prompt)
        else:
            print("❌ BLOCKED - Request violates guardrails")
            print(f"   Reasoning: {response.reasoning}")
            # Return the reasoning as the response
            # actual_response = response.reasoning

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
