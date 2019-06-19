#! encoding=utf-8
from view.main_window import MainWindow
from control.controler import Controler
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="TCY End Manager")
    parser.add_argument('--config-file', type=str, default="config.ini", help='specify the configuration file')
    return parser.parse_args()

def readConfiguration(filename):
    context = {}
    with open(filename, "r") as fd:
        context = json.loads(fd.read())
    return context

if __name__ == "__main__":
    args = parse_args()
    config = readConfiguration(args.config_file)
    view = MainWindow(config["servers"], config["clients"])
    controler = Controler(config["servers"], config["clients"])
    view.loadControler(controler)
    controler.loadView(view)
    view.run()