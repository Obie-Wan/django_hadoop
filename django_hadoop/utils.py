#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pytz import timezone
from datetime import datetime
from logging import getLogger
from traceback import format_exc

from django.utils.timezone import utc
from django.utils.importlib import import_module
from django.contrib.sites.models import Site


def load_class(full_class_string):
    """Dynamically load a class from a string.

       Arguments:
           full_class_string(str) - full class path like
                                    module.submodule.ClassName

       Returns:
           class  - class type valiable
    """
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = import_module(module_path)

    # Finally, we retrieve the Class
    return getattr(module, class_str)


def utc_now():
    """Get current datetime as UTC.

       Returns:
           datetiem - UTC datetime object
    """
    return timezone(utc.zone).localize(datetime.utcnow())


def process_exception(logger, message=None):
    """Common exception handler.

       Arguments:
           logger(str) - logger name.
           message(str) - additional message.
    """
    message = message or 'caught exception'
    if not logger:
        logger = getLogger('root')
        logger.error('ACHTUNG! Unknown logger!')
    else:
        logger = getLogger(logger)
        logger.error('%s\n%s' % (message, format_exc()))


def get_host_name():
    """Return current hostname.
    """
    return Site.objects.get_current().domain
