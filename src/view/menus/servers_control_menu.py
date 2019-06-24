from tkinter import Menu, BooleanVar

class ServersControlMenu(Menu):
    def __init__(self, parent=None, servers={}):
        Menu.__init__(self, parent, tearoff=0, bd=5)
        self.servers = servers
        self.servers_status = {}
        self.callback = None
        for serverName in self.servers:
            self._add_item(serverName)

    def loadCallback(self, callback):
        self.callback = callback

    def _add_item(self, serverName):
        self.servers_status[serverName] = BooleanVar()
        self.servers_status[serverName].set(False)
        self.add_checkbutton(label="运行"+serverName, command=lambda: self._onClickServer(serverName), onvalue=True, offvalue=False, variable=self.servers_status[serverName])

    def _onClickServer(self, serverName):
        if self.callback is None: return
        self.callback(serverName, self.servers_status[serverName].get())
    
    def resetStatus(self):
        for serverName in self.servers_status:
            self.servers_status[serverName].set(False)