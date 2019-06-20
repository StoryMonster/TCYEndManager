from tkinter import Button

class GeneralCtrlBtn(Button):
    def __init__(self, parent=None, btnName="", callback=None):
        Button.__init__(self, parent, text=btnName, command=self._onClick)
        self.btnName = btnName
        self.callback = callback

    def loadCallBack(self, callback):
        self.callback = callback
    
    def _onClick(self):
        if self.callback is None: return
        self.callback()
