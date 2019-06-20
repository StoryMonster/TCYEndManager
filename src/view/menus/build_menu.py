from tkinter import Menu


class BuildMenu(Menu):
    def __init__(self, parent=None, servers={}, controler=None):
        Menu.__init__(self, parent, tearoff=0)
        self.controler = controler
        self.servers = servers
        for serverName in self.servers:
            if self.servers[serverName]["isCompileEnable"].lower() == "no": continue
            self._add_item(serverName)
            
    
    def loadControler(self, controler):
        self.controler = controler

    def _add_item(self, serverName):
        self.add_command(label=f"build {serverName}", command=lambda: self._onBuildServer(serverName))

    def _onBuildServer(self, serverName):
        if self.controler is None: return
        self.controler.compileServer(serverName)
