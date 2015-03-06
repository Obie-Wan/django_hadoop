#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Select and run jobs.
"""
from os import fork, _exit

from django_hadoop import (MRJOB_LOGGER,
                           NEW, FAILED, RUNNING, COMPLETED,
                           RESULT_PATH)
from django_hadoop.models import CommonJob
from django_hadoop.runner import RestJobRunner
from django_hadoop.results import DummyResultParser
from django_hadoop.hdfs import ExternalCallHDFSOperations
from django_hadoop.utils import process_exception


class JobManager(object):
    """Job spawning.
    """
    _job_runner = RestJobRunner  # override with your custom runner
    _job_model = CommonJob  # override with your custom model
    _job_result_parser = DummyResultParser  # override with your custom parser

    @classmethod
    def get_model(cls):
        """Job model getter.
        """
        return cls._job_model

    @classmethod
    def get_runner(cls):
        """Job runner getter.
        """
        return cls._job_runner

    @classmethod
    def get_result_parser(cls):
        """Result parser getter.
        """
        return cls._job_result_parser

    def reinit_job_instance_for_child(self, job_pk):
        """Close all sql connections and retrieve job instance again.
           Used in forked processes.
        """
        from django.db import connections
        for conn in connections.all():
            conn.close()
        return self._job_model.objects.get(pk=job_pk)

    def process_jobs(self):
        """Try to execute NEW and FAILED jobs.
        """
        new_jobs_qs = self._job_model.objects.filter(status__in=(NEW, FAILED))
        for job in new_jobs_qs:
            if not fork():
                # fork jobs and update their statuses, according to result
                try:
                    job = self.reinit_job_instance_for_child(job.pk)

                    # forked, update status and exec
                    job.update_status(RUNNING)
                    self.execute_forked_job(job)

                    job.update_status(COMPLETED)
                except:
                    job.update_status(FAILED)
                    # re-raise for proper logging
                    raise
                finally:
                    _exit(0)

    def execute_forked_job(self, job):
        """Fork MR-task => wait for completion => process result.
        """
        try:
            if isinstance(job, int):
                job = self._job_model.objects.get(pk=job)
            # 2DO: fuking optimize !!! -> glue parameters and jobs!
            # execute job and process results from HDFS
            self._job_runner(job).run_job()
            self.process_job_results(job)
        except:
            process_exception(MRJOB_LOGGER)
            raise

    @classmethod
    def process_job_results(cls, job):
        """Job completed - parse results and write them to cache.
        """
        job_result = ExternalCallHDFSOperations().read_file(RESULT_PATH %
                                                            job.pk)
        # skip empty job results
        if job_result.strip(' \n'):
            cls.get_result_parser()(job, job_result).parse_results()
