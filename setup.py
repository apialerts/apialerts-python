from setuptools import setup
import re

def derive_version() -> str:
    with open('apialerts/__init__.py') as f:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


setup(version=derive_version())