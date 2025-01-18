# Release Process

1. Update the version in `apialerts/__init__.py`
2. Update the version in `apialerts/constants.py`
3. PR and merge to `main` branch after tests pass
4. Create a new release on GitHub from `main`
5. GitHub Actions will publish to PyPi
