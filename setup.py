import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = ['httplib2', 'argparse', 'prettytable']
if sys.version_info < (2,6):
    requirements.append('simplejson')

setup(
    name = "openstack.compute",
    version = "2.0a1",
    description = "Client library for the OpenStack Compute API",
    long_description = read('README.rst'),
    url = 'http://openstack.compute.rtfd.org/',
    license = 'BSD',
    author = 'Jacob Kaplan-Moss',
    author_email = 'jacob@jacobian.org',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    namespace_packages = ["openstack"],
    install_requires = requirements,
    
    tests_require = ["nose", "mock"],
    test_suite = "nose.collector",
    
    entry_points = {
        'console_scripts': ['openstack-compute = openstack.compute.shell:main']
    }
)