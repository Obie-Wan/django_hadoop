#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Job management urls.
"""
from django.conf.urls import patterns, url
from django_hadoop.views import JobView, UpdateJobStateView

urlpatterns = patterns(
    '',
    url(r'^(?P<id>\d+)/$', JobView.as_view()),
    url(r'^(?P<hadoop_job_id>[a-zA-Z0-9\-\@]+)/state/(?P<status>[A-Z]+)/$',
        UpdateJobStateView.as_view(), name='hadoop-notification-view'),
)
