import subprocess
import os
import re
import time
from model.common.file_writer import FileWriter
from model.common.file_reader import FileReader

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
    def __init__(self, server, compilerContext, wnd):
        self.server = server
        self.compilerContext = compilerContext
        self.wnd = wnd
        self.proc = None
        self.serverName = self.server["name"]
        self.logfile = os.path.abspath(self.compilerContext["logfile"])
        self.fileReader = FileReader(self.logfile)

    def stop(self):
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.wnd.warn("未能成功结束进程："+self.serverName)
            self.proc = None
        if self.fileReader is not None:
            self.fileReader.close()
            self.fileReader = None

    def __exit__(self, *args):
        self.stop()

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

    def run(self):
        if not self._precheck(): return
        self.wnd.info("开始编译："+self.serverName)
        vcvarsall = os.path.join(self.compilerContext["path"], "VC/vcvarsall.bat")
        projectdir = self.server["projectdir"]
        sln, vcxproj = getProjectKeyFiles(projectdir)
        buildmode =  recorgnizeBuildMode(self.compilerContext["compilemode"])
        cmd = f'scripts\\compiler.bat "{vcvarsall}" "{projectdir}" "{sln}" "{buildmode}" "{vcxproj}" "{self.logfile}"'
        self.proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.proc.wait()
        self.wnd.writelines(self.fileReader.readlines())
        self.wnd.info("编译完成，详细编译日志: {logfile}\n".format(logfile=self.logfile))
