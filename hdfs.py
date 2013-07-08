from abc import ABCMeta, abstractmethod
from subprocess import Popen, PIPE

class BaseHDFSOperations(object):
    """Common HDFS operations interface.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_file(self, path):
        pass


class ExternalCallHDFSOperations(BaseHDFSOperations):
    """HDFS operations realisation, using external binary call.
    """
    command = 'hadoop fs -cat '

    def _run_external(self, command):
        pipe = Popen(command.split(), 
                     stdout=PIPE, stderr=PIPE, 
                     bufsize=256*1024*1024)
        output, errors = pipe.communicate()
        if pipe.returncode:
            raise Exception(errors)
        else:
            return output.strip()

    def read_file(self, path):        
        return self._run_external(self.command + path)

