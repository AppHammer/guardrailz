# Important: GitHub Installation Setup

## Before Users Can Install from GitHub

For users to install your package from GitHub using:
```bash
pip install git+https://github.com/Apphammer/guardrailz.git
```

You need to **commit and push all package files to GitHub first**:

```bash
# Add all package files
git add pyproject.toml MANIFEST.in
git add __init__.py cli.py config.py core.py exceptions.py signatures.py
git add requirements.txt README.md LICENSE
git add testdata/ examples/

# Commit
git commit -m "Add package configuration for pip installation"

# Push to GitHub
git push origin main
```

## Why This Matters

When pip installs from GitHub, it:
1. Clones your git repository
2. Looks for `pyproject.toml` or `setup.py`
3. Builds and installs the package

If `pyproject.toml` isn't committed, the installation will fail with:
```
ERROR: does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found
```

## Verification

After pushing to GitHub, test the installation:

```bash
# Uninstall local version
pip uninstall guardrailz -y

# Install from GitHub
pip install git+https://github.com/Apphammer/guardrailz.git

# Verify
python -c "import guardrailz; print(guardrailz.__version__)"
```

## Quick Checklist

- [ ] `pyproject.toml` committed and pushed
- [ ] All `.py` files committed and pushed
- [ ] `README.md`, `LICENSE` committed
- [ ] Pushed to GitHub
- [ ] Tested installation from GitHub

Once these steps are complete, users can install directly from your GitHub repository!
