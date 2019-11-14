try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Bell TBOT python API',
    'author': 'cl',
    'packages': ['bell'],
    'install_requires': ['websocket-client'],
    'author_email': 'chencassc@gmail.com',
    'version': "0.0.1",
    'name': 'bell',
}

setup(**config)
