import os
import subprocess
from model.common.file_reader import FileReader
from model.common.file_writer import FileWriter

class ServerManager(object):
    def __init__(self, name, context, others, logWnd):
        self.name = name
        self.exe_file = context["exe_file"]
        self.run_dir = os.path.dirname(os.path.abspath( self.exe_file))
        self.logWnd = logWnd
        self.fileWriter = None
        self.fileReader = None
        self.proc = None
        self.logfile = os.path.join(others["logdir"], "{}.log".format(name))

    def __del__(self, *args):
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

    def _unique_check(self):
        try:
            from psutil import process_iter
            exefile = self.exe_file
            exefile = exefile if "\\" not in exefile else exefile[exefile.rfind("\\")+1:]
            for proc in process_iter():
                if proc.name() == exefile:
                    self.logWnd.warn("系统中存在{}正在执行，请确认(pid: {})".format(exefile, proc.pid))
                    return True
            return True
        except ImportError:
            self.logWnd.warn("psutil包不存在，将不会检查是否已经有该程序在执行。可在控制台执行pip install psutil安装")
            return True

    def _precheck(self):
        if self.isRunning():
            self.logWnd.error(self.name + " 还在运行中")
            return False
        if not os.path.exists(self.run_dir):
            self.logWnd.error("执行路径 {} 不存在".format(self.run_dir))
            return False
        if not os.path.isfile(self.exe_file):
            self.logWnd.error(self.exe_file+" 不存在!")
            return False
        return self._unique_check()

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
            self.logWnd.error("不再支持Python 2.x")
            return None
        if sys.version_info.minor <= 6:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, startupinfo=startupinfo)
        else: return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)

    def run(self):
        if not self._precheck(): return
        if not self._startupLogEnvironment(): return
        cwd = os.getcwd()
        os.chdir(self.run_dir)
        self.proc = self._launchSubprocess(self.exe_file)
        os.chdir(cwd)
        if self.proc is None: return
        self.logWnd.info("进程 {} 正在运行".format(self.name))
