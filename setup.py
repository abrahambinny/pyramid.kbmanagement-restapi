import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'sqlalchemy',
    'pyramid_tm',
    'zope.sqlalchemy',
    'cornice',
    'waitress',
    'pytest',
    'webtest',
    'requests',
    'psycopg2',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest'
]

setup(
    name='kbm',
    version=0.1,
    description='kbm api',
    long_description='api for kbm',
    install_requires=requires,
    extras_require={
    'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = kbm:main'
        ],
        'console_scripts': [
            'initialize_kbm_db = kbm.initialize_db:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords="web services",
    author='binny abraham',
    author_email='abrahambinny@gmail.com',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    paster_plugins=['pyramid']
)
