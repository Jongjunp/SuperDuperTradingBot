import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from Design import MainWindow

from old_model.Agent import Agent
from old_model.Scrab import Scrab
from old_model.Environment import Env


class System:
    def __init__(self):
        # GUI Interface
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    agent = Agent()
    agent.run()

    #system = System()
    #sys.exit(system.app.exec())
