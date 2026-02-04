# GuardRailz Examples

This directory contains example scripts demonstrating different usage patterns for GuardRailz.

## Running Examples

All examples can be run directly from the repository root:

```bash
python guardrailz/examples/example_boolean_pattern.py
python guardrailz/examples/example_exception_pattern.py
python guardrailz/examples/example_custom_config.py
python guardrailz/examples/example_quick_check.py
python guardrailz/examples/example_mathchat.py
```

## Examples Overview

### 1. Boolean Pattern (`example_boolean_pattern.py`)

Demonstrates the simple if/else boolean check pattern.

**Key concepts:**
- Initialize GuardRailz with expertise
- Call `.judge()` to evaluate prompts
- Check `response.answer` for pass/fail
- Use `response.reasoning` for explanation

**Example output:**
```
✅ PASSED - Request is safe to process
   Reasoning: The request pertains to creating a secure password...

❌ BLOCKED - Request violates guardrails
   Reasoning: The request is seeking guidance on illegal activity...
```

**Use case:** Simple conditional logic based on guardrails check.

### 2. Exception Pattern (`example_exception_pattern.py`)

Demonstrates the try/except exception-based pattern.

**Key concepts:**
- Call `.raise_for_guardrail()` to enable exception mode
- Use try/except to catch `BlockedException`
- Access `exception.reasoning` for block explanation

**Example output:**
```
✅ PASSED - Request is safe to process
   Reasoning: The request is on-topic and safe...

❌ BLOCKED - Request violates guardrails
   Reasoning: Harmful request detected...
```

**Use case:** Pythonic error handling with exceptions.

### 3. Custom Configuration (`example_custom_config.py`)

Shows how to customize guardrails, expertise, and settings.

**Key concepts:**
- Custom `guardrails` parameter
- Custom `expertise` area
- Model selection
- Specialized domain configuration

**Example:**
```python
custom_guardrails = """
1. Only Cooking: ONLY answer questions about cooking
2. Safety First: NOT dangerous food preparation
3. No Allergens Without Warning: Always warn about allergens
"""

g = GuardRailz(
    expertise="Cooking and Culinary Arts",
    guardrails=custom_guardrails,
    model="openrouter/openai/gpt-4o-mini"
)
```

**Use case:** Domain-specific guardrails (cooking, math, medicine, etc.)

### 4. Quick Check (`example_quick_check.py`)

Demonstrates the `.check()` method for quick boolean results.

**Key concepts:**
- Use `.check()` for simple True/False
- No detailed reasoning returned
- Fastest way to validate prompts

**Example:**
```python
g = GuardRailz(expertise="Mathematics")

if g.check("What is 2+2?"):
    print("✅ SAFE")
else:
    print("❌ BLOCKED")
```

**Use case:** Fast validation without needing detailed reasoning.

### 5. MathChat - Interactive Chatbot (`example_mathchat.py`)

Demonstrates a complete interactive chatbot application with topic restrictions.

**Key concepts:**
- Command-line interactive chat interface
- Mathematics-only topic enforcement
- Chat history management
- DSPy integration for LLM responses
- Real-world application pattern

**Features:**
```
- Interactive chat loop
- Guardrails check before each LLM call
- Commands: history, clear, quit
- Context-aware responses using chat history
- Graceful blocking of off-topic requests
```

**Example session:**
```
You: What is 2+2?
MathBot: The sum of 2 + 2 is 4. [detailed explanation]

You: Can you help me cook pasta?
MathBot: 🚫 I can only help with mathematics topics.
         This request is about cooking, not mathematics.

You: What is the Pythagorean theorem?
MathBot: The Pythagorean theorem states that in a right triangle... [explanation]
```

**Use case:** Building domain-specific chatbots with strict topic boundaries.

## Common Patterns

### Pattern 1: Pre-screening User Input

```python
from guardrailz import GuardRailz

g = GuardRailz(expertise="Your Domain")

def process_user_request(user_input):
    response = g.judge(user_input)

    if response.answer:
        # Safe - proceed with actual LLM call
        return invoke_llm(user_input)
    else:
        # Blocked - return reasoning
        return f"Cannot process: {response.reasoning}"
```

### Pattern 2: Exception-Based Flow Control

```python
from guardrailz import GuardRailz, BlockedException

g = GuardRailz(expertise="Your Domain")
g.raise_for_guardrail()

def safe_llm_call(user_input):
    try:
        response = g.judge(user_input)
        return invoke_llm(user_input)
    except BlockedException as e:
        log_blocked_request(user_input, e.reasoning)
        return "Request blocked by safety guardrails"
```

### Pattern 3: Batch Processing

```python
from guardrailz import GuardRailz

g = GuardRailz(expertise="Your Domain")

def process_batch(prompts):
    results = []
    for prompt in prompts:
        response = g.judge(prompt)
        results.append({
            'prompt': prompt,
            'safe': response.answer,
            'reasoning': response.reasoning
        })
    return results
```

### Pattern 4: Domain-Specific Assistant

```python
from guardrailz import GuardRailz

# Medical assistant with strict guardrails
medical_guardrails = """
1. Medical Topics Only: ONLY answer questions about general health information
2. No Diagnosis: Do NOT provide medical diagnoses
3. No Prescriptions: Do NOT recommend specific medications
4. Professional Referral: Always suggest consulting healthcare professionals
"""

g = GuardRailz(
    expertise="General Health Information",
    guardrails=medical_guardrails
)

def medical_assistant(question):
    response = g.judge(question)

    if response.answer:
        return get_health_info(question)
    else:
        return "Please consult a healthcare professional"
```

## Customization Examples

### Example 1: Multiple Expertise Areas

```python
# Create different instances for different domains
cyber_guard = GuardRailz(expertise="Cybersecurity")
math_guard = GuardRailz(expertise="Mathematics")
cooking_guard = GuardRailz(expertise="Cooking")

# Use appropriate guard based on context
def route_question(question, domain):
    guards = {
        'cyber': cyber_guard,
        'math': math_guard,
        'cooking': cooking_guard
    }

    guard = guards.get(domain)
    if guard:
        return guard.judge(question)
    else:
        return "Unknown domain"
```

### Example 2: Logging and Monitoring

```python
from guardrailz import GuardRailz
import logging

g = GuardRailz(expertise="Your Domain")

def monitored_judge(prompt):
    response = g.judge(prompt)

    # Log all requests
    logging.info(f"Prompt: {prompt[:50]}...")
    logging.info(f"Result: {'PASS' if response.answer else 'BLOCK'}")
    logging.info(f"Reasoning: {response.reasoning}")

    # Track metrics
    if response.blocked:
        increment_blocked_counter()

    return response
```

### Example 3: Caching Results

```python
from guardrailz import GuardRailz
from functools import lru_cache

g = GuardRailz(expertise="Your Domain")

@lru_cache(maxsize=1000)
def cached_judge(prompt):
    response = g.judge(prompt)
    return response.answer, response.reasoning

# Repeated prompts will use cached results
result = cached_judge("Common question")
```

## Testing Your Configuration

Use the CLI to quickly test your configuration:

```bash
# Test individual prompts
python guardrailz/cli.py judge "Your prompt" --expertise "Your Domain"

# Test from CSV file
python guardrailz/cli.py test-file your_tests.csv --expertise "Your Domain"

# Interactive testing
python guardrailz/cli.py interactive --expertise "Your Domain"
```

## Next Steps

1. **Read the main README:** `guardrailz/README.md`
2. **Try the CLI:** `python guardrailz/cli.py --help`
3. **Run the tests:** `python guardrailz/test_guardrailz_testdata.py`
4. **Customize for your domain:** Copy an example and modify it

## Environment Setup

Make sure your API key is set:

```bash
export LLM_API_KEY="your-key-here"
```

Or create a `.env` file:
```
LLM_API_KEY=your-key-here
```

## Questions?

- Check the main documentation: `guardrailz/README.md`
- CLI guide: `CLI_GUIDE.md`
- Testing guide: `guardrailz/TESTING.md`
