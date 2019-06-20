from tkinter import Menu
from .build_menu import BuildMenu

class MenuBar(Menu):
    def __init__(self, parent=None, servers={}, clients={}, others={}):
        Menu.__init__(self, parent)
        self.buildMenu = BuildMenu(self, servers)
        self.add_cascade(label="构建", menu=self.buildMenu)
    
    def loadBuildControler(self, controler):
        self.buildMenu.loadControler(controler)