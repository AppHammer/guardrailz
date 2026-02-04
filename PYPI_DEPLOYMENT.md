# PyPI Deployment Guide for GuardRailz

This guide will walk you through deploying GuardRailz to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - TestPyPI (for testing): https://test.pypi.org/account/register/
   - PyPI (for production): https://pypi.org/account/register/

2. **Install Build Tools**:
   ```bash
   pip install --upgrade pip build twine
   ```

3. **API Tokens**: Generate API tokens for authentication:
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

   Store these securely - you'll need them for authentication.

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Update version number in `pyproject.toml` (follow [semantic versioning](https://semver.org/))
- [ ] Update GitHub URL in `pyproject.toml` (replace `yourusername` with actual username)
- [ ] All tests pass: `python test_guardrailz_testdata.py`
- [ ] README.md is up-to-date and properly formatted
- [ ] LICENSE file is present
- [ ] No sensitive information (API keys, secrets) in the code

## Step-by-Step Deployment

### Step 1: Clean Previous Builds

```bash
# Remove any previous build artifacts
rm -rf dist/ build/ *.egg-info
```

### Step 2: Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates two files in the `dist/` directory:
- `guardrailz-X.X.X.tar.gz` (source distribution)
- `guardrailz-X.X.X-py3-none-any.whl` (wheel distribution)

### Step 3: Verify the Build

```bash
# Check the package contents
tar -tzf dist/guardrailz-*.tar.gz

# Verify package metadata
twine check dist/*
```

### Step 4: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

Verify the upload at: https://test.pypi.org/project/guardrailz/

Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ guardrailz
```

Note: `--extra-index-url` is needed because dependencies come from regular PyPI.

### Step 5: Deploy to Production PyPI

Once testing is successful:

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

### Step 6: Verify Production Deployment

Check your package at: https://pypi.org/project/guardrailz/

Test installation:
```bash
pip install guardrailz
```

## Using .pypirc for Authentication (Optional)

To avoid entering credentials each time, create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```

**Security Warning**: Make sure this file has restricted permissions:
```bash
chmod 600 ~/.pypirc
```

## Automated Deployment with GitHub Actions (Recommended)

For automated releases, create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Then add your PyPI API token to GitHub:
1. Go to your repo → Settings → Secrets and variables → Actions
2. Add secret named `PYPI_API_TOKEN` with your PyPI token

## Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Update version in `pyproject.toml`:
```toml
version = "0.1.0"  # Change this for each release
```

## Common Issues

### Issue: "File already exists"
**Solution**: You can't re-upload the same version. Increment the version number in `pyproject.toml`.

### Issue: "Invalid or non-existent authentication"
**Solution**: Ensure you're using `__token__` as username and your API token as password.

### Issue: Dependencies not found when installing from TestPyPI
**Solution**: Use both index URLs:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ guardrailz
```

### Issue: "README rendering failed"
**Solution**: Validate your README with:
```bash
pip install readme-renderer
python -m readme_renderer README.md
```

## Post-Deployment

After successful deployment:

1. **Tag the release in Git**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create GitHub Release**: Go to your repo → Releases → Create new release

3. **Update Documentation**: Update installation instructions in README.md

4. **Monitor**: Check PyPI stats and watch for issues

## Quick Reference Commands

```bash
# Full deployment workflow
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # Test first
twine upload dist/*                         # Production

# Verify
pip install guardrailz
python -c "import guardrailz; print(guardrailz.__version__)"
```

## Resources

- PyPI Documentation: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
- Semantic Versioning: https://semver.org/
- Python Packaging Guide: https://packaging.python.org/tutorials/packaging-projects/
