from tkinter import Menu

class OutputBoxPopupMenu(Menu):
    def __init__(self, parent=None):
        Menu.__init__(self, parent, tearoff=0)

    def show(self, x, y):
        self.post(x=x, y=y)

    def register(self, name, callback):
        self.add_command(label=name, command=callback)
