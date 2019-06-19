import os
import subprocess
from .file_reader import FileReader
from .file_writer import FileWriter


class ServerManager(object):
    def __init__(self, name, context, logWnd):
        self.name = name
        self.context = context
        self.logWnd = logWnd
        self.fileWriter = FileWriter(context["logfile"])
        self.fileReader = FileReader(context["logfile"])
        self.proc = None
        self._printServerComments()

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.stop()
        if self.fileWriter is not None:
            self.fileWriter.close()
            self.fileWriter = None
        if self.fileReader is not None:
            self.fileReader.close()
            self.fileReader = None

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        self.logWnd.writelines(self.fileReader.readlines())

    def stop(self):
        self.println(f"stop {self.name}")
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.println(f"The process {self.name} is not killed!")
            self.proc = None

    def println(self, line):
        self.logWnd.writeline(line)

    def _printServerComments(self):
        if "comments" in self.context:
            for line in self.context["comments"]:
                self.println(line)

    def run(self):
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.println(f"{workdir} is not exist")
            return
        cwd = os.getcwd()
        os.chdir(workdir)
        exename, configFileName = self.context["exefile"], self.context["configfile"]
        if (not os.path.exists(exename)) or (not os.path.exists(configFileName)):
            self.println(f"The {exename} not exist or config file {configFileName} not exist!")
            return
        self.proc = subprocess.Popen(exename, stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.println(f"{exename} is running")
