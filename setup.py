from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1.0'

setup(name='mail',
    version=version,
    description="This is a description of the package",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='mail, Gmail, CouchDB',
    author='Nicolas Landier',
    author_email='nicolas.landier@gmail.com',
    url='http://wiki.secondlife.com/wiki/Eventlet',
    license='MIT',
    packages=find_packages('mail'),
    install_requires=['couchdb'],
)