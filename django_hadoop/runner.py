"""Job runner classes.
   Executes MR-job, using appropriate method.
"""
from abc import ABCMeta, abstractmethod
from subprocess import call
from urllib2 import Request, urlopen
from django.utils import simplejson

from django_hadoop import MRJOB_LOGGER
from django_hadoop.utils import process_exception, get_host_name
from django_hadoop import (NORMAL, 
    OOZIE_REST_URL, OOZIE_START_URL, OOZIE_STAT_URL,
    OOZIE_SERVER, OOZIE_JOB_TEMPLATE,
    JOB_OPTIONS, JOB_VIEW_URL, HADOOP_JOB_CMD)


class BaseJobRunner(object):
    """Abstract job runner class. Segregates job execution logic.
       Creates job arguments from the job instance and runs this job.
    """
    __metaclass__ = ABCMeta
    _job_options  = JOB_OPTIONS

    def __init__(self, job, priority=NORMAL):
        self._job      = job
        self._priority = priority

    @abstractmethod
    def run_job(self):
        """Start a new job.
           
           Return:
               success_status(Boolean) - status of job exceution.
        """
        pass

    def prepare_job_args(self):
        """Update _job_options dict with custom arguments.
        """
        pass


class LocalJobRunner(BaseJobRunner):
    """Simple Hadoop local job runner (simple exec).
    """
    def create_hadoop_command(self):
        """Create full hadoop command with arguments from job 
           and from job_options dict.
        """
        return '%s %s' % (HADOOP_JOB_CMD, 
                          ' '.join('-D %s=%s' % (key, value)
               for (key, value) in self._job_options.iteritems() if value))
 
    def run_job(self):
        """Start a new job in a subprocess.
        """
        try:
            self.prepare_job_args()
            self._job.to_running_state('-') # 2do: get job id for local runner
            return call(self.create_hadoop_command().split())
        except OSError:
            process_exception(MRJOB_LOGGER, 
                              message='External command execution error!')
 

class RestJobRunner(BaseJobRunner):
    """Oozie REST job runner.
    """
    _response = None
    _headers = {'Content-type': 'application/xml;charset=UTF-8'}

    @property
    def oozie_job_id(self):
        return self.get_response_field('id')

    @property
    def oozie_job_status(self):
        # 2DO: get job error code & error message on FAIL
        return self.get_response_field('status')

    def get_response_field(self, field):
        """Retrieve the field from an oozie response.
        """
        if self._response:        
            return self._response[field] if field in self._response else None

    def send(self, server, action, data=None):
        """Send request to server with POST.
        """        
        headers = {} if not data else self._headers
        try:
            request = Request(url='%s/%s%s' % (server, OOZIE_REST_URL, action),
                              data=data, headers=headers)
            self._response = simplejson.loads(urlopen(request).read())            
        except:
            process_exception(MRJOB_LOGGER, 
                              message='Oozie REST communication error\n%s' % 
                              request.get_data())
 
    @property
    def notification_url(self):
        """Construct notification url for Hadoop.

           Return:
               notification_url(string) - full link to django_hadoop
                                          notification view.
        """
        return 'http://%s%s' % (get_host_name(), 
                                JOB_VIEW_URL.replace('JOBID', '$jobId')\
                                            .replace('STATUS', '$status'))

    def _create_conf(self):
        """Create XML job config for Oozie.

           Returns:
               hadoop_xml_config(string) - hadoop task options in XML
        """
        # get current host name
        self._job_options['oozie.wf.workflow.notification.url'] = \
        self.notification_url
        return OOZIE_JOB_TEMPLATE % \
               '\n'.join(
               '''<property>\n'''
                   '''<name>%s</name>\n'''
                    '''<value>%s</value>\n'''
               '''</property>'''
               % (k, v) for (k,v) in self._job_options.items())

    def run_job(self):
        """Start a new job with an Oozie.
        """
        self.prepare_job_args()
        self.send(OOZIE_SERVER, OOZIE_START_URL, self._create_conf())

        if self.oozie_job_id:
            self._job.to_running_state(self.oozie_job_id)
            return True

    def retrieve_job_status(self, oozie_job_id):
        """Get job status from an Oozie.
        """
        self.send(OOZIE_SERVER, OOZIE_STAT_URL % oozie_job_id)
        return self.oozie_job_status

