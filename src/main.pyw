#! encoding=utf-8
from view.main_window import MainWindow
from control.controler import Controler
from model.common.file_reader import FileReader
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="TCY End Manager")
    parser.add_argument('--config-file', type=str, default="config.ini", help='specify the configuration file')
    return parser.parse_args()

def readConfiguration(filename):
    try:
        fileReader = FileReader(filename)
        context = json.loads(fileReader.read())
        return context
    except Exception as e:
        print(str(e))
        return {}

if __name__ == "__main__":
    args = parse_args()
    config = readConfiguration(args.config_file)
    if ("servers" not in config) or ("clients" not in config) or ("others" not in config):
        exit(-1)
    view = MainWindow(config["servers"], config["clients"], config["others"])
    controler = Controler(config["servers"], config["clients"], config["others"])
    view.loadControler(controler)
    controler.loadView(view)
    view.run()