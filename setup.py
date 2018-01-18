from setuptools import setup, find_packages

setup(
    name='confluence-rest-library',
    packages=find_packages(),
    version='0.2.2',
    description='A simple wrapper around the Confluence REST API.',
    author='David Tyler',
    author_email='davet.code@gmail.com',
    url='https://github.com/DaveTCode/confluence-python-lib',
    keywords=['confluence'],
    classifiers=[],
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    install_requires=['requests >= 2.18.4, < 3.0.0a0'],
    tests_require=['pytest >= 3.0.7, < 4.0.0a0', 'pytest-cov >= 2.5.0, < 3.0.0a0']
)
