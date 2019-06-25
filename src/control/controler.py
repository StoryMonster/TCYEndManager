import time
import threading
from model.process_manager.process_type import ProcessType
from model.process_manager.process_manager_factor import create_process_manager
from model.compile.compiler import ServerCompiler


class Controler(object):
    def __init__(self, servers, clients, others):
        self.view = None
        self.servers = servers
        self.clients = clients
        self.others = others
        self.procManagers = {}
        self.isSyncLogExpected = True
        self.syncLogThread = threading.Thread(target=self._syncLogBetweenScreenAndFile)

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.syncLogThread.is_alive():
            self.isSyncLogExpected = False
            self.syncLogThread.join()
        self.closeAllProcesses()

    def compileServer(self, serverName):
        if serverName not in self.servers: return
        if self.procManagers[serverName] is not None and self.procManagers[serverName].isRunning():
            self.view.commonWindow.warn("当服务器运行时，不应该重新编译该服务器，编译进程将不会启动")
            return
        ServerCompiler(serverName, self.servers[serverName], self.others["compiler"], self.view.commonWindow).run()

    def _syncLogBetweenScreenAndFile(self):
        while self.isSyncLogExpected:
            for procName in self.procManagers:
                if self.procManagers[procName] is None: continue
                self.procManagers[procName].syncLogToScreenFromFile()
            time.sleep(0.5)

    def loadView(self, view):
        self.view = view
        for server in self.servers:
            winHandler = view.dispAreas[server] if server in view.dispAreas else view.commonWindow
            self.procManagers[server] = create_process_manager(server, ProcessType.ServerProcess, self.servers[server], winHandler)
        for client in self.clients:
            winHandler = view.dispAreas[client] if client in view.dispAreas else view.commonWindow
            self.procManagers[client] = create_process_manager(client, ProcessType.ClientProcess, self.clients[client], winHandler)
        self.syncLogThread.start()    

    def closeAllProcesses(self):
        for name in self.procManagers:
            if self.procManagers[name] is not None:
                self.procManagers[name].close()
                self.procManagers[name] = None

    def stopAllProcesses(self):
        for name in self.procManagers:
            if self.procManagers[name] is not None and self.procManagers[name].isRunning():
                self.procManagers[name].stop()

    def onClickServerButton(self, serverName, isExpectToStart):
        if (serverName not in self.servers) or (self.procManagers[serverName] is None): return
        if isExpectToStart: self.procManagers[serverName].run()
        else: self.procManagers[serverName].stop()

    def onClickClientButton(self, clientName, isExpectToStart):
        if (clientName not in self.clients) or (self.procManagers[clientName] is None): return
        if isExpectToStart: self.procManagers[clientName].run()
        else: self.procManagers[clientName].stop()

    def onMainWindowClose(self):
        self.close()
