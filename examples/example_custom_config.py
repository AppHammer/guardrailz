"""
Example: Using GuardRailz with Custom Configuration

This example shows how to customize guardrails, expertise, and system prompts.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from guardrailz import GuardRailz


def main():
    print("="*80)
    print("GuardRailz Example: Custom Configuration")
    print("="*80)

    # Custom guardrails for a cooking assistant
    custom_guardrails = """
    The guardrails are:

    1. Only Cooking: You ONLY answer questions about cooking, recipes, and food preparation
    2. Safety First: You do NOT provide instructions for dangerous food preparation (e.g., fugu, raw chicken)
    3. No Allergens Without Warning: Always warn about common allergens
    """

    # Initialize with custom configuration
    g = GuardRailz(
        expertise="Cooking and Culinary Arts",
        guardrails=custom_guardrails,
        model="openrouter/openai/gpt-4o-mini"
    )

    # Test cases
    test_prompts = [
        "How do I make chocolate chip cookies?",
        "What's the recipe for homemade pasta?",
        "How do I prepare fugu (pufferfish)?",
        "Can you help me with my math homework?",
    ]

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        print("-" * 80)

        response = g.judge(prompt)

        if response.passed:
            print("✅ PASSED")
        else:
            print("❌ BLOCKED")

        print(f"   Reasoning: {response.reasoning}")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
