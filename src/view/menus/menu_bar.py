from tkinter import Menu
from .build_menu import BuildMenu
from .clients_control_menu import ClientsControlMenu
from .servers_control_menu import ServersControlMenu
from .other_control_menu import OtherControlMenu

class MenuBar(Menu):
    def __init__(self, parent=None, servers={}, clients={}, others={}):
        Menu.__init__(self, parent)
        self.buildMenu = None
        if "compiler" in others:
            self.buildMenu = BuildMenu(self, servers)
            self.add_cascade(label="构建", menu=self.buildMenu)
        self.clientsMenu = ClientsControlMenu(self, clients)
        self.serversMenu = ServersControlMenu(self, servers)
        self.otherMenu = OtherControlMenu(self)
        self.add_cascade(label="客户端", menu=self.clientsMenu)
        self.add_cascade(label="服务器", menu=self.serversMenu)
        self.add_cascade(label="其他", menu=self.otherMenu)
    
    def registerBuilderCallback(self, callback):
        if self.buildMenu is None: return
        self.buildMenu.loadCallback(callback)

    def registerClientsCallback(self, callback):
        self.clientsMenu.loadCallback(callback)

    def registerServersCallback(self, callback):
        self.serversMenu.loadCallback(callback)

    def registerOtherItems(self, name, callback):
        self.otherMenu.addItem(name, callback)

    def resetServersStatus(self):
        self.serversMenu.resetStatus()

    def resetClientsStatus(self):
        self.clientsMenu.resetStatus()

        
