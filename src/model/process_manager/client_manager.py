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

    def println(self, line):
        self.logWnd.writeline(line)

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        self.logWnd.writelines(self.fileReader.readlines())

    def run(self):
        try:
            self.fileWriter = FileWriter(self.logfile)
            self.fileReader = FileReader(self.logfile)
        except IOError as e:
            self.logWnd.writeline(str(e))
            raise Exception(f"进程 {self.name} 无法启动")
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.logWnd.error(f"工作路径不存在 {workdir}")
            return
        cwd = os.getcwd()
        os.chdir(workdir)
        simulator, configFile = self.context["simulator"], self.context["configFile"]
        if (not os.path.exists(simulator)) or (not os.path.exists(configFile)):
            self.logWnd.error(f"模拟器 {simulator} 或者配置文件 {configFile} 不存在!")
            return
        VALID_CONFIG_FILE = simulator[:simulator.rfind("/")+1] + "windows.ini"
        shutil.copy(configFile, VALID_CONFIG_FILE)
        scriptPath = self.context["script"]
        self.proc = subprocess.Popen(f"{simulator} {scriptPath}", stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.logWnd.info(f"进程 {self.name} 正在运行")
