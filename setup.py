#!/usr/bin/env python
# -*- coding: utf-8 -*-


from distutils.core import setup

setup(
    name='django_hadoop',
    description='Django application for running Hadoop Map-Reduce \
                 tasks and getting their results',
    packages=[
        'django_hadoop',
    ],
    version=u'0.1.0',
    url=u'https://github.com/Obie-Wan/django_hadoop',
    license='LICENSE',
)
