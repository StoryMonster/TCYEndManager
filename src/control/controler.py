import os
import subprocess
import time
import threading
from model.server_names import *
from model.server_contexts import serverContexts
from model.client_names import *
from model.client_contexts import clientContexts
from .concrete_server_controler import ConcreteServerControler
from .concrete_client_controler import ConcreteClientControler


class Controler(object):
    def __init__(self):
        self.view = None
        self.serverContexts = serverContexts
        self.clientContexts = clientContexts
        self.controlers = {}
        self.syncLogThread = threading.Thread(target=self._syncLogBetweenScreenAndFile)

    def __exit__(self, *args):
        self.close()
    
    def close(self):
        for client in CLIENT_NAMES:
            self.closeClient(client)
        for server in SERVER_NAMES:
            self.closeServer(server)
    
    def _syncLogBetweenScreenAndFile(self):
        while True:
            for controler in self.controlers:
                if self.controlers[controler] is None: continue
                self.controlers[controler].syncLogFromFile()
            time.sleep(0.5)

    def loadView(self, view):
        self.view = view
        for serverName in SERVER_NAMES:
            self.controlers[serverName] = ConcreteServerControler(serverName, self.serverContexts[serverName], view.logAreas[serverName])
        for clientName in CLIENT_NAMES:
            self.controlers[clientName] = ConcreteClientControler(clientName, self.clientContexts[clientName], view.logAreas[clientName])
        self.syncLogThread.start()

    def closeServer(self, serverName):
        if self.controlers[serverName] is not None:
            self.controlers[serverName].close()
            self.controlers[serverName] = None

    def closeClient(self, clientName):
        if self.controlers[clientName] is not None:
            self.controlers[clientName].close()
            self.controlers[clientName] = None

    def onClickServerButton(self, serverName, isExpectToStart):
        if (serverName not in SERVER_NAMES) or (self.controlers[serverName] is None): return
        if isExpectToStart: self.controlers[serverName].run()
        else: self.controlers[serverName].stop()

    def onClickClientButton(self, clientName, isExpectToStart):
        if (clientName not in CLIENT_NAMES) or (self.controlers[clientName] is None): return
        if isExpectToStart: self.controlers[clientName].run()
        else: self.controlers[clientName].stop()
    
    def onMainWindowClose(self):
        self.close()

