from tkinter import Frame
from tkinter import Tk, LEFT, RIGHT, BOTH, X, TOP, W, E, N, S, Y
from .display_panel import DisplayPanel
from .control_panel import ControlPanel

class MainWindow(Tk):
    def __init__(self, servers, clients):
        Tk.__init__(self)
        self.title("同城游 管理工具")
        self.servers = servers
        self.clients = clients
        self.display_panel = DisplayPanel(self, servers, clients)
        self.control_panel = ControlPanel(self, servers, clients)
        self.serverCtrlBtns = self.control_panel.get_server_control_buttons()
        self.clientCtrlBtns = self.control_panel.get_client_control_buttons()
        self.commonWindow = self.display_panel.get_common_window()
        self.dispAreas = self.display_panel.get_other_windows()
        self.controler = None
        self.control_panel.pack(side=LEFT, fill=BOTH, expand=1)
        self.display_panel.pack(side=LEFT, fill=BOTH, expand=1)

    def run(self):
        self.mainloop()

    def loadControler(self, controler):
        self.controler = controler
        for server in self.servers:
            self.serverCtrlBtns[server].loadCallBack(controler.onClickServerButton)
        for client in self.clients:
            self.clientCtrlBtns[client].loadCallBack(controler.onClickClientButton)
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)

    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()