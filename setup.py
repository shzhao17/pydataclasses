#!/usr/bin/env python

from codecs import open

from setuptools import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='pydataclasses',
    version='0.0.1',
    description='Python Data Classes',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author='Patrick Zhao',
    author_email='dearpatrickzhao@gmail.com',
    url='https://github.com/dearpatrickzhao/pydataclasses',
    packages=['pydataclasses'],
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    python_requires=">=2.7, >=3.6",
    install_requires=['six', 'typing'],
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    tests_require=[],
    extras_require={},
)
