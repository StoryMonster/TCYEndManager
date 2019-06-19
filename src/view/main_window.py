from tkinter import Frame
from tkinter import Tk, LEFT, RIGHT, BOTH, X, TOP, W, E, N, S
from .output_box import OutputBox
from .control_btn import ControlButton

def getExpectCols(servers, clients):
    endNumExpectWindow = 1          ## reserve for common window
    for server in servers:
        if servers[server]["isWindowExpected"] == "yes":
            endNumExpectWindow += 1
    for client in clients:
        if clients[client]["isWindowExpected"] == "yes":
            endNumExpectWindow += 1
    if endNumExpectWindow <= 3: return endNumExpectWindow
    else:
        half = endNumExpectWindow/2
        if half == int(half): return int(half)
        else: return int(half) + 1

class MainWindow(Tk):
    def __init__(self, servers, clients):
        Tk.__init__(self)
        self.title("同城游 管理工具")
        self.servers = servers
        self.clients = clients
        self.svrCtrlBtns = {}
        self.clientCtrlBtns = {}
        self.logAreas = {}
        self.controler = None
        self.commonWindow = None
        self.outputFrame = Frame(self)
        self.controlFrame = Frame(self)
        self._deployControlFrame(self.controlFrame)
        self._deployDisplayFrame(self.outputFrame)
        self.controlFrame.pack(side=LEFT, padx=0)
        self.outputFrame.pack(side=LEFT, fill=BOTH, expand=1)

    def run(self):
        self.mainloop()

    def loadControler(self, controler):
        self.controler = controler
        for server in self.servers:
            self.svrCtrlBtns[server].loadCallBack(controler.onClickServerButton)
        for client in self.clients:
            self.clientCtrlBtns[client].loadCallBack(controler.onClickClientButton)
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)
    
    def _deployControlFrame(self, frame):
        serverControlFrame = Frame(frame)
        clientControlFrame = Frame(frame)
        self._deployClientControlFrame(clientControlFrame)
        self._deployServerControlFrame(serverControlFrame)
        serverControlFrame.grid(row=0, column=0)
        clientControlFrame.grid(row=1, column=0)

    def _deployServerControlFrame(self, frame):
        for serverName in self.servers:
            if serverName in self.svrCtrlBtns: continue
            self.svrCtrlBtns[serverName] = ControlButton(frame, serverName, "", None)
            self.svrCtrlBtns[serverName].pack(side=TOP, fill=X, expand=1)
    
    def _deployClientControlFrame(self, frame):
        for clientName in self.clients:
            if clientName in self.clientCtrlBtns: continue
            self.clientCtrlBtns[clientName] = ControlButton(frame, clientName, "", None)
            self.clientCtrlBtns[clientName].pack(side=TOP, fill=X, expand=1)

    def _deployDisplayFrame(self, frame):
        counter = 0
        for server in self.servers:
            if server in self.logAreas or self.servers[server]["isWindowExpected"] == "no": continue
            self.logAreas[server] = OutputBox(frame, server)
            self.logAreas[server].grid(row=int(counter/3), column=counter%3)
            counter += 1
        for client in self.clients:
            if client in self.logAreas or self.clients[client]["isWindowExpected"] == "no": continue
            self.logAreas[client] = OutputBox(frame, client)
            self.logAreas[client].grid(row=int(counter/3), column=counter%3)
            counter += 1
        self.commonWindow = OutputBox(frame, "Common Window")
        self.commonWindow.grid(row=int(counter/3), column=counter%3)

    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()