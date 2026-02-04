"""
Example: Using GuardRailz Quick Check Method

This example demonstrates the .check() method for quick boolean results.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from guardrailz import GuardRailz


def main():
    print("="*80)
    print("GuardRailz Example: Quick Check Method")
    print("="*80)

    g = GuardRailz(expertise="Mathematics")

    # Test cases
    test_prompts = [
        "What is 2+2?",
        "How do I solve quadratic equations?",
        "Can you write an essay about history?",
        "Explain how to calculate derivatives",
    ]

    for prompt in test_prompts:
        # Quick boolean check
        is_safe = g.check(prompt)

        status = "✅ SAFE" if is_safe else "❌ BLOCKED"
        print(f"{status} | {prompt}")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
