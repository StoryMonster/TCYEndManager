from tkinter import Tk, LEFT, BOTH
from .display_panel import DisplayPanel
from .control_panel import ControlPanel
from .menus.menu_bar import MenuBar

class MainWindow(Tk):
    def __init__(self, servers, clients, others={}):
        Tk.__init__(self)
        self.title("同城游 管理工具")
        self.servers = servers
        self.clients = clients
        self.others = others
        self.menu = MenuBar(self, servers, clients, others)
        self.config(menu=self.menu)
        self.display_panel = DisplayPanel(self, servers, clients)
        self.control_panel = ControlPanel(self, servers, clients)
        self._add_general_control_buttons()
        self.serverCtrlBtns = self.control_panel.get_server_control_buttons()
        self.clientCtrlBtns = self.control_panel.get_client_control_buttons()
        self.commonWindow = self.display_panel.get_common_window()
        self.dispAreas = self.display_panel.get_other_windows()
        self.controler = None
        self.control_panel.pack(side=LEFT, fill=BOTH, expand=1)
        self.display_panel.pack(side=LEFT, fill=BOTH, expand=1)

    def _add_general_control_buttons(self):
        self.control_panel.add_general_control_button("Clear Windows", self._onClearWindows)

    def run(self):
        self.mainloop()

    def loadControler(self, controler):
        self.controler = controler
        for server in self.servers:
            self.serverCtrlBtns[server].loadCallBack(controler.onClickServerButton)
        for client in self.clients:
            self.clientCtrlBtns[client].loadCallBack(controler.onClickClientButton)
        self.menu.loadBuildControler(self.controler.getCompiler())
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)

    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()

    def _onClearWindows(self):
        self.commonWindow.clear()
        for wndName in self.dispAreas:
            self.dispAreas[wndName].clear()
