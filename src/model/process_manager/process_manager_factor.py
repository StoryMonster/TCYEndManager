from .client_manager import ClientManager
from .server_manager import ServerManager
from .process_type import ProcessType

def create_process_manager(name="", type=ProcessType.ServerProcess, context={}, others={}, wnd=None):
    try:
        if type == ProcessType.ServerProcess: return ServerManager(name, context, others, wnd)
        elif type == ProcessType.ClientProcess: return ClientManager(name, context, others, wnd)
        else: return None
    except:
        return None
