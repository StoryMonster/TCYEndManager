import os
import subprocess
import shutil
from model.common.file_reader import FileReader
from model.common.file_writer import FileWriter

class ClientManager(object):
    def __init__(self, name, context, others, logWnd):
        self.name = name
        self.context = context
        self.script_path = others["simulator"]["script"]
        self.simulator = others["simulator"]["path"]
        self.run_dir = os.path.dirname(os.path.abspath(self.simulator))
        self.account = context["account"]
        self.password = context["password"]
        self.config_file = os.path.join(self.run_dir, "windows.ini")
        self.is_console_expected = context["is_console_expected"].lower() == "yes"
        self.logWnd = logWnd
        self.fileWriter = None
        self.fileReader = None
        self.logfile = os.path.join(others["logdir"], "{}.log".format(name))
        self.proc = None

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

    def stop(self):
        self._closeLogFileHandlers()
        self.logWnd.info("停止进程 "+self.name)
        if self.proc is not None:
            try:
                os.kill(self.proc.pid, 9)
            except PermissionError:
                self.logWnd.warn("未能杀死进程 {name} 或者该进程不存在".format(name=self.name))
            self.proc = None

    def syncLogToScreenFromFile(self):
        if self.fileReader is None: return
        try:
            self.logWnd.writelines(self.fileReader.readlines())
        except Exception as e:
            self.logWnd.warn(str(e))

    def _precheck(self):
        if self.isRunning():
             self.logWnd.error(self.name+" 还在运行中")
             return False
        if not os.path.isdir(self.run_dir):
            self.logWnd.error("执行路径不存在: "+self.run_dir)
            return False
        if (not os.path.isfile(self.simulator)) or (not os.path.isfile(self.config_file)):
            self.logWnd.error("模拟器 {} 或者配置文件 {} 不存在!".format(self.simulator, self.config_file))
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
            self.logWnd.error("不再支持Python 2.x")
            return None
        if sys.version_info.minor <= 6:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, startupinfo=startupinfo)
        else: return subprocess.Popen(cmd, stdout=self.fileWriter, stderr=self.fileWriter, creationflags=subprocess.CREATE_NO_WINDOW)

    def _write_client_information_into_config_file(self):
        lines = []
        with open(self.config_file, "r", encoding="utf-8") as fd:
            lines = fd.readlines()
        is_read_user_info = False
        NECCESSARY_USER_INFO_ITEM_NUM = 2
        modified_user_info_item_num = 0
        for i in range(len(lines)):
            if lines[i].rstrip() == "[user]":
                is_read_user_info = True
                continue
            if is_read_user_info:
                if lines[i].find("name=") == 0:
                    lines[i] = "name=" + self.account
                    modified_user_info_item_num += 1
                elif lines[i].find("password=") == 0:
                    lines[i] = "password=" + self.password
                    modified_user_info_item_num += 1
                if NECCESSARY_USER_INFO_ITEM_NUM == modified_user_info_item_num: break
        FileWriter(self.config_file, encoding="utf-8").writelines(lines)

    def run(self):
        if not self._precheck(): return
        if not self._startupLogEnvironment(): return
        self._write_client_information_into_config_file()
        cwd = os.getcwd()
        os.chdir(self.run_dir)
        self.proc = self._launchSubprocess("{} {} -workdir {}".format(self.simulator, "" if self.is_console_expected else "-console disable", self.script_path))
        os.chdir(cwd)
        if self.proc is None: return
        self.logWnd.info("进程 {} 开始运行".format(self.name))
