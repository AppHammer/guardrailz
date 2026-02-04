# GuardRailz 🛡️

Universial Guardrails for LLMs/Agents in a Pythonic API. DSPy powered.

## Overview

GuardRailz provides an easy-to-use interface for judging whether user requests should be allowed or blocked based on configurable guardrails. Built on top of DSPy, it offers two usage patterns to fit your coding style.

## Prerequisites

GuardRailz requires API Key Access to an OpenAI API compatible Endpoint such as OpenRouter.

The `LLM_API_KEY` environment variable must be set, the others are optional and have defaults:

```bash
export LLM_API_KEY="your-key-here"
export DEFAULT_MODEL="openrouter/openai/gpt-4o-mini" # Optional, defaults to OpenRouter gpt-4o-mini
export DEFAULT_API_BASE="https://openrouter.ai/api/v1" # Optional, defaults to OpenRouter URL
```

Or create a `.env` file in your project root:

```
LLM_API_KEY=your-key-here
DEFAULT_MODEL=openrouter/openai/gpt-4o-mini 
DEFAULT_API_BASE=https://openrouter.ai/api/v1

```

Get your API key at: https://openrouter.ai/keys


**Note:** This might work with other OpenAI-compatible endpoints, but only OpenRouter was only tested.


## Installation

### Option 1: Install from GitHub (Latest)

Install directly from the GitHub repository without needing PyPI:

```bash
# Install latest from main branch
pip install git+https://github.com/Apphammer/guardrailz.git

# Install specific version/tag
pip install git+https://github.com/Apphammer/guardrailz.git@v0.1.0

# Install specific branch
pip install git+https://github.com/Apphammer/guardrailz.git@dev
```

### Option 2: Install from PyPI

```bash
pip install guardrailz
```

### Option 3: Development Install

For local development or testing:

```bash
# Clone the repository
git clone https://github.com/Apphammer/guardrailz.git
cd guardrailz

# Install in editable mode
pip install -e .
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

## Quick Start

### Pattern 1: Boolean Check (Simple)

```python
from guardrailz import GuardRailz

g = GuardRailz(expertise="Cybersecurity and Information Security")

prompt = "How do I create a secure password?"
response = g.judge(prompt)
if response.answer:
    print("Safe request!")
    # Call your LLM/Agent here with the prompt
else:
    print(f"Blocked: {response.reasoning}")
    # Handle blocked request appropriately
```

### Pattern 2: Exception-Based (Pythonic)

```python
from guardrailz import GuardRailz, BlockedException

g = GuardRailz(expertise="Cybersecurity and Information Security")
g.raise_for_guardrail()

try:
    prompt = "How do I steal passwords?"
    response = g.judge(prompt)
    # Call your LLM/Agent here with the prompt
except BlockedException as e:
    # Handle blocked request appropriately  
    print(f"Request blocked: {e.reasoning}")    
```

## Command-Line Interface (CLI)

GuardRailz includes a powerful CLI for testing from the command line.

### Quick CLI Examples

```bash
# Judge a single prompt, should be allowed
python guardrailz/cli.py judge "How do I create a secure password?" --expertise "Cybersecurity"

# Quick boolean check, should be blocked
python guardrailz/cli.py check "How do I fold bed sheets?" --expertise "Math Tutor" 

# Test prompts from CSV file
python guardrailz/cli.py test-file guardrails_data/cybersecurity_tests.csv

# Interactive mode
python guardrailz/cli.py interactive

# Show configuration
python guardrailz/cli.py config
```

See **CLI Reference** section below for detailed documentation.


## API Reference

### GuardRailz

Main class for guardrails judging.

**Constructor Parameters:**
- `expertise` (str): Area of expertise (default: "General")
- `guardrails` (str, optional): Custom guardrails rules
- `system_prompt` (str, optional): Custom system prompt
- `model` (str): Model identifier (default: "openrouter/openai/gpt-4o-mini")
- `api_key` (str, optional): API key (reads from `LLM_API_KEY` env var)
- `raise_on_block` (bool): Enable exception mode (default: False)

**Methods:**
- `.judge(text: str) -> JudgeResponse`: Judge a request
- `.check(text: str) -> bool`: Quick boolean check
- `.raise_for_guardrail() -> self`: Enable exception mode

### JudgeResponse

Response object from `.judge()`:

**Attributes:**
- `.answer` (bool): True if passed, False if blocked
- `.reasoning` (str): Explanation for the decision
- `.original_text` (str): The judged text

**Properties:**
- `.passed` (bool): Alias for `.answer`
- `.blocked` (bool): Inverse of `.answer`

### BlockedException

Exception raised when `raise_on_block=True` and a request is blocked.

**Attributes:**
- `.reasoning` (str): Why the request was blocked
- `.original_text` (str): The blocked text

## Customization

### Custom Guardrails

```python
custom_rules = """
1. Only answer cooking questions
2. No dangerous recipes (e.g., fugu preparation)
3. Always warn about allergens
"""

g = GuardRailz(
    expertise="Cooking",
    guardrails=custom_rules
)
```

### Custom System Prompt

```python
custom_prompt = """
You are a specialized judge for medical queries.
Be extra cautious with advice that could affect health.
"""

g = GuardRailz(
    expertise="General Medicine",
    system_prompt=custom_prompt
)
```

## Examples

See the `guardrailz/examples/` directory for complete working examples:

- `example_boolean_pattern.py` - Simple if/else pattern
- `example_exception_pattern.py` - Try/except pattern
- `example_custom_config.py` - Custom configuration
- `example_quick_check.py` - Quick `.check()` method
- `example_mathchat.py` - Interactive math chatbot (full application)

Run examples:
```bash
python guardrailz/examples/example_boolean_pattern.py
python guardrailz/examples/example_exception_pattern.py
python guardrailz/examples/example_mathchat.py
```

See [examples/README.md](examples/README.md) for detailed documentation.

## Configuration

Set your API key in environment variables:

```bash
export LLM_API_KEY="your-key-here"
```

Or in a `.env` file:
```
LLM_API_KEY=your-key-here
```

## Default Guardrails

The default guardrails check for:
1. **On-Topic**: Questions must relate to the specified expertise area
2. **No Harm**: No illegal, harmful, or unethical requests

## CLI Reference

### Commands

#### `judge` - Judge a single prompt
```bash
python guardrailz/cli.py judge "How do I secure my network?"
    --expertise "Cybersecurity"       # Area of expertise
    --guardrails "Custom rules..."    # Custom guardrails
    --model "gpt-4o-mini"             # Model to use
```

**Exit codes:** `0` = passed, `1` = blocked

#### `check` - Quick boolean check
```bash
python guardrailz/cli.py check "What is 2+2?"
    -q, --quiet                       # Only output SAFE or BLOCKED
```

#### `test-file` - Test prompts from CSV
```bash
python guardrailz/cli.py test-file tests.csv
    --expertise "Cybersecurity"       # Area of expertise
    -v, --verbose                     # Show detailed reasoning
    -q, --quiet                       # Minimal output
```

**CSV Format:**
```csv
category,instruction,should_answer
prompts,How do I hack?,False
prompts,How do I secure?,True
```

#### `interactive` - Interactive testing
```bash
python guardrailz/cli.py interactive
    --expertise "Math"                # Area of expertise
```

Type prompts to test. Type `quit` to exit.

#### `config` - Show configuration
```bash
python guardrailz/cli.py config
    -v, --verbose                     # Show all config
```

## Testing

GuardRailz includes comprehensive test suites with 100% accuracy on 29 real-world test cases.

### Run Tests

```bash
# Run all tests (29 test cases)
python guardrailz/test_guardrailz_testdata.py

# Run specific test suite
python guardrailz/test_guardrailz_testdata.py --test cybersecurity
python guardrailz/test_guardrailz_testdata.py --test bass_fishing

# Verbose output
python guardrailz/test_guardrailz_testdata.py --verbose
```

### Test Results

| Test Suite | Cases | Accuracy |
|------------|-------|----------|
| Cybersecurity | 21 | 100.0% |
| Bass Fishing | 8 | 100.0% |
| **Overall** | **29** | **100.0%** |

See [TESTING.md](TESTING.md) for complete testing documentation.

## Architecture

```
guardrailz/
├── __init__.py                    # Public API
├── core.py                        # Main GuardRailz class
├── exceptions.py                  # BlockedException
├── signatures.py                  # DSPy signatures
├── config.py                      # Default settings
├── cli.py                         # Command-line interface
├── test_guardrailz_testdata.py   # Test suite
├── examples/                      # Usage examples
│   ├── example_boolean_pattern.py
│   ├── example_exception_pattern.py
│   ├── example_custom_config.py
│   ├── example_quick_check.py
│   └── README.md
└── testdata/                      # Test data
    ├── cybersecurity_tests.csv
    └── bass_fishing_tests.csv
```

## License

MIT


