from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "python-cloudservers",
    version = "1.0a2",
    description = "Client library for Rackspace's Cloud Servers API",
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