import subprocess
import os
import re
import time
from model.common.file_reader import FileReader
from model.common.file_writer import FileWriter

def getProjectKeyFiles(projectdir):
    if not os.path.isdir(projectdir):
        return None, None
    files = os.listdir(projectdir)
    sln, vcxproj = None, None
    patterns = [ r".+\.sln$", r".+\.vcxproj$"]
    for filename in files:
        if re.match(patterns[0], filename):
            sln = filename
        elif re.match(patterns[1], filename):
            vcxproj = filename
    return sln, vcxproj

def recorgnizeBuildMode(originalBuildMode):
    if originalBuildMode.lower() == "release":
        return "Release"
    return "Debug"

def toWinPath(str):
    return str.replace("/", "\\")

class ServerCompiler(object):
    def __init__(self, serverName, serverContext, compilerContext, wnd):
        self.server = serverContext
        self.compilerContext = compilerContext
        self.wnd = wnd
        self.proc = None
        self.serverName = serverName
        self.logfile = os.path.abspath(self.compilerContext["logfile"])
        self.fileWriter = None
        self.fileReader = None

    def stop(self):
        if self.fileWriter is not None:
            self.fileWriter.close()
            self.fileWriter = None
        if self.fileReader is not None:
            self.fileReader.close()
            self.fileReader = None
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.wnd.warn("未能成功结束进程："+self.serverName)
            self.proc = None

    def __exit__(self, *args):
        self.stop()

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        try:
            lines = self.fileReader.readlines()
            self.wnd.writelines(lines)
        except Exception as e:
            self.wnd.warn(str(e))

    def isRunning(self):
        return self.proc is not None

    def _precheck(self):
        vcvarsall = os.path.join(self.compilerContext["path"], "VC/vcvarsall.bat")
        if not os.path.isfile(vcvarsall):
            self.wnd.error("未找到编译器，无法编译 "+self.serverName)
            return False
        sln, vcxproj = getProjectKeyFiles(self.server["projectdir"])
        if sln is None or vcxproj is None:
            self.wnd.error("工程中未发现.sln文件或者.vcxproj文件，无法编译"+self.serverName)
            return False
        return True

    def _startupLogEnvironment(self):
        try:
            self.fileWriter = FileWriter(self.logfile)
            self.fileReader = FileReader(self.logfile)
            return True
        except IOError as e:
            self.wnd.error(str(e))
            self.wnd.error("无法启动编译, 因为创建或读取日志文件({})出错".format(self.name))
            return False

    def _launchSubprocess(self, cmd):
        import sys
        if sys.version_info.major < 3:
            self.wnd.error("不再支持Python 3.0以下版本")
            return None
        if sys.version_info.minor <= 5: return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter)
        else: return subprocess.Popen(cmd,  stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)

    def run(self):
        if not self._precheck(): return
        if not self._startupLogEnvironment(): return
        self.wnd.info("开始编译："+self.serverName)
        vcvarsall = os.path.join(self.compilerContext["path"], "VC/vcvarsall.bat")
        projectdir = self.server["projectdir"]
        sln, vcxproj = getProjectKeyFiles(projectdir)
        buildmode =  recorgnizeBuildMode(self.compilerContext["compilemode"])
        cmd = 'scripts\\compiler.bat "{}" "{}" "{}" "{}" "{}"'.format(vcvarsall, projectdir, sln, buildmode, vcxproj)
        self.proc = self._launchSubprocess(cmd)
        if self.proc is None:
            self.wnd.error("无法启动编译")
            self.stop()
            return
