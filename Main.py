import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import qdarkstyle

from Design import MainWindow

from reinforcement.Agent import Agent
from reinforcement.Scrab import Scrab
from reinforcement.Environment import Env


class System:
    def __init__(self):
        # GUI Interface
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        self.main_window = MainWindow()
        self.main_window.show()

    # 로그 기록
    def log(self, text):
        self.main_window.log(text)
        return


if __name__ == "__main__":
    system = System()
    sys.exit(system.app.exec())
