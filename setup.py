from codecs import open
from os import path
from setuptools import setup, find_packages

readme = path.join(path.abspath(path.dirname(__file__)), 'README.rst')

with open(readme, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='confluence-rest-library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version='1.2.1',
    description='A simple wrapper around the Confluence REST API.',
    long_description=long_description,
    author='David Tyler',
    author_email='davet.code@gmail.com',
    url='https://github.com/DaveTCode/confluence-python-lib',
    keywords=['confluence'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=2.7,!=3.0,!=3.1,!=3.2,!=3.3,!=3.4',
    setup_requires=['pytest-runner', 'pypandoc', 'typing', 'pycodestyle', 'bandit', 'mypy'],
    install_requires=['requests >= 2.19.1, < 3.0.0a0'],
    tests_require=['pytest >= 4.3.0, < 5.0.0a0', 'pytest-cov >= 2.5.0, < 3.0.0a0']
)
