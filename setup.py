"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='Credenciamento',  # Required
    version='1.0.0',  # Required
    description='Microservice Recipe',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/caiorodro/Credenciamento',  # Optional

    author='Caio Rodrigues (https://github.com/caiorodro)',  # Optional
    author_email='caiorodro@gmail.com',  # Optional
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6.3'
    ],

    keywords='sample setuptools development',  # Optional
    packages=find_packages(exclude=[]),  # Required
    python_requires='>=3.6.*',
    install_requires=['peppercorn'],  # Optional
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={  # Optional
        'sample': ['package_data.dat'],
    },
    data_files=[('my_data', ['base.sql'])],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/caiorodro/Credenciamento/issues',
        'Funding': '',
        'Say Thanks!': 'https://github.com/caiorodro/',
        'Source': 'https://github.com/caiorodro/Credenciamento',
    },
)
