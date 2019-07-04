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

    def _unique_check(self):
        try:
            from psutil import process_iter
            exefile = self.context["exefile"]
            exefile = exefile if "/" not in exefile else exefile[exefile.rfind("/")+1:]
            for proc in process_iter():
                if proc.name() == exefile:
                    self.logWnd.error("系统中存在{}正在执行，请手动杀死该进程(pid: {})".format(exefile, proc.pid))
                    return False
            return True
        except ImportError:
            self.logWnd.warn("psutil包不存在，将不会检查是否已经有该程序在执行。可在控制台执行pip install psutil安装")
            return True

    def _precheck(self):
        if self.isRunning():
            self.logWnd.error(self.name + " 还在运行中")
            return False
        rundir = self.context["rundir"]
        if not os.path.exists(rundir):
            self.logWnd.error("执行路径 {} 不存在".format(rundir))
            return False
        exefile = self.context["exefile"]
        if not os.path.isfile(exefile):
            self.logWnd.error(exefile+" 不存在!")
            return False
        return self._unique_check() if self.context["isUniqueCheckExpected"] == "yes" else True

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
        rundir = self.context["rundir"]
        cwd = os.getcwd()
        os.chdir(rundir)
        exename = self.context["exefile"]
        self.proc = self._launchSubprocess(exename)
        os.chdir(cwd)
        if self.proc is None: return
        self.logWnd.info("进程 {} 正在运行".format(exename))
