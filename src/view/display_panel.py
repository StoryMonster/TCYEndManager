from tkinter import Frame
from tkinter import X, Y, TOP, RIGHT, HORIZONTAL, VERTICAL, BOTH
from .output_box import OutputBox

class DisplayPanel(Frame):
    def __init__(self, parent=None, servers={}, clients={}):
        Frame.__init__(self, parent)
        self.servers = servers
        self.clients = clients
        self.dispAreas = {}
        self.commonWindow = None
        self._deploy_components()
    
    def _deploy_components(self):
        counter = 0
        for server in self.servers:
            if server in self.dispAreas or self.servers[server]["isWindowExpected"] == "no": continue
            self.dispAreas[server] = OutputBox(self, server)
            self.dispAreas[server].grid(row=int(counter/3), column=counter%3)
            counter += 1
        for client in self.clients:
            if client in self.dispAreas or self.clients[client]["isWindowExpected"] == "no": continue
            self.dispAreas[client] = OutputBox(self, client)
            self.dispAreas[client].grid(row=int(counter/3), column=counter%3)
            counter += 1
        self.commonWindow = OutputBox(self, "Common Window")
        self.commonWindow.grid(row=int(counter/3), column=counter%3)
    
    def get_common_window(self):
        return self.commonWindow

    def get_other_windows(self):
        return self.dispAreas