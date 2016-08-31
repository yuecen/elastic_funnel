# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

pkg_file = open("elastic_funnel/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", pkg_file))
description = open('README.md').read()
requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='elastic_funnel',
    description='Analysis tool for funnel visualization with log from Elasticsearch',
    version=metadata['version'],

    # Author details
    author='yuecen',
    author_email='yuecendev+pypi@gmail.com',
    url='https://github.com/yuecen/elastic_funnel',
    long_description=description,
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    keywords='elasticsearch, log, funnel, elastic_funnel',
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'elastic_funnel = elastic_funnel.cli:main'
        ]
    }
)