from tkinter import Menu


class BuildMenu(Menu):
    def __init__(self, parent=None, servers={}):
        Menu.__init__(self, parent, tearoff=0, bd=5)
        self.callback = None
        self.servers = servers
        for serverName in self.servers:
            self._add_item(serverName)
            
    
    def loadCallback(self, callback):
        self.callback = callback

    def _add_item(self, serverName):
        self.add_command(label="编译{}".format(serverName), command=lambda: self._onBuildServer(serverName))

    def _onBuildServer(self, serverName):
        if self.callback is None: return
        self.callback(serverName)
