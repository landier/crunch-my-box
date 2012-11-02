from setuptools import setup

setup(
    name = 'Mail',
    version = '0.1.0',
    author = 'Nicolas Landier',
    author_email = 'mescouilles@surton.nez',
    packages = ['mail', 'mail.test'],
    scripts = ['bin/mail.py'],
    url = '',
    license =  open('LICENSE.txt').read(),
    description = 'Grabs emails and store them into a CouchDB.',
    long_description = open('README.rst').read(),
    install_requires = ['couchdb'],
)