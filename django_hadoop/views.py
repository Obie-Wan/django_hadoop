#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Job status views.
"""
from traceback import format_exc
from json import dumps

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404

from django_hadoop import (JOB_STATES, COMPLETED, FAILED, RUNNING,
                           MRJOB_LOGGER, JOB_MANAGER_CLASS)
from django_hadoop.utils import process_exception


class JobView(View):
    """Job status retrieval view.

       Returns:
           status(HttpResponse) - job status value or "error".
    """
    def get(self, request, **kwargs):
        json_resp = '{"status": %s}'
        try:
            job = JOB_MANAGER_CLASS.get_model()\
                                   .objects.get(pk=int(self.kwargs['id']))
            status = str(job.status)
        except:
            status = '"error"'
        return HttpResponse(json_resp % status,
                            content_type='application/json')


class UpdateJobStateView(View):
    """Update job status.
       This URL must be followed by an Oozie, when the job state changes.
       oozie.action.notification.url handler.
    """
    def get(self, request, **kwargs):
        response = {}
        status = self.kwargs['status']
        if status not in JOB_STATES:
            raise ValueError('Unknown job status "%s"' % status)

        # race condition protection on job creation
        # status could be changed to RUNNING before object creation
        if status == RUNNING:
            return HttpResponse('Skip RUNNING state')

        job = get_object_or_404(JOB_MANAGER_CLASS.get_model(),
                                hadoop_job_id=self.kwargs['hadoop_job_id'])
        try:
            if status == COMPLETED:
                JOB_MANAGER_CLASS.process_job_results(job)
        except:
            process_exception(MRJOB_LOGGER)
            status = FAILED
            response['error'] = format_exc()

        job.update_status(status)
        response['status'] = status
        return HttpResponse(dumps(response), content_type='application/json')
