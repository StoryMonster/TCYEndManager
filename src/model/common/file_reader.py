import os

class FileReader(object):
    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise IOError("未找到文件 " + filepath)
        self.fd = open(filepath, "r")
    
    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.fd is not None:
            self.fd.close()
            self.fd = None
    
    def read(self):
        return self.fd.read()
    
    def readlines(self):
        data = self.read()
        lines = []
        for line in data.split("\n"):
            _line = line.rstrip()
            if _line != "":
                lines.append(_line)
        return lines

    def fileno(self):
        return self.fd.fileno()
