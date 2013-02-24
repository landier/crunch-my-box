from setuptools import setup

setup(
    name = 'crunch_my_box',
    version = '0.1.0',
    author = 'Nicolas Landier',
    author_email = '',
    packages = ['cmb', 'cmb.grabber', 'cmd.splitter', 'cmb.cruncher', 'cmb.util'],
    scripts = ['cmb/launch_grabber.py'],
    url = 'https://github.com/landier/crunch-my-box',
    license =  open('LICENSE.txt').read(),
    description = 'Grabs emails and store them into a mongoDB database.',
    long_description = open('README.rst').read(),
    install_requires = ['couchdb', 'pymongo', 'nltk'],
)
