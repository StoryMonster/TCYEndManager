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
        self.logfile = context["logfile"]
        self.proc = None

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.stop()

    def _closeLogFileHandlers(self):
        if self.fileWriter is not None:
            self.fileWriter.close()
            self.fileWriter = None
        if self.fileReader is not None:
            self.fileReader.close()
            self.fileReader = None

    def isRunning(self):
        return self.proc is not None

    def stop(self):
        self._closeLogFileHandlers()
        self.logWnd.info(f"停止进程 {self.name}")
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.logWnd.warn(f"未能杀死进程 {self.name} 或者该进程不存在")
            self.proc = None

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        try:
            self.logWnd.writelines(self.fileReader.readlines())
        except Exception as e:
            self.logWnd.warn(str(e))

    def _precheck(self):
        if self.isRunning():
             self.logWnd.error(f"{self.name} 还在运行中")
             return False
        workdir = self.context["workdir"]
        if not os.path.isdir(workdir):
            self.logWnd.error(f"工作路径不存在 {workdir}")
            return False
        simulator, configFile = self.context["simulator"], self.context["configFile"]
        if (not os.path.isfile(simulator)) or (not os.path.isfile(configFile)):
            self.logWnd.error(f"模拟器 {simulator} 或者配置文件 {configFile} 不存在!")
            return False
        return True

    def _startupLogEnvironment(self):
        try:
            self.fileWriter = FileWriter(self.logfile)
            self.fileReader = FileReader(self.logfile)
            return True
        except IOError as e:
            self.logWnd.error(str(e))
            self.logWnd.error(f"进程 {self.name} 无法启动")
            return False

    def run(self):
        if not self._precheck(): return
        if not self._startupLogEnvironment(): return
        workdir = self.context["workdir"]
        cwd = os.getcwd()
        os.chdir(workdir)
        simulator, configFile = self.context["simulator"], self.context["configFile"]
        VALID_CONFIG_FILE = simulator[:simulator.rfind("/")+1] + "windows.ini"
        shutil.copy(configFile, VALID_CONFIG_FILE)
        scriptPath = self.context["script"]
        self.proc = subprocess.Popen(f"{simulator} {scriptPath}", stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.logWnd.info(f"进程 {self.name} 正在运行")
