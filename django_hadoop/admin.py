#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.admin import site, ModelAdmin
from django_hadoop import JOB_MANAGER_CLASS

job_model_cls = JOB_MANAGER_CLASS.get_model()


class ExposeAllFieldsMixin(object):
    """ModelAdmin mixin for auto-exposing model fields to admin.
    """
    def __init__(self, *args, **kwargs):
        self.fields = self.get_fields()
        self.list_display = self.get_supported_fields()
        self.list_display_links = self.list_display
        super(ExposeAllFieldsMixin, self).__init__(*args, **kwargs)

    def get_fields(self):
        """Get all model field names, except id.
        """
        return [n for n in self.model._meta.get_all_field_names() if n != 'id']

    def get_supported_fields(self):
        """Get all model field names, applicable to list_display.
        """
        NOT_SUPPORTED = ('ManyToManyField',)
        return [field.name for field in self.model._meta.fields
                if field.__class__.__name__ not in NOT_SUPPORTED]


class JobAdmin(ExposeAllFieldsMixin, ModelAdmin):
    """Job management model admin.
    """
    model = job_model_cls
    list_filter = ('status', 'priority',)
    ordering = ['-start_date']

site.register(job_model_cls, JobAdmin)
