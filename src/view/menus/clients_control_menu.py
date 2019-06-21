from tkinter import Menu, BooleanVar


class ClientsControlMenu(Menu):
    def __init__(self, parent=None, clients={}):
        Menu.__init__(self, parent, tearoff=0, bd=5)
        self.clients = clients
        self.clients_status = {}
        for clientName in self.clients:
            self._addItem(clientName)
    
    def loadCallback(self, callback):
        self.callback = callback

    def _addItem(self, clientName):
        self.clients_status[clientName] = BooleanVar()
        self.clients_status[clientName].set(False)
        self.add_checkbutton(label=f"运行{clientName}", onvalue=True, offvalue=False, variable=self.clients_status[clientName], command=lambda : self._onClickClient(clientName))

    def _onClickClient(self, clientName):
        if self.callback is None: return
        self.callback(clientName, self.clients_status[clientName].get())

    def resetStatus(self):
        for name in self.clients_status:
            self.clients_status[name].set(False)
