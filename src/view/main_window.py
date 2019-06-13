from tkinter import Frame
from tkinter import Tk, LEFT, RIGHT, BOTH, X, TOP, W, E, N, S
from .output_box import OutputBox
from .control_btn import ControlButton
from model.server_names import *
from model.client_names import *


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.svrCtrlBtns = {}
        self.clientCtrlBtns = {}
        self.logAreas = {}
        self.controler = None
        self.title("同城游 服务器管理")
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
        for serverName in SERVER_NAMES:
            self.svrCtrlBtns[serverName].loadCallBack(controler.onClickServerButton)
        for clientName in CLIENT_NAMES:
            self.clientCtrlBtns[clientName].loadCallBack(controler.onClickClientButton)
        self.protocol("WM_DELETE_WINDOW", self._onMainWindowClose)
    
    def _deployControlFrame(self, frame):
        serverControlFrame = Frame(frame)
        clientControlFrame = Frame(frame)
        self._deployClientControlFrame(clientControlFrame)
        self._deployServerControlFrame(serverControlFrame)
        serverControlFrame.grid(row=0, column=0)
        clientControlFrame.grid(row=1, column=0)

    def _deployServerControlFrame(self, frame):
        for serverName in SERVER_NAMES:
            if serverName in self.svrCtrlBtns: continue
            self.svrCtrlBtns[serverName] = ControlButton(frame, serverName, "", None)
            self.svrCtrlBtns[serverName].pack(side=TOP, fill=X, expand=1)
    
    def _deployClientControlFrame(self, frame):
        for clientName in CLIENT_NAMES:
            if clientName in self.clientCtrlBtns: continue
            self.clientCtrlBtns[clientName] = ControlButton(frame, clientName, "", None)
            self.clientCtrlBtns[clientName].pack(side=TOP, fill=X, expand=1)
    
    def _deployDisplayFrame(self, frame):
        row, col = 0, 0
        for serverName in SERVER_NAMES:
            if serverName in self.logAreas: continue
            self.logAreas[serverName] = OutputBox(frame, serverName)
            self.logAreas[serverName].grid(row=row, column=col)
            col += 1
            if col > 2:
                row += 1
                col = 0
        for clientName in CLIENT_NAMES:
            if clientName in self.logAreas: continue
            self.logAreas[clientName] = OutputBox(frame, clientName)
            self.logAreas[clientName].grid(row=row, column=col)
            col += 1
            if col > 2:
                row += 1
                col = 0
    
    def _onMainWindowClose(self):
        self.controler.close()
        self.destroy()