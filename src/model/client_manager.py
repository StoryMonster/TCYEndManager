import os
import subprocess
import shutil
from .file_reader import FileReader
from .file_writer import FileWriter

class ClientManager(object):
    def __init__(self, name, context, logWnd):
        self.name = name
        self.context = context
        self.logWnd = logWnd
        self.fileWriter = None
        self.fileReader = None
        try:
            self.fileWriter = FileWriter(context["logfile"])
            self.fileReader = FileReader(context["logfile"])
        except IOError as e:
            self.logWnd.write(str(e))
            raise Exception(f"process {self.name} cannot start!")
        self.proc = None

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

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        self.logWnd.writelines(self.fileReader.readlines())

    def run(self):
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.println(f"{workdir} is not exist")
            return
        cwd = os.getcwd()
        os.chdir(workdir)
        simulator, configFile = self.context["simulator"], self.context["configFile"]
        if (not os.path.exists(simulator)) or (not os.path.exists(configFile)):
            self.println(f"The {simulator} not exist or config file {configFile} not exist!")
            return
        VALID_CONFIG_FILE = simulator[:simulator.rfind("/")+1] + "windows.ini"
        shutil.copy(configFile, VALID_CONFIG_FILE)
        scriptPath = self.context["script"]
        self.proc = subprocess.Popen(f"{simulator} {scriptPath}", stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.println(f"{self.name} is running")
