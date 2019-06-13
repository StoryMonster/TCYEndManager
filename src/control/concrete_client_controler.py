import os
import subprocess
import shutil

class ConcreteClientControler(object):
    def __init__(self, name, context, logWnd):
        self.name = name
        self.context = context
        self.logWnd = logWnd
        self.fileWriter = open(context["logfile"], "w")
        self.fileReader = open(context["logfile"], "r")
        self.readedLength = 0
        self.proc = None
    
    def fileno(self):
        return self.fileWriter.fileno()

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
                pass
            self.proc = None

    def println(self, line):
        self.logWnd.writeline(line)
    
    def syncLogFromFile(self):
        if self.fileReader is None: return
        data = self.fileReader.read()
        lines = data.split("\n")
        for line in lines:
            if line.strip() == "": continue
            self.println(line.rstrip())
    
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
        self.proc = subprocess.Popen(f"{simulator} {scriptPath}", stdout=self, stderr=self, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.println(f"{self.name} is running")
