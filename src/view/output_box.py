from tkinter import Label, Scrollbar, Frame, scrolledtext, Menu
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, X, RIGHT, Y, BOTH, TOP
from .menus.output_box_popup_menu import OutputBoxPopupMenu

class OutputBox(Frame):
    def __init__(self, parent=None, boxName=""):
        Frame.__init__(self, parent, bg="grey")
        Label(self, text=boxName).pack(fill=X, expand=False)
        xScrollarBar = Scrollbar(self, orient=HORIZONTAL)
        xScrollarBar.pack(side=BOTTOM, fill=X)
        self.textArea = scrolledtext.ScrolledText(self, bd=5, wrap="none", xscrollcommand=xScrollarBar.set)
        xScrollarBar.config(command=self.textArea.xview)
        self.textArea.pack(side=TOP, expand=True, fill=BOTH)
        self.textArea.tag_configure("WARN_TEXT",background="blue", foreground="yellow")
        self.textArea.tag_configure("ERROR_TEXT", background="blue", foreground="red")
        self.textArea.tag_configure("COMMENT_TEXT", background="blue", foreground="white")
        self.popupMenu = OutputBoxPopupMenu(self.textArea)
        self.popupMenu.register("清空", self.clear)
        self.textArea.bind("<Button-3>", self._rightClick)
        self.textLength = 0

    def write(self, text):
        self.textArea.insert("end", text)
        self.textArea.see("end")
        self._increseWrittenTextLength(len(text))

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
        self.textLength = 0

    def comment(self, text):
        self.writeLineWithTag("[COMMENT] " + text, "COMMENT_TEXT")

    def _rightClick(self, event):
        self.popupMenu.show(event.x_root, event.y_root)

    def _increseWrittenTextLength(self, length):
        self.textLength += length
        if self.textLength > 10000:
            self.clear()
