import os
import subprocess
from model.common.file_reader import FileReader
from model.common.file_writer import FileWriter


class ServerManager(object):
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
            raise Exception(f"进程 {self.name} 不能启动!")
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
    
    def isRunning(self):
        return self.proc is not None

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        self.logWnd.writelines(self.fileReader.readlines())

    def stop(self):
        self.logWnd.info(f"停止进程 {self.name}")
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.logWnd.warn(f"未能杀死进程 {self.name} 或者该进程不存在")
            self.proc = None

    def println(self, line):
        self.logWnd.writeline(line)

    def _printServerComments(self):
        if "comments" in self.context:
            for line in self.context["comments"]:
                self.logWnd.info(line)

    def run(self):
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.logWnd.error(f"工作空间 {workdir} 不存在")
            return
        cwd = os.getcwd()
        os.chdir(workdir)
        exename, configFileName = self.context["exefile"], self.context["configfile"]
        if (not os.path.exists(exename)) or (not os.path.exists(configFileName)):
            self.logWnd.error(f"可执行程序 {exename} 或者配置文件 {configFileName} 不存在!")
            return
        self.proc = subprocess.Popen(exename, stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)
        os.chdir(cwd)
        self.logWnd.info(f"进程 {exename} 正在运行")
