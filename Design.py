from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

from reinforcement.Agent import Agent
from reinforcement.Scrab import Scrab
from reinforcement.Environment import Env
import time

form_class = uic.loadUiType("untitled.ui")[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.setupUi(self)

    def trainButtonClicked(self):
        self.trainStatus.setText("Training")
        self.log("Train Start")
        self.agent.start()

    def stopButtonClicked(self):
        self.trainStatus.setText("Stopped")
        self.log("Train Stop.")

    def log(self, text):
        now = time.localtime()
        text = "[%02d:%02d:%02d]  " % (now.tm_hour, now.tm_min, now.tm_sec) + text
        self.prompt.appendPlainText(text)
