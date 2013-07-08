"""
MapReduce output processing logic.
"""
from abc import ABCMeta, abstractmethod

class JobResultParser(object):
    """Process job results, finish calculations and put them to cache.
    """
    __metaclass__ = ABCMeta

    def __init__(self, job, job_result):
        """Save job results to dict.
        """
        self._result_dict = {}
        self._job = job
        self.split_results(job_result)

    def split_results(self, job_result):
        """Separate result keys from values and save to dict.
           ACHTUNG! Sucks on a very big sets of data (just override this method)!
        """
        for line in job_result.split('\n'):
            if line:        
                (key, value) = line.strip().split()
                self._result_dict[key] = value

    @abstractmethod
    def parse_results(self):
        """Process result dict.
        """
        pass


class DummyResultParser(JobResultParser):
    """Concrete job resut parser, that does nothing.
    """
    def parse_results(self):
        pass
