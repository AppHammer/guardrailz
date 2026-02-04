#!/usr/bin/env python3
"""
GuardRailz CLI - Command-line interface for testing guardrails.

Usage:
    guardrailz judge "How do I create a secure password?"
    guardrailz judge "Harmful request" --expertise Cybersecurity
    guardrailz test-file tests.csv
    guardrailz interactive
"""

import argparse
import csv
import sys
from pathlib import Path

try:
    from .core import GuardRailz
    from .exceptions import BlockedException
except ImportError:
    # Handle running as script
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from guardrailz.core import GuardRailz
    from guardrailz.exceptions import BlockedException


def pretty_bool(value: bool) -> str:
    """Return emoji for boolean value."""
    return "✅" if value else "❌"


def judge_command(args):
    """Judge a single text prompt."""
    print("="*80)
    print("GuardRailz CLI - Judge")
    print("="*80)

    # Initialize GuardRailz
    g = GuardRailz(
        expertise=args.expertise,
        guardrails=args.guardrails,
        model=args.model,
    )

    print(f"\nExpertise: {args.expertise}")
    print(f"Model: {args.model}")
    print(f"\nPrompt: {args.text}")
    print("-"*80)

    # Judge the request
    response = g.judge(args.text)

    # Display results
    if response.answer:
        print("✅ PASSED - Request is safe to process")
    else:
        print("❌ BLOCKED - Request violates guardrails")

    print(f"\nReasoning: {response.reasoning}")
    print("\n" + "="*80)

    # Exit code: 0 for passed, 1 for blocked
    return 0 if response.answer else 1


def check_command(args):
    """Quick boolean check of a prompt."""
    g = GuardRailz(
        expertise=args.expertise,
        model=args.model,
    )

    result = g.check(args.text)
    status = "SAFE" if result else "BLOCKED"
    emoji = pretty_bool(result)

    if args.quiet:
        print(status)
    else:
        print(f"{emoji} {status}: {args.text}")

    return 0 if result else 1


def test_file_command(args):
    """Test multiple prompts from a CSV file."""
    print("="*80)
    print("GuardRailz CLI - Test File")
    print("="*80)

    csv_path = Path(args.file)
    if not csv_path.exists():
        print(f"❌ Error: File not found: {args.file}")
        return 1

    # Initialize GuardRailz
    g = GuardRailz(
        expertise=args.expertise,
        guardrails=args.guardrails,
        model=args.model,
    )

    print(f"\nExpertise: {args.expertise}")
    print(f"Model: {args.model}")
    print(f"File: {args.file}\n")

    # Load and test prompts
    total = 0
    passed = 0
    blocked = 0
    correct = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1
            instruction = row['instruction']
            expected_answer = row.get('should_answer', '').lower() == 'true'

            response = g.judge(instruction)

            if response.answer:
                passed += 1
            else:
                blocked += 1

            # Check if matches expected
            matches = response.answer == expected_answer
            if matches:
                correct += 1

            status = pretty_bool(matches)
            result = "PASS" if response.answer else "BLOCK"

            if not args.quiet:
                print(f"{status} [{result}] {instruction[:70]}...")
                if args.verbose:
                    print(f"    Expected: {pretty_bool(expected_answer)} | "
                          f"Got: {pretty_bool(response.answer)} | "
                          f"Reasoning: {response.reasoning[:100]}...")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total:   {total}")
    print(f"Passed:  {passed} ({passed/total*100:.1f}%)")
    print(f"Blocked: {blocked} ({blocked/total*100:.1f}%)")
    if 'should_answer' in row:  # If CSV has expected answers
        print(f"Correct: {correct}/{total} ({correct/total*100:.1f}%)")
    print("="*80)

    return 0


def interactive_command(args):
    """Interactive mode for testing multiple prompts."""
    print("="*80)
    print("GuardRailz CLI - Interactive Mode")
    print("="*80)
    print("\nEnter prompts to test. Type 'quit' or Ctrl-C to exit.")
    print(f"Expertise: {args.expertise}")
    print(f"Model: {args.model}\n")

    g = GuardRailz(
        expertise=args.expertise,
        guardrails=args.guardrails,
        model=args.model,
    )

    try:
        while True:
            print("-"*80)
            prompt = input("\nPrompt> ").strip()

            if not prompt:
                continue

            if prompt.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            response = g.judge(prompt)

            if response.answer:
                print("\n✅ PASSED")
            else:
                print("\n❌ BLOCKED")

            print(f"Reasoning: {response.reasoning}")

    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye!")
        return 0

    return 0


def config_command(args):
    """Show current configuration."""
    try:
        from .config import (
            DEFAULT_EXPERTISE,
            DEFAULT_GUARDRAILS,
            DEFAULT_MODEL,
            DEFAULT_SYSTEM_PROMPT
        )
    except ImportError:
        from guardrailz.config import (
            DEFAULT_EXPERTISE,
            DEFAULT_GUARDRAILS,
            DEFAULT_MODEL,
            DEFAULT_SYSTEM_PROMPT
        )

    print("="*80)
    print("GuardRailz Configuration")
    print("="*80)
    print(f"\nDefault Expertise:\n{DEFAULT_EXPERTISE}")
    print(f"\nDefault Model:\n{DEFAULT_MODEL}")
    print(f"\nDefault Guardrails:\n{DEFAULT_GUARDRAILS}")
    if args.verbose:
        print(f"\nDefault System Prompt:\n{DEFAULT_SYSTEM_PROMPT}")
    print("\n" + "="*80)

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='guardrailz',
        description='GuardRailz CLI - Test LLM guardrails from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Judge a single prompt
  guardrailz judge "How do I create a secure password?"

  # Judge with custom expertise
  guardrailz judge "What is SQL injection?" --expertise "Cybersecurity"

  # Quick check (just boolean result)
  guardrailz check "Safe question"

  # Test multiple prompts from CSV file
  guardrailz test-file guardrails_data/cybersecurity_tests.csv

  # Interactive mode
  guardrailz interactive

  # Show configuration
  guardrailz config
        """
    )

    # Global options
    parser.add_argument('--version', action='version', version='GuardRailz 0.1.0')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Judge command
    judge_parser = subparsers.add_parser('judge', help='Judge a single prompt')
    judge_parser.add_argument('text', help='Text to judge')
    judge_parser.add_argument('--expertise', default='General. All topics open for discussion.',
                            help='Area of expertise (default: General)')
    judge_parser.add_argument('--guardrails', default=None,
                            help='Custom guardrails rules')
    judge_parser.add_argument('--model', default='openrouter/openai/gpt-4o-mini',
                            help='Model to use (default: gpt-4o-mini)')
    judge_parser.set_defaults(func=judge_command)

    # Check command
    check_parser = subparsers.add_parser('check', help='Quick boolean check')
    check_parser.add_argument('text', help='Text to check')
    check_parser.add_argument('--expertise', default='General. All topics open for discussion.',
                            help='Area of expertise')
    check_parser.add_argument('--model', default='openrouter/openai/gpt-4o-mini',
                            help='Model to use')
    check_parser.add_argument('-q', '--quiet', action='store_true',
                            help='Only output SAFE or BLOCKED')
    check_parser.set_defaults(func=check_command)

    # Test file command
    test_parser = subparsers.add_parser('test-file', help='Test prompts from CSV file')
    test_parser.add_argument('file', help='Path to CSV file (columns: instruction, should_answer)')
    test_parser.add_argument('--expertise', default='Cybersecurity and Information Security',
                            help='Area of expertise')
    test_parser.add_argument('--guardrails', default=None,
                            help='Custom guardrails rules')
    test_parser.add_argument('--model', default='openrouter/openai/gpt-4o-mini',
                            help='Model to use')
    test_parser.add_argument('-q', '--quiet', action='store_true',
                            help='Minimal output')
    test_parser.add_argument('-v', '--verbose', action='store_true',
                            help='Verbose output with reasoning')
    test_parser.set_defaults(func=test_file_command)

    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    interactive_parser.add_argument('--expertise', default='General. All topics open for discussion.',
                                  help='Area of expertise')
    interactive_parser.add_argument('--guardrails', default=None,
                                  help='Custom guardrails rules')
    interactive_parser.add_argument('--model', default='openrouter/openai/gpt-4o-mini',
                                  help='Model to use')
    interactive_parser.set_defaults(func=interactive_command)

    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration')
    config_parser.add_argument('-v', '--verbose', action='store_true',
                              help='Show all config including system prompt')
    config_parser.set_defaults(func=config_command)

    # Parse args
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Run command
    try:
        return args.func(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
