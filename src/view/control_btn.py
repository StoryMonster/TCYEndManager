from tkinter import Button, Label, Frame
from tkinter import StringVar, X, BOTH


class ControlButton(Frame):
    def __init__(self, parent=None, btnName="", description="", callback=None):
        Frame.__init__(self, parent)
        self.btnName = btnName
        self.isRunningStatus = True
        self.btnText = StringVar()
        self._autoRotateButton()
        self.btn = Button(self, textvariable=self.btnText, command=self._onClick, bd=4)
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
        self._autoRotateButton()
        self.callback(self.btnName, self.isRunningStatus)

    def _autoRotateButton(self):
        self.isRunningStatus = not self.isRunningStatus
        self.btnText.set(("启动" if self.isRunningStatus == False else "停止") + self.btnName)
    
    def changeButtonStatus(self, status):
        self.isRunningStatus = status
        self.btnText.set(("启动" if self.isRunningStatus == False else "停止") + self.btnName)
        
