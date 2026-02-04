# GuardRailz Installation Guide

Complete installation instructions for GuardRailz.

## Table of Contents
- [Quick Install](#quick-install)
- [Installation Methods](#installation-methods)
- [Requirements](#requirements)
- [Virtual Environments](#virtual-environments)
- [Using in Projects](#using-in-projects)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

## Quick Install

```bash
# From GitHub (recommended for latest features)
pip install git+https://github.com/Apphammer/guardrailz.git

# From PyPI (once published)
pip install guardrailz
```

## Installation Methods

### Method 1: Install from GitHub

**Best for:** Getting the latest version, testing pre-release features, or when PyPI package is not yet available.

```bash
# Install from main branch (latest stable)
pip install git+https://github.com/Apphammer/guardrailz.git

# Install specific version tag
pip install git+https://github.com/Apphammer/guardrailz.git@v0.1.0

# Install from development branch
pip install git+https://github.com/Apphammer/guardrailz.git@dev

# Install specific commit
pip install git+https://github.com/Apphammer/guardrailz.git@abc1234
```

**Upgrade from GitHub:**
```bash
pip install --upgrade git+https://github.com/Apphammer/guardrailz.git
```

### Method 2: Install from PyPI

**Best for:** Production use, stable releases.

```bash
# Install latest version
pip install guardrailz

# Install specific version
pip install guardrailz==0.1.0

# Upgrade to latest
pip install --upgrade guardrailz
```

### Method 3: Local Development Install

**Best for:** Contributors, local development, testing changes.

```bash
# Clone the repository
git clone https://github.com/Apphammer/guardrailz.git
cd guardrailz

# Install in editable mode
pip install -e .
```

**Editable mode benefits:**
- Changes to code take effect immediately
- No need to reinstall after editing
- Perfect for development and testing

**Update your local install:**
```bash
cd guardrailz
git pull origin main
# No reinstall needed in editable mode
```

## Requirements

### System Requirements
- Python 3.8 or higher
- pip (latest version recommended)
- Git (for GitHub installation)

### Dependencies

GuardRailz automatically installs these dependencies:
- `dspy-ai` - DSPy framework for LLM orchestration
- `python-dotenv` - Environment variable management

### API Requirements

GuardRailz requires access to an OpenAI-compatible API endpoint:

```bash
# Required environment variable
export LLM_API_KEY="your-api-key"

# Optional (defaults provided)
export DEFAULT_MODEL="openrouter/openai/gpt-4o-mini"
export DEFAULT_API_BASE="https://openrouter.ai/api/v1"
```

Get an API key at: https://openrouter.ai/keys

## Virtual Environments

### Why Use Virtual Environments?

Virtual environments isolate your project dependencies and prevent conflicts. Always recommended!

### Using venv (Built-in)

```bash
# Create virtual environment
python -m venv guardrailz-env

# Activate (Linux/Mac)
source guardrailz-env/bin/activate

# Activate (Windows)
guardrailz-env\Scripts\activate

# Install GuardRailz
pip install git+https://github.com/Apphammer/guardrailz.git

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create environment
conda create -n guardrailz python=3.11

# Activate
conda activate guardrailz

# Install GuardRailz
pip install git+https://github.com/Apphammer/guardrailz.git

# Deactivate
conda deactivate
```

## Using in Projects

### In requirements.txt

```txt
# From GitHub (latest)
git+https://github.com/Apphammer/guardrailz.git

# From GitHub (specific version)
git+https://github.com/Apphammer/guardrailz.git@v0.1.0

# From PyPI (once published)
guardrailz==0.1.0
```

Then install:
```bash
pip install -r requirements.txt
```

### In pyproject.toml

```toml
[project]
dependencies = [
    "guardrailz @ git+https://github.com/Apphammer/guardrailz.git",
    # or
    "guardrailz==0.1.0",  # from PyPI
]
```

### In setup.py

```python
setup(
    name="your-project",
    install_requires=[
        "guardrailz @ git+https://github.com/Apphammer/guardrailz.git",
    ],
)
```

## Verification

After installation, verify everything works:

### Check Installation

```bash
# Check if package is installed
pip list | grep guardrailz

# Show package details
pip show guardrailz
```

### Test Import

```bash
# Test basic import
python -c "import guardrailz; print(f'GuardRailz v{guardrailz.__version__} installed')"

# Test all exports
python -c "from guardrailz import GuardRailz, BlockedException, JudgeResponse; print('All imports successful')"
```

### Test CLI (if using development install)

```bash
# Check CLI is available
guardrailz --help

# Or run directly
python -m guardrailz --help
```

### Run Examples

```bash
# Clone repo if needed
git clone https://github.com/Apphammer/guardrailz.git
cd guardrailz

# Set API key
export LLM_API_KEY="your-key"

# Run example
python examples/example_boolean_pattern.py
```

## Troubleshooting

### "No module named 'guardrailz'"

**Cause:** Package not installed or wrong Python environment

**Solution:**
```bash
# Check if installed
pip list | grep guardrailz

# Install if missing
pip install git+https://github.com/Apphammer/guardrailz.git

# Check Python version
python --version  # Should be 3.8+
```

### "ERROR: Could not find a version that satisfies the requirement"

**Cause:** Network issues or incorrect package name

**Solution:**
```bash
# Check internet connection
ping github.com

# Try with verbose output
pip install -v git+https://github.com/Apphammer/guardrailz.git

# Ensure Git is installed
git --version
```

### "Permission denied" errors

**Cause:** Installing to system Python without sudo

**Solution:**
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/Apphammer/guardrailz.git

# Or use --user flag (not recommended)
pip install --user git+https://github.com/Apphammer/guardrailz.git
```

### Dependencies conflict

**Cause:** Version conflicts with existing packages

**Solution:**
```bash
# Create fresh virtual environment
python -m venv fresh-env
source fresh-env/bin/activate
pip install git+https://github.com/Apphammer/guardrailz.git
```

### "Command 'guardrailz' not found" (after editable install)

**Cause:** CLI entry point not configured or PATH issue

**Solution:**
```bash
# Use Python module syntax instead
python -m cli

# Or call directly
python cli.py

# Reinstall package
pip install -e .
```

### Import works but no LLM_API_KEY

**Cause:** Environment variable not set

**Solution:**
```bash
# Set temporarily
export LLM_API_KEY="your-key"

# Or create .env file
echo "LLM_API_KEY=your-key" > .env

# Or set in Python
import os
os.environ['LLM_API_KEY'] = 'your-key'
```

### SSL Certificate errors

**Cause:** Corporate proxy or certificate issues

**Solution:**
```bash
# Install from GitHub with no SSL verification (not recommended)
pip install --trusted-host github.com git+https://github.com/Apphammer/guardrailz.git

# Better: Fix your SSL certificates
pip install --upgrade certifi
```

## Uninstallation

```bash
# Uninstall package
pip uninstall guardrailz

# Confirm
y

# Verify removal
pip list | grep guardrailz
```

**Clean up development install:**
```bash
# Uninstall
pip uninstall guardrailz

# Remove cloned repository
rm -rf guardrailz/

# Remove virtual environment if you created one
rm -rf guardrailz-env/
```

## Getting Help

If you encounter issues:

1. **Check the documentation**: [README.md](README.md)
2. **Search existing issues**: https://github.com/Apphammer/guardrailz/issues
3. **Create a new issue**: Include:
   - Python version: `python --version`
   - pip version: `pip --version`
   - OS: `uname -a` (Linux/Mac) or `ver` (Windows)
   - Full error message
   - Installation method used

## Additional Resources

- **README**: [README.md](README.md)
- **Examples**: [examples/](examples/)
- **Testing Guide**: [TESTING.md](TESTING.md)
- **PyPI Deployment**: [PYPI_DEPLOYMENT.md](PYPI_DEPLOYMENT.md)
- **Repository**: https://github.com/Apphammer/guardrailz
