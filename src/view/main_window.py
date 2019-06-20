from tkinter import Tk, Scrollbar
from tkinter import X, Y, TOP, RIGHT, LEFT, HORIZONTAL, VERTICAL, BOTH, BOTTOM
from .output_box import OutputBox
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
        self.commonWindow = None
        self.dispAreas = {}
        self.controler = None
        #self._deploy_scroller_bar()
        self._deploy_display_windows()
        #self.pack()

    def run(self):
        self.mainloop()

    def loadControler(self, controler):
        self.controler = controler
        self.menu.registerOtherItems("清空全部窗口", self._onClearWindows)
        self.menu.registerOtherItems("停止全部进程", self._onStopControler)
        self.menu.registerBuilderCallback(self._onClickServerBuilders)
        self.menu.registerClientsCallback(self._onClickClients)
        self.menu.registerServersCallback(self._onClickServers)
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)

    def _deploy_display_windows(self):
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

    def _deploy_scroller_bar(self):
        xScrollarBar = Scrollbar(self, orient=HORIZONTAL)
        xScrollarBar.pack(side=BOTTOM, fill=X)
        yScrollarBar = Scrollbar(self, orient=VERTICAL)
        yScrollarBar.pack(side=RIGHT, fill=Y)
        #self.config(xscrollcommand=xScrollarBar.set, yscrollcommand=yScrollarBar.set)
        xScrollarBar.config(command=self.xview)
        yScrollarBar.config(command=self.yview)

    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()

    def _onClearWindows(self):
        if self.commonWindow is not None:
            self.commonWindow.clear()
        for wndName in self.dispAreas:
            if self.dispAreas[wndName] is not None:
                self.dispAreas[wndName].clear()
    
    def _onStopControler(self):
        if self.controler is None: return
        self.controler.stopAllProcesses()

    def _onClickServers(self, serverName, toRunServer):
        if self.controler is None: return
        self.controler.onClickServerButton(serverName, toRunServer)

    def _onClickClients(self, clientName, toRunClient):
        if self.controler is None: return
        self.controler.onClickClientButton(clientName, toRunClient)

    def _onClickServerBuilders(self, serverName):
        self.controler.compileServer(serverName)
