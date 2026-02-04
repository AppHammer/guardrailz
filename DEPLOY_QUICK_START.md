# Quick Start: Deploy to PyPI

## Note: Users Can Install from GitHub Now!

Your package is already installable from GitHub without PyPI:

```bash
pip install git+https://github.com/Apphammer/guardrailz.git
```

This works immediately and is perfect for beta testers or early adopters. See [INSTALL.md](INSTALL.md) for details.

---

## Prerequisites

```bash
pip install --upgrade pip build twine
```

## Get Your PyPI Token

1. **TestPyPI** (for testing): https://test.pypi.org/manage/account/token/
2. **PyPI** (production): https://pypi.org/manage/account/token/

Save these tokens securely!

## Deploy Steps

### 1. Test on TestPyPI First (Recommended)

```bash
# Clean and build
rm -rf dist/ build/ *.egg-info
python -m build

# Verify
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*
# Username: __token__
# Password: pypi-YOUR_TESTPYPI_TOKEN

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ guardrailz
```

### 2. Deploy to Production PyPI

```bash
# Upload to PyPI
twine upload dist/*
# Username: __token__
# Password: pypi-YOUR_PYPI_TOKEN

# Verify
pip install guardrailz
python -c "import guardrailz; print(guardrailz.__version__)"
```

### 3. Tag the Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

## Before Next Release

1. Update version in [pyproject.toml](pyproject.toml)
2. Run tests: `python test_guardrailz_testdata.py`
3. Update [README.md](README.md) if needed
4. Rebuild: `python -m build`
5. Upload again

## Troubleshooting

**"File already exists"**: Increment version in `pyproject.toml`

**"Invalid auth"**: Use `__token__` as username, not your PyPI username

**README not rendering**: Check with `python -m readme_renderer README.md`

---

For detailed documentation, see [PYPI_DEPLOYMENT.md](PYPI_DEPLOYMENT.md)
