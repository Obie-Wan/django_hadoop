Hadoop integration for Django (through an Oozie REST API or local job execution).
This code allows running MapReduce tasks from the Django views.

### Installation
- Install this django app as usual (urls.py, settings.py, etc.).
 
- Prepare common Hadoop-related settings in your project's settings.py:
```python
HADOOP_MAIN         = 'node'
NAMENODE            = 'hdfs://%s:8020' % HADOOP_MAIN          # Hadoop namenode
JOB_USER            = 'oozie'                                 # Hadoop user for jobs & HDFS stuff
JOB_MANAGER_CLASS   = 'your_app.your_module.CustomJobManager' # your JobManager subclass
```

- Choose job runner

**a.** Oozie job runner (submits MR-jobs through an Oozie) [RECOMMENDED] settings:
```python
OOZIE_SERVER        = 'http://%s:11000' % HADOOP_MAIN         # Oozie RESTful server
HDFS_APP_DIR        = '/user/%s/your-app-in-hdfs' % JOB_USER  # Oozie application dir in HDFS
HDFS_APP_NAME       = 'YourHadoopApp.jar'                     # Oozie application name (in HDFS)
```

Put Oozie job configuration data to HDFS (*.jar, workflow.xml).
Add a Site in django admin with ip/domain reachable from the host running Oozie, then
setup SITE_ID in your project settings file.

**b.** Local job runner (submits MR-jobs locally through the pipe) settings:
```python
HADOOP_HOME         = '/usr/lib/hadoop-0.20'                  # path to Hadoop client home 
JOB_JAR_PATH        = '/home/%s/YourHadoopApp.jar'            # path to jar on the local FS 
HADOOP_JOB_CMD      = '%s/bin/hadoop jar %s' % (HADOOP_HOME,  # Hadoop command for running the job
                                                JOB_JAR_PATH) 
```

- Install hadoop client for reading from HDFS (required in both cases for reading job results).

- [OPTIONAL] Add crontab entry to run periodically ```python manage.py process_jobs```. This command should start new (and failed) jobs from database.

### JobManager customization

JobManager customization could be made through inheritance:
```python
class JobManager(object):
    _job_runner = RestJobRunner             # override with your custom runner (non-obligatory)
    _job_model = CommonJob                  # override with your custom model (non-obligatory)
    _job_result_parser = DummyResultParser  # override with your custom result parser (required)
```

- Processing results

Result parser could be subclassed from results.JobResultParser.
```python
class CustomJobManager(JobManager):
    _job_result_parser = CustomResulParser # your result parser implementation
```
Implement parse_results method and do everything you wish with self._result_dict.

- Changing runner behaviour

Job runner could be inherited from:
 1. RestJobRunner implements Oozie job runner.
 2. LocalJobRunner implements local job runner.

### Example
```python
        job = CustomJobManager.get_model().create()           # create model instance
        rest_job_runner = CustomJobManager.get_runner()(job)  # create job runner instance
        succeeded = rest_job_runner.run_job()                 # start a job
```

- You can get job model, runner and result parser via JobManager class methods: 
 - get_model(), 
 - get_runner()
 - get_result_parser()


Task state could be determined from JSON by getting task view. 
To manually update task status, just GET 'hadoop-notification-view' (pass hadoop_job_id and status variables).
This view is called by an Oozie automatically upon status change.

### Admin
All your model fields are exposed to admin with the help of ExposeAllFieldsMixin.
You can register your own ModelAdmin, if you don't like this behaviour.

---

Tested with hadoop 0.20.2-cdh3u5 and django 1.4 (1.75).

P.S. There's a lot of things to do. Just let me know, if you want some feature.
