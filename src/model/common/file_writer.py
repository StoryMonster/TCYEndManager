import os

class FileWriter(object):
    def __init__(self, filepath):
        self.fd = open(filepath, "w")
        self.filepath = filepath
    
    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.fd is not None:
            self.fd.close()
            self.fd = None
    
    def write(self, content):
        self.fd.write(content)

    def fileno(self):
        return self.fd.fileno()
