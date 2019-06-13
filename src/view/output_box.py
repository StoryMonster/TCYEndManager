from tkinter import Text, Label, Scrollbar, Frame
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, X, RIGHT, Y, BOTH, TOP

class OutputBox(Frame):
    def __init__(self, parent=None, boxName=""):
        Frame.__init__(self, parent)
        self.lbl = Label(self, text=boxName)
        self.xScrollarBar = Scrollbar(self, orient=HORIZONTAL)
        self.xScrollarBar.pack(side=BOTTOM, fill=X)
        self.yScrollarBar = Scrollbar(self, orient=VERTICAL)
        self.yScrollarBar.pack(side=RIGHT, fill=Y)
        self.textArea = Text(self, bd=5, wrap="none", xscrollcommand=self.xScrollarBar.set, yscrollcommand=self.yScrollarBar.set)
        self.xScrollarBar.config(command=self.textArea.xview)
        self.yScrollarBar.config(command=self.textArea.yview)
        self.lbl.pack(expand=1, fill=X, side=TOP)
        self.textArea.pack(expand=1, fill=BOTH, side=TOP)

    def write(self, text):
        self.textArea.insert("end", text)
        self.textArea.see("end")
    
    def writeline(self, text):
        self.write(text+"\n")
        
    def writelines(self, lines):
        for line in lines:
            self.writeline(line.rstrip())

    def clear(self):
        self.textArea.delete(1.0, "end")
