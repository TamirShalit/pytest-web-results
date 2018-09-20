from setuptools import setup, find_packages

setup(
    name='pytest-web-results',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/TamirShalit/pytest-web-results',
    install_requires=['pytest'],
    tests_requires=['pytest-web-results-server', 'pytest-flask'],
    author='Tamir Shalit',
    author_email='shalit.tamir@gmail.com',
    description='Pytest plugin for viewing results via web server'
)
