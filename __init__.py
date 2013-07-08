"""
Map-Reduce job runner settings.
"""
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

MRJOB_LOGGER        = getattr(settings, 'MRJOB_LOGGER', 'oozie_communications')

# common job runner settings ###################################################
NAMENODE           = getattr(settings, 'NAMENODE')
OOZIE_SERVER       = getattr(settings, 'OOZIE_SERVER')

                     # job/$jobId/state/$status/
JOB_VIEW_URL       = getattr(settings, 'JOB_VIEW_URL',
                             reverse_lazy('hadoop-notification-view',
                                          # shadow values (for reverse)
                                          # replaced later
                                          kwargs = {'hadoop_job_id': 'JOBID',
                                                    'status':        'STATUS'}))

################################################################################

try:
    JOB_USER = settings.JOB_USER
except AttributeError:
    raise ValueError('settings.JOB_USER is not set!')

HDFS_APP_DIR        = getattr(settings, 'HDFS_APP_DIR')
HDFS_APP_PATH       = '%s%s' % (NAMENODE, HDFS_APP_DIR)
HDFS_OUTPUT_DIR     = getattr(settings, 'HDFS_OUTPUT_DIR', 
                              '%s/jobs' % HDFS_APP_DIR)

# output file name pattern where %d is a job id
RESULT_FILE_PATTERN = getattr(settings, 'RESULT_FILE_PATTERN',
                              'mon_result_%d/part-*')
RESULT_PATH         = '%s%s' % (HDFS_OUTPUT_DIR, RESULT_FILE_PATTERN,)

################################################################################
# local job runner settings ####################################################
HADOOP_HOME         = getattr(settings, 'HADOOP_HOME', '/usr/lib/hadoop-0.20')
JOB_JAR_PATH        = getattr(settings, 'JOB_JAR_PATH',
                             '/home/%s/MonitoringStatAggregator.jar' % JOB_USER)
HADOOP_JOB_CMD      = getattr(settings, 'HADOOP_JOB_CMD', 
                             '%s/bin/hadoop jar %s' % (HADOOP_HOME,
                                                       JOB_JAR_PATH))

################################################################################
# hadoop level job options #####################################################
JOB_OPTIONS         = getattr(settings, 'JOB_OPTIONS', 
                              {
                               'user.name': JOB_USER,
                               'oozie.wf.application.path': HDFS_APP_PATH,
                               #'mapred.reduce.tasks': 10,
                               'output_dir': HDFS_OUTPUT_DIR
                              })

###############################################################################
# constants ###################################################################
OOZIE_REST_URL      = 'oozie/v1/'
OOZIE_START_URL     = 'jobs?action=start'
OOZIE_STAT_URL      = 'job/%s?show=info'

# job creation POST request template
OOZIE_JOB_TEMPLATE  = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                       '<configuration>\n%s\n</configuration>\n')

# job statuses: PREP, RUNNING , SUSPENDED , SUCCEEDED , KILLED and FAILED
JOB_STATES = ('NEW', 'RUNNING', 'FAILED', 'SUCCEEDED', 'KILLED', 'SUSPENDED',) 
NEW, RUNNING, FAILED, COMPLETED, KILLED, SUSPENDED = JOB_STATES

# job priorities
JOB_PRIORITIES = ('VERY_LOW', 'LOW', 'NORMAL', 'HIGH', 'VERY_HIGH',)
VERY_LOW, LOW, NORMAL, HIGH, VERY_HIGH = JOB_PRIORITIES

###############################################################################

from django_hadoop.job_spawner import JobManager
from django_hadoop.utils import load_class
try:
    JOB_MANAGER_CLASS = getattr(settings, 'JOB_MANAGER_CLASS')
    JOB_MANAGER_CLASS = load_class(JOB_MANAGER_CLASS)
except AttributeError:
    JOB_MANAGER_CLASS = JobManager

