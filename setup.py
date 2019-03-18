from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='app_json_file_cache',
    version='0.1.2',
    description='Simple user directory respecting JSON cache for expensive functions.',
    long_description=long_description,
    url='https://github.com/JohannesEbke/app_json_file_cache',
    author='Johannes Ebke',
    author_email='johannes@ebke.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='xdg json cache appdirs',
    install_requires=['appdirs'],
    packages=['app_json_file_cache'],
)
