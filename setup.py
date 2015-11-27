__author__ = 'sumeet'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Keep your passwords safe',
    'author': 'Sumeet Rohatgi',
    'url': 'https://github.com/srohatgi',
    'download_url': 'https://github.com/srohatgi',
    'author_email': 'sum.rohatgi@gmail.com',
    'version': '0.1',
    'install_requires': ['nose2'],
    'packages': ['safe'],
    'scripts': [],
    'name': 'safe'
}

setup(**config, requires=['daemon', 'cherrypy', 'Crypto'])
