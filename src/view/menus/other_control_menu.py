from tkinter import Menu


class OtherControlMenu(Menu):
    def __init__(self, parent=None):
        Menu.__init__(self, parent, tearoff=0, bd=5)

    def addItem(self, name, callback):
        self.add_command(label=name, command=callback)
