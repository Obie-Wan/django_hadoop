#!/usr/bin/env python
#-*- coding:utf-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand
from django.utils import termcolors
from django_hadoop.job_spawner import JobManager

style = termcolors.make_style(fg='green', opts=('bold',))

class Command(NoArgsCommand):
    def handle_noargs(self, **options):        
        JobManager().process_jobs()
        

