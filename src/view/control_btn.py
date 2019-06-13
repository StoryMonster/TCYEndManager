from tkinter import Button, Label, Frame
from tkinter import StringVar, X, BOTH


class ControlButton(Frame):
    def __init__(self, parent=None, btnName="", description="", callback=None):
        Frame.__init__(self, parent)
        self.btnName = btnName
        self.btnText = StringVar()
        self.btnText.set(f"Start {btnName}")
        self.btn = Button(self, textvariable=self.btnText, command=self._onClick)
        self.btn.pack(fill=X)
        self.description = StringVar()
        self.description.set(description)
        self.descLbl = Label(self, textvariable=self.description)
        self.descLbl.pack(fill=X)
        self.callback = callback

    def loadCallBack(self, callback):
        self.callback = callback
    
    def _onClick(self):
        if self.callback is None: return
        if self.btnText.get()[0:5] == "Start":
            self.btnText.set("Stop  " + self.btnName)
            self.callback(self.btnName, True)
            return
        self.btnText.set("Start " + self.btnName)
        self.callback(self.btnName, False)
