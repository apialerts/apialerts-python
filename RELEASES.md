# Release Process

## Files to update

1. `apialerts/__init__.py` - update `__version__`
2. `apialerts/network.py` - update `_VERSION` constant (the value sent in the `X-Version` header)
3. `pyproject.toml` - update `version`
4. Confirm constants test still passes (`python -m unittest tests.test_constants`)
5. PR and merge to `main` after tests pass
6. Create a new release on GitHub from `main`
7. GitHub Actions publishes to PyPI via OIDC trusted publishing

## Checking the published version

```bash
pip index versions apialerts
```
