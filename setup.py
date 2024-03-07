from setuptools import setup, find_packages

setup(
    name='apialerts',
    version='0.1.0',
    author='API Alerts',
    author_email='admin@apialerts.com',
    description='Python wrapper for the API Alerts service',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
