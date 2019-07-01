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
        self.proc = None
        self.logfile = context["logfile"]
        self._printServerComments()

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

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        try:
            self.logWnd.writelines(self.fileReader.readlines())
        except Exception as e:
            self.logWnd.warn(str(e))

    def stop(self):
        self._closeLogFileHandlers()
        self.logWnd.info("停止进程 "+self.name)
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.logWnd.warn("未能杀死进程 {} 或者该进程不存在".format(self.name))
            self.proc = None

    def _printServerComments(self):
        if "comments" in self.context:
            for line in self.context["comments"]:
                self.logWnd.comment(line)

    def _precheck(self):
        if self.isRunning():
            self.logWnd.error(self.name + " 还在运行中")
            return False
        workdir = self.context["workdir"]
        if not os.path.exists(workdir):
            self.logWnd.error("工作空间 {} 不存在".format(workdir))
            return False
        exefile = self.context["exefile"]
        if not os.path.isfile(exefile):
            self.logWnd.error(exefile+" 不存在!")
            return False
        return True

    def _startupLogEnvironment(self):
        try:
            self.fileWriter = FileWriter(self.logfile)
            self.fileReader = FileReader(self.logfile)
            return True
        except IOError as e:
            self.logWnd.error(str(e))
            self.logWnd.error("进程 {} 无法启动".format(self.name))
            return False

    def _launchSubprocess(self, cmd):
        import sys
        if sys.version_info.major == 2:
            self.logWnd.error("不再支持Python 3.0以下版本")
            return None
        if sys.version_info.minor <= 5:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, startupinfo=startupinfo)
        else: return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)

    def run(self):
        if not self._precheck(): return
        if not self._startupLogEnvironment(): return
        workdir = self.context["workdir"]
        cwd = os.getcwd()
        os.chdir(workdir)
        exename = self.context["exefile"]
        self.proc = self._launchSubprocess(exename)
        os.chdir(cwd)
        if self.proc is None: return
        self.logWnd.info("进程 {} 正在运行".format(exename))
