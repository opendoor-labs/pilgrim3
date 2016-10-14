import os, sys
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from subprocess import call

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test')))

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
    'selenium==2.53.6',
    'pytest==3.0.3',
    'py==1.4.31'
]


develop_requires = [
]


dependency_links = [
]

class build_py(_build_py):
    def run(self):
        result = call('bin/bundle_js')
        if result != 0:
            raise OSError("Could not compile javascript.  Make script/bundle_js works from root directory.")
        _build_py.run(self)

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
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={
        'dev': develop_requires,
        'test': tests_require,
    },
    cmdclass={'build_py': build_py},
    entry_points="""\
    [console_scripts]
        pilgrim3 = pilgrim3.scripts.run:main
    """
)
