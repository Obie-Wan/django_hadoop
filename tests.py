from django.utils.unittest import skipUnless
from django.test import TestCase

from django_hadoop.models import CommonJob
from django_hadoop.runner import LocalJobRunner, RestJobRunner

from django_hadoop import RUNNING, COMPLETED, HADOOP_JOB_CMD, JOB_MANAGER_CLASS
JOB_RUNNER_CLASS = JOB_MANAGER_CLASS.get_runner()


@skipUnless(JOB_RUNNER_CLASS == LocalJobRunner, 
            'skip if local runner is not used') 
class LocalJobRunnerTest(TestCase):
    """Test Map-Reduce runner.
    """
    def setUp(self):
        super(LocalJobRunnerTest, self).setUp()
        self._job = CommonJob.objects.create()
        self._runner = LocalJobRunner(self._job)

    def testShouldMakeValidMRCommand(self):
        """Should create valid MR command line.
        """
        self.assertTrue(self._runner.create_hadoop_command()\
                                    .startswith(HADOOP_JOB_CMD)) 

    def testShouldRunJobWithFailedExitCode(self):
        """Should start a job in a new process.
        """
        self.assertEquals(self._runner.run_job(), 0)


@skipUnless(JOB_RUNNER_CLASS == RestJobRunner, 
            'skip if REST runner is not used')
class RestJobRunnerTest(TestCase):
    """Test Map-Reduce runner.
    """
    def setUp(self):
        super(RestJobRunnerTest, self).setUp()
        self._job = CommonJob.objects.create()
        self._runner = RestJobRunner(self._job)

    def testShouldMakeValidMRConf(self):
        """Should create valid MR command line.
        """
        self.assertTrue(self._runner\
                            ._create_conf()\
                            .startswith('<?xml version="1.0"'
                                        ' encoding="UTF-8"?>\n<configuration>'))
        self.assertTrue(self._runner\
                            ._create_conf()\
                            .endswith('</configuration>\n'))

    def testShouldSubmitAJob(self):
        """Should submit a job to an Oozie REST API.
        """
        # job should start
        self.assertTrue(self._runner.run_job())

        # oozie job id should be received
        self.assertTrue(self._runner.oozie_job_id)

        # oozie job status should be RUNNING or COMPLETED
        self._runner.retrieve_job_status(self._runner.oozie_job_id)
        self.assertTrue(self._runner.oozie_job_status in (RUNNING, COMPLETED))

