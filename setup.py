from setuptools import setup, find_packages

setup(
    name='pytest-web-results',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/TamirShalit/pytest-web-results',
    install_requires=['pytest', 'requests'],
    extras_require={'test': ['pytest-web-results-server', 'pytest-flask', 'flask']},
    author='Tamir Shalit',
    author_email='shalit.tamir@gmail.com',
    description='Pytest plugin for viewing results via web server',
    entry_points={'pytest11': ['webresults = pytestwebresults.plugin']},
    classifiers=["Framework :: Pytest"]
)
