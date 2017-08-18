#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
#history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'selenium',
    'requests',
    'pexpect',
]

test_requirements = [
    'selenium',
    'requests',
    'pexpect',
    'mock',
    'pytest',
]

setup(
    name='et',
    version='0.0.1',
    description='Framework for testing the expedition tool',
    author='Palo Alto Networks',
    author_email='techpartners@paloaltonetworks.com',
    url='https://github.com/PaloAltoNetworks/expedition-test',
    packages=[
        'et',
        'et.server',
        'et.gui',
        'et.logs',
    ],
    package_dir={
        'et': 'et',
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC",
    zip_safe=False,
    keywords='et',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=['pytest-runner', ],
)
