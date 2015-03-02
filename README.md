Hadoop integration for Django (through an Oozie REST API or local job execution).
This code allows running MapReduce tasks from the Django views.

#### Installation:
- Install this django app as usual (urls.py, settings.py, etc.).
 
- Prepare several settings in your project's settings.py:
```python
HADOOP_MAIN         = 'node'
NAMENODE            = 'hdfs://%s:8020' % HADOOP_MAIN          # Hadoop namenode
JOB_USER            = 'oozie'                                 # Hadoop user for jobs & HDFS stuff
JOB_MANAGER_CLASS   = 'your_app.your_module.CustomJobManager' # your JobManager subclass
```

- Choose job runner

Oozie job runner (submits MR-jobs through an Oozie) settings:
```
OOZIE_SERVER        = 'http://%s:11000' % HADOOP_MAIN         # Oozie RESTful server
HDFS_APP_DIR        = '/user/%s/your-app-in-hdfs' % JOB_USER  # Oozie application dir in HDFS
```
Local job runner (submits MR-jobs locally through the pipe) settings:
```
HADOOP_HOME         = '/usr/lib/hadoop-0.20'                  # path to Hadoop client home 
JOB_JAR_PATH        = '/home/%s/YourHadoopApp.jar'            # path to jar on the local FS 
HADOOP_JOB_CMD      = '%s/bin/hadoop jar %s' % (HADOOP_HOME,  # Hadoop command for running the job
                                                    JOB_JAR_PATH) 
```

- Install hadoop client for reading from HDFS (required for reading job results).

- Put Oozie job configuration data to HDFS (*.jar, workflow.xml) if you are using OozieJobRunner (default).

### Customization JobManager
- Processing results

Result parser could be subclassed from results.JobResultParser.
```python
class CustomJobManager(JobManager):
    _job_result_parser = CustomResulParser # your result parser implementation
```
- Changing runner behaviour

Job runner could be subclassed from runner.RestJobRunner/runner.LocalJobRunner.
Available base classes for job runners:
 1. RestJobRunner implements Oozie job runner.
 2. LocalJobRunner implements local job runner.

- Use job model where you wish.
```python
        job = CustomJobManager.get_model().create()                          
        rest_job_runner = CustomJobManager.get_runner()(job)
        succeeded = rest_job_runner.run_job()
```

- You can get job model, runner and result parser via JobManager class methods: 
 - get_model(), 
 - get_runner()
 - get_result_parser()

### Admin stuff:
All your model fields are exposed to admin with the help of ExposeAllFieldsMixin.
You can register your own ModelAdmin, if you don't like this behaviour.

---

Tested with hadoop 0.20.2-cdh3u5 and django 1.4.

P.S. There's a lot of things to do. Just let me know, if you want some feature.
