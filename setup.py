#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django_hadoop',
    description='Django application for running Hadoop Map-Reduce \
                 tasks and getting their results',
    version=u'0.1.0',
    url=u'https://github.com/Obie-Wan/django_hadoop',
    install_requires=[
        'pytz',
    ],
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
)
