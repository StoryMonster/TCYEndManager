#! encoding=utf-8
from view.main_window import MainWindow
from control.controler import Controler
from model.common.file_reader import FileReader
import argparse
import os
import xml.etree.ElementTree as ET

class ConfigFileParser(object):
    def __init__(self, filename):
        self.root = ET.parse(filename).getroot()

    def _parse_server_related_configuration(self, servers, others):
        servers_node = self.root.find("servers")
        assert(servers_node is not None)
        instances = servers_node.find("instances")
        assert(instances is not None)
        for server in instances:
            servers[server.tag] = server.attrib
        compiler = servers_node.find("compiler")
        if compiler is not None:
            others[compiler.tag] = compiler.attrib
        quick_launch_servers = servers_node.find("quick_launch_servers")
        if quick_launch_servers is not None:
            others[quick_launch_servers.tag] = quick_launch_servers.attrib

    def _parse_client_related_configuration(self, clients, others):
        clients_node = self.root.find("clients")
        assert(clients_node)
        simulator = clients_node.find("simulator")
        assert(simulator is not None)
        others[simulator.tag] = simulator.attrib
        instances = clients_node.find("instances")
        assert(instances is not None)
        for client in instances:
            clients[client.tag] = client.attrib

    def parse(self):
        try:
            config = {"servers":{}, "clients":{}, "others":{}}
            self._parse_server_related_configuration(config["servers"], config["others"])
            self._parse_client_related_configuration(config["clients"], config["others"])
            return config
        except Exception as e:
            print(str(e))
            raise Exception("Parse config file fail")

def parse_args():
    parser = argparse.ArgumentParser(description="TCY End Manager")
    parser.add_argument('--config-file', type=str, default="config.xml", help='specify the configuration file')
    parser.add_argument('--log-dir', type=str, default=".", help='specify the log directory')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    assert(os.path.isdir(args.log_dir))
    config = ConfigFileParser(args.config_file).parse()
    config["others"]["logdir"] = os.path.abspath(args.log_dir)
    view = MainWindow(config["servers"], config["clients"], config["others"])
    controler = Controler(config["servers"], config["clients"], config["others"])
    view.loadControler(controler)
    controler.loadView(view)
    view.run()