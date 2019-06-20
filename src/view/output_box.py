from tkinter import Text, Label, Scrollbar, Frame
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, X, RIGHT, Y, BOTH, TOP

class OutputBox(Frame):
    def __init__(self, parent=None, boxName=""):
        Frame.__init__(self, parent, bg="grey")
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
        self.textArea.tag_configure("WARN_TEXT",background="blue", foreground="yellow")
        self.textArea.tag_configure("ERROR_TEXT", background="blue", foreground="red")

    def write(self, text):
        self.textArea.insert("end", text)
        self.textArea.see("end")

    def writeline(self, text):
        self.write(text+"\n")

    def writelines(self, lines):
        for line in lines:
            self.writeline(line.rstrip())

    def writeLineWithTag(self, line, tag):
        lines = self.textArea.get(1.0, "end").split("\n")
        self.writeline(line)
        self.textArea.tag_add(tag, "{}.{}".format(len(lines)-1, 0) , "{}.{}".format(len(lines), len(line)))
        
    def warn(self, text):
        self.writeLineWithTag("[WARN] " + text, "WARN_TEXT")

    def info(self, text):
        self.writeline("[INFO] " + text)

    def error(self, text):
        self.writeLineWithTag("[ERROR] " + text, "ERROR_TEXT")

    def clear(self):
        self.textArea.delete(1.0, "end")
