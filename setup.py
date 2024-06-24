from os.path import join, dirname

from setuptools import setup, find_packages

def get_description():
    with open(join(dirname(__file__), 'README.md'), 'rb') as fileh:
        return fileh.read().decode("utf8").replace('\r\n', '\n')

setup(
    name='apialerts',
    version='1.0.3',
    url='https://github.com/apialerts/apialerts-python',
    author='API Alerts',
    author_email='admin@apialerts.com',
    license='MIT',
    description='Python wrapper for the API Alerts service',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    keywords=['API Alerts', 'push', 'notifications', 'alert', 'monitoring'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['aiohttp', 'dataclasses'],
)
