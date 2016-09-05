import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

short_desc = "Short description"
long_desc = "Long description"

install_requires = [
    'flask==0.10.1',
    'click==6.6',
    'protobuf==3.0.0',
    'Flask-CORS==2.1.2'
]

tests_require = [
]


develop_requires = [
]


dependency_links = [
]


setup(
    name='pilgrim3',
    version='0.1.0',
    description=short_desc,
    long_description=long_desc,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Opendoor',
    author_email='developers@opendoor.com',
    url='https://github.com/opendoor-labs/pilgrim3',
    keywords='protobuf visualizer',
    packages=find_packages(),
    dependency_links=dependency_links,
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'dev': develop_requires,
        'test': tests_require,
    },
    entry_points="""\
    [console_scripts]
        pilgrim3 = pilgrim3.scripts.run:main
    """
)
