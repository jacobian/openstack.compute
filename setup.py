import os
from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-cloudservers",
    version = "1.0a3",
    description = "Client library for Rackspace's Cloud Servers API",
    long_description = read('README.rst'),
    url = 'http://packages.python.org/python-cloudservers',
    license = 'BSD',
    author = 'Jacob Kaplan-Moss',
    author_email = 'jacob@jacobian.org',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ['httplib2', 'argparse', 'prettytable'],
    
    tests_require = ["nose", "mock"],
    test_suite = "nose.collector",
    
    entry_points = {
        'console_scripts': ['cloudservers = cloudservers.shell:main']
    }
)