from view.main_window import MainWindow
from control.controler import Controler

if __name__ == "__main__":
    view = MainWindow()
    controler = Controler()
    view.loadControler(controler)
    controler.loadView(view)
    view.run()