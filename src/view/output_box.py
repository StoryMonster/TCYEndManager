from tkinter import Label, Scrollbar, Frame, scrolledtext, Menu
from tkinter import HORIZONTAL, VERTICAL, BOTTOM, X, RIGHT, Y, BOTH, TOP
from .menus.output_box_popup_menu import OutputBoxPopupMenu
import os

class OutputBox(Frame):
    def __init__(self, parent=None, boxName="", process_path=""):
        Frame.__init__(self, parent, bg="grey")
        self.name = boxName
        self._ui_config()
        self.textLength = 0
        self.process_path = process_path
        self.run_dir = "."
        if os.path.isfile(process_path):
            abspath = os.path.abspath(process_path)
            self.info(abspath)
            self.run_dir = os.path.dirname(abspath)

    def _ui_config(self):
        Label(self, text=self.name).pack(fill=X, expand=False)
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
        self.popupMenu.register("打开进程运行路径", self._open_process_running_dir)
        self.textArea.bind("<ButtonPress-3>", self._rightClick)

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
        if self.popupMenu is None or event.widget != self.textArea: return
        self.popupMenu.post(event.x_root, event.y_root)

    def _increseWrittenTextLength(self, length):
        self.textLength += length
        if self.textLength > 100 * 1024:
            self.clear()

    def _open_process_running_dir(self):
        os.system("explorer {}".format(self.run_dir))
