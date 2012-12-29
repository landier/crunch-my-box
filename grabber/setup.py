from setuptools import setup

setup(
    name = 'Mail',
    version = '0.1.0',
    author = 'Nicolas Landier',
    author_email = '',
    packages = ['mail', 'mail.grabber', 'mail.util'],
    scripts = ['mail/launch_grabber.py'],
    url = 'https://github.com/landier/crunch-my-box',
    license =  open('../LICENSE.txt').read(),
    description = 'Grabs emails and store them into a CouchDB.',
    long_description = open('../README.rst').read(),
    install_requires = ['couchdb', 'pymongo'],
)
