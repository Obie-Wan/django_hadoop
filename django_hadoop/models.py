#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Job manager models.
"""
from django.db.models import Model, CharField, DateTimeField
from django_hadoop import (NEW, FAILED, RUNNING, COMPLETED, NORMAL,
                           SUSPENDED, KILLED, JOB_PRIORITIES)
from django_hadoop.utils import utc_now


class BaseJob(Model):
    """Base Map-Reduce job class.
    """
    JOB_STATUS_CHOICES = (
        (NEW,       u'Новая'),
        (RUNNING,   u'Запущена'),
        (FAILED,    u'Ошибка'),
        (COMPLETED, u'Завершено'),
        (SUSPENDED, u'Приостановлено'),
        (KILLED,    u'Убито'),
    )
    JOB_PRIORITY_CHOICES = ((value, value) for value in JOB_PRIORITIES)

    hadoop_job_id = CharField(blank=True, null=True, max_length=36)
    status = CharField(default=NEW, choices=JOB_STATUS_CHOICES,
                       max_length=16)
    priority = CharField(default=NORMAL, choices=JOB_PRIORITY_CHOICES,
                         max_length=16)
    start_date = DateTimeField(null=True, blank=True)

    def update_status(self, new_status):
        """Quick wrapper for updating job status.
        """
        self.status = new_status
        self.save()

    def to_running_state(self, job_id):
        """Change job state to RUNNING.
        """
        self.start_date = utc_now()
        self.hadoop_job_id = job_id
        self.status = RUNNING
        self.save()

    def __unicode__(self):
        return u'job started at %s, priority=%s, status=%s' % (self.start_date,
                                                               self.priority,
                                                               self.status)

    class Meta:
        abstract = True


class CommonJob(BaseJob):
    """Common job model.
    """
    pass
