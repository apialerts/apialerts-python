from setuptools import setup, find_packages

setup(
    name='apialerts',
    version='0.0.2',
    url='https://github.com/mononz/apialerts-python',
    author='API Alerts',
    author_email='admin@apialerts.com',
    description='Python wrapper for the API Alerts service',
    long_description='Python wrapper for the API Alerts service',
    packages=find_packages(),
    keywords=['API Alerts', 'push', 'notifications', 'alert', 'monitoring'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=['aiohttp', 'dataclasses'],
)