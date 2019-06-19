from tkinter import Frame
from tkinter import TOP, X, BOTH, BOTTOM
from .control_btn import ControlButton

class ControlPanel(Frame):
    def __init__(self, parent=None, servers={}, clients={}):
        Frame.__init__(self, parent)
        self.servers = servers
        self.clients = clients
        self.clientCtrlBtns = {}
        self.serverCtrlBtns = {}
        self.serverCtrlPanel = Frame(self)
        self.clientCtrlPanel = Frame(self)
        self._deploy_server_control_panel(self.serverCtrlPanel)
        self._deploy_client_control_panel(self.clientCtrlPanel)
        self.serverCtrlPanel.pack(side=TOP, fill=BOTH, expand=1)
        self.clientCtrlPanel.pack(side=BOTTOM, fill=BOTH, expand=1)
    
    def _deploy_client_control_panel(self, frame):
        for clientName in self.clients:
            if clientName in self.clientCtrlBtns: continue
            self.clientCtrlBtns[clientName] = ControlButton(frame, clientName, "", None)
            self.clientCtrlBtns[clientName].pack(side=TOP, fill=X, expand=1)
    
    def _deploy_server_control_panel(self, frame):
        for serverName in self.servers:
            if serverName in self.serverCtrlBtns: continue
            self.serverCtrlBtns[serverName] = ControlButton(frame, serverName, "", None)
            self.serverCtrlBtns[serverName].pack(side=TOP, fill=X, expand=1)

    def get_server_control_buttons(self):
        return self.serverCtrlBtns
    
    def get_client_control_buttons(self):
        return self.clientCtrlBtns