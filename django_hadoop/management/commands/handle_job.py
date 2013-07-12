#!/usr/bin/env python
#-*- coding:utf-8 -*-
from optparse import make_option

from django.core.management.base import LabelCommand, CommandError
from django.utils import termcolors
from django_hadoop.job_spawner import JobManager

style = termcolors.make_style(fg='green', opts=('bold',))

class Command(LabelCommand):
    help  = 'Execute given Map-Reduce job and process result'
    label = 'job id'
    args  = '<job id>'
    requires_model_validation = False

    def handle_label(self, label, **options):        
        JobManager().execute_forked_job(int(label))

