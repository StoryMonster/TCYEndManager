import os
import subprocess
import time
import threading
from .concrete_server_controler import ConcreteServerControler
from .concrete_client_controler import ConcreteClientControler


class Controler(object):
    def __init__(self, servers, clients):
        self.view = None
        self.servers = servers
        self.clients = clients
        self.controlers = {}
        self.isSyncLogExpected = True
        self.syncLogThread = threading.Thread(target=self._syncLogBetweenScreenAndFile)

    def __exit__(self, *args):
        self.close()
    
    def close(self):
        self.isSyncLogExpected = False
        self.syncLogThread.join()
        for client in self.clients:
            self.closeControler(client)
        for server in self.servers:
            self.closeControler(server)

    def _syncLogBetweenScreenAndFile(self):
        while self.isSyncLogExpected:
            for controler in self.controlers:
                if self.controlers[controler] is None: continue
                self.controlers[controler].syncLogFromFile()
            time.sleep(0.5)

    def loadView(self, view):
        self.view = view
        for server in self.servers:
            winHandler = view.logAreas[server] if server in view.logAreas else view.commonWindow
            self.controlers[server] = ConcreteServerControler(server, self.servers[server], winHandler)
        for client in self.clients:
            winHandler = view.logAreas[client] if client in view.logAreas else view.commonWindow
            self.controlers[client] = ConcreteClientControler(client, self.clients[client], winHandler)
        self.syncLogThread.start()
    
    def closeControler(self, name):
        if self.controlers[name] is not None:
            self.controlers[name].close()
            self.controlers[name] = None

    def onClickServerButton(self, serverName, isExpectToStart):
        if (serverName not in self.servers) or (self.controlers[serverName] is None): return
        if isExpectToStart: self.controlers[serverName].run()
        else: self.controlers[serverName].stop()

    def onClickClientButton(self, clientName, isExpectToStart):
        if (clientName not in self.clients) or (self.controlers[clientName] is None): return
        if isExpectToStart: self.controlers[clientName].run()
        else: self.controlers[clientName].stop()

    def onMainWindowClose(self):
        self.close()

