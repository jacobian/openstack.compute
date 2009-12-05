from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup

setup(
    name = "cloudservers",
    version = "1.0",
    description = "Client library for Rackspace's Cloud Servers",
    license = 'BSD',
    author = 'Jacob Kaplan-Moss',
    author_email = 'jacob@jaobian.org',
    py_modules = ['cloudservers'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ['httplib2', 'cmdln', 'prettytable'],
    
    tests_require = ["nose", "mock"],
    test_suite = "nose.collector",
    
    entry_points = {
        'console_scripts': ['cloudservers = cloudservers.shell:main']
    }
)