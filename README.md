Hadoop integration for Django (through an Oozie REST API or local job execution).
It's a refactored version of the previously removed django_oozie.
# Installation:
1. Install this django app as usual.
 
2. Prepare several settings in your project's settings.py.
Here's an example:
```
HADOOP_MAIN         = 'node'
NAMENODE            = 'hdfs://%s:8020' % HADOOP_MAIN
OOZIE_SERVER        = 'http://%s:11000' % HADOOP_MAIN
JOB_USER            = 'oozie'
HDFS_APP_DIR        = '/user/%s/your-app-in-hdfs' % JOB_USER
JOB_MANAGER_CLASS   = 'monitoring_jobs.job_spawner.CustomJobManager'
```
3. Override job manager with appropriate job runner and result parser realisations.
Result parser could be subclassed from results.JobResultParser.
Job runner could be subclassed from runner.RestJobRunner/runner.LocalJobRunner.
Available base classes for job runners:
```
RestJobRunner submits MR-jobs through an Oozie.
LocalJobRunner submits MR-jobs locally through the pipe.
```

Tested with hadoop 0.20.2-cdh3u5.

P.S. docs are coming soon.
