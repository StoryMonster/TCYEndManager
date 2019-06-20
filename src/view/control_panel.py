from tkinter import Frame
from tkinter import TOP, X, BOTH, BOTTOM
from .control_btn import ControlButton
from .general_ctrl_btn import GeneralCtrlBtn

class ControlPanel(Frame):
    def __init__(self, parent=None, servers={}, clients={}):
        Frame.__init__(self, parent, bd=5)
        self.servers = servers
        self.clients = clients
        self.clientCtrlBtns = {}
        self.serverCtrlBtns = {}
        self.generalCtrlBtns = {}
        self.serverCtrlPanel = Frame(self, bd=3)
        self.clientCtrlPanel = Frame(self, bd=3)
        self.generalCtrlPanel = Frame(self, bd=3)
        self._deploy_server_control_panel(self.serverCtrlPanel)
        self._deploy_client_control_panel(self.clientCtrlPanel)
        self._deploy_general_control_panel(self.generalCtrlPanel)
        self.serverCtrlPanel.pack(side=TOP, fill=BOTH, expand=1)
        self.clientCtrlPanel.pack(side=TOP, fill=BOTH, expand=1)
        self.generalCtrlPanel.pack(side=TOP, fill=BOTH, expand=1)
    
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

    def _deploy_general_control_panel(self, frame):
        pass

    def get_server_control_buttons(self):
        return self.serverCtrlBtns

    def get_client_control_buttons(self):
        return self.clientCtrlBtns
    
    def add_general_control_button(self, btnName, btnCallback):
        self.generalCtrlBtns[btnName] = GeneralCtrlBtn(self.generalCtrlPanel, btnName, btnCallback)
        self.generalCtrlBtns[btnName].pack(side=TOP, fill=X, expand=1)