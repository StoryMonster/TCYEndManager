from tkinter import Tk, Scrollbar
from tkinter import X, Y, TOP, RIGHT, LEFT, HORIZONTAL, VERTICAL, BOTH, BOTTOM
from .output_box import OutputBox
from .menus.menu_bar import MenuBar
import time

class MainWindow(Tk):
    def __init__(self, title, servers, clients, others={}):
        Tk.__init__(self)
        self.title(title)
        self.iconbitmap("res/head.ico")
        self.servers = servers
        self.clients = clients
        self.others = others
        self.menu = MenuBar(self, servers, clients, others)
        self.popup_menu = None
        self.config(menu=self.menu)
        self.commonWindow = None
        self.dispAreas = {}
        self.controler = None
        self._deploy_display_windows()
        self.bind("<ButtonPress-3>", self._rightClick)

    def run(self):
        self.mainloop()

    def loadControler(self, controler):
        self.controler = controler
        self.menu.registerOtherItems("清空全部窗口", self._onClearWindows)
        self.menu.registerOtherItems("停止全部进程", self._onStopControler)
        if "quick_launch_servers" in self.others:
            self.menu.registerOtherItems("服务器一键启动", self._onQuickLaunchServers)
        self.menu.registerOtherItems("启动全部客户端", self._onQuickLaunchClients)
        self.menu.registerBuilderCallback(self._onClickServerBuilders)
        self.menu.registerClientsCallback(self._onClickClients)
        self.menu.registerServersCallback(self._onClickServers)
        self.popup_menu = self.menu.otherMenu
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)

    def _deploy_display_windows(self):
        window_num = 1
        for server in self.servers:
            if self.servers[server]["is_window_expected"] == "yes":
                self.dispAreas[server] = OutputBox(self, server, self.servers[server]["exe_file"])
                window_num += 1
        self.dispAreas["Common Window"] =  OutputBox(self, "Common Window", "")
        self.commonWindow = self.dispAreas["Common Window"]
        if window_num == 1:
            self.commonWindow.pack(fill=BOTH, expand=1)
        elif window_num == 2 or window_num == 4:
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            counter = 0
            for name in self.dispAreas:
                if counter % 2 == 0: self.rowconfigure(int(counter/2), weight=1)
                self.dispAreas[name].grid(row=int(counter/2), column=counter%2, sticky="NSEW")
                counter += 1
        else:
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)
            counter = 0
            for name in self.dispAreas:
                if counter % 3 == 0: self.rowconfigure(int(counter/3), weight=1)
                self.dispAreas[name].grid(row=int(counter/3), column=counter%3, sticky="NSEW")
                counter += 1

    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()

    def _onClearWindows(self):
        for wndName in self.dispAreas:
            if self.dispAreas[wndName] is not None:
                self.dispAreas[wndName].clear()
    
    def _onStopControler(self):
        if self.controler is None: return
        self.controler.stopAllProcesses()
        self.menu.resetServersStatus()
        self.menu.resetClientsStatus()

    def _onClickServers(self, serverName, toRunServer):
        if self.controler is None: return
        self.controler.onClickServerButton(serverName, toRunServer)

    def _onClickClients(self, clientName, toRunClient):
        if self.controler is None: return
        self.controler.onClickClientButton(clientName, toRunClient)

    def _onClickServerBuilders(self, serverName):
        self.controler.compileServer(serverName)

    def _rightClick(self, event):
        if self.popup_menu is None or event.widget != self: return
        self.popup_menu.post(event.x_root, event.y_root)

    def _onQuickLaunchServers(self):
        for serverName in self.others["quick_launch_servers"]["launch_queue"].split(";"):
            if self.menu.serversMenu.getServerButtonStatus(serverName) == "selected":
                self.menu.serversMenu.clickServer(serverName)
            self.menu.serversMenu.clickServer(serverName)

    def _onQuickLaunchClients(self):
        for client in self.clients:
            if self.menu.clientsMenu.getClientsButtonStatus(client) == "selected":
                self.menu.clientsMenu.clickClient(client)
            self.menu.clientsMenu.clickClient(client)
            time.sleep(2)
