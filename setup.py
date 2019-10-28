try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Bell TBOT python API',
    'author': 'cl',
    'packages': ['bell'],
    'install_requires': ['nose'],
    'author_email': 'chencassc@gmail.com',
    # 'scripts:': [],
    'name': 'bell',
}

setup(**config)
