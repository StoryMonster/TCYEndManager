import os
import subprocess

class ConcreteServerControler(object):
    def __init__(self, name, context, logWnd):
        self.name = name
        self.context = context
        self.logWnd = logWnd
        self.fileWriter = open(context["logfile"], "w")
        self.fileReader = open(context["logfile"], "r")
        self.readedLength = 0
        self.proc = None

    def __exit__(self, *args):
        self.close()
    
    def fileno(self):
        return self.fileWriter.fileno()

    def close(self):
        self.stop()
        if self.fileWriter is not None:
            self.fileWriter.close()
            self.fileWriter = None
        if self.fileReader is not None:
            self.fileReader.close()
            self.fileReader = None
    
    def syncLogFromFile(self):
        if self.fileReader is None: return
        data = self.fileReader.read()
        lines = data.split("\n")
        for line in lines:
            if line.strip() == "": continue
            self.println(line.rstrip())
    
    def stop(self):
        self.println(f"stop {self.name}")
        if self.proc is not None:
            os.kill(self.proc.pid, 9)
            self.proc = None

    def println(self, line):
        self.logWnd.writeline(line)
    
    def _printServerComments(self):
        if "comments" in self.context:
            for line in self.context["comments"]:
                self.println(line)
    
    def run(self):
        self._printServerComments()
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
        self.proc = subprocess.Popen(exename, stdout=self, stderr=self, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.println(f"{exename} is running")
