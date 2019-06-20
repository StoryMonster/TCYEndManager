import os
import subprocess
import shutil
from model.common.file_reader import FileReader
from model.common.file_writer import FileWriter

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
            self.logWnd.writeline(str(e))
            raise Exception(f"进程 {self.name} 无法启动")
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

    def isRunning(self):
        return self.proc is not None

    def stop(self):
        self.println(f"stop {self.name}")
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.println(f"未能杀死进程 {self.name}")
            self.proc = None

    def println(self, line):
        self.logWnd.writeline(line)

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        self.logWnd.writelines(self.fileReader.readlines())

    def run(self):
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.println(f"工作路径不存在 {workdir}")
            return
        cwd = os.getcwd()
        os.chdir(workdir)
        simulator, configFile = self.context["simulator"], self.context["configFile"]
        if (not os.path.exists(simulator)) or (not os.path.exists(configFile)):
            self.println(f"模拟器 {simulator} 或者配置文件 {configFile} 不存在!")
            return
        VALID_CONFIG_FILE = simulator[:simulator.rfind("/")+1] + "windows.ini"
        shutil.copy(configFile, VALID_CONFIG_FILE)
        scriptPath = self.context["script"]
        self.proc = subprocess.Popen(f"{simulator} {scriptPath}", stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.println(f"进程 {self.name} 正在运行")
