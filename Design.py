from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

from old_model.Agent import Agent
from old_model.Scrab import Scrab
from old_model.Environment import Env
import time

form_class = uic.loadUiType("untitled.ui")[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.agent.done_interval.connect(self.change_board)
        self.agent.episode_start.connect(self.episode_start)
        self.setupUi(self)

    # Train 버튼 눌렀을 때
    def trainButtonClicked(self):
        self.trainStatus.setText("Training")
        self.log("Train Start")
        self.agent.start()

    # 정지 버튼 눌렀을 때
    def stopButtonClicked(self):
        self.trainStatus.setText("Stopped")
        self.log("Train Stopped")

    # 프롬프트에 로그하기
    @QtCore.pyqtSlot(str)
    def log(self, text):
        now = time.localtime()
        text = "[%02d:%02d:%02d]  " % (now.tm_hour, now.tm_min, now.tm_sec) + text
        self.prompt.appendPlainText(text)

    # Environment Combo box 업데이트
    @QtCore.pyqtSlot(list)
    def change_board(self, data):
        try:
            self.balanceLabel.setText(str(data[0]))
        except Exception as e:
            self.log(e)

        return

    @QtCore.pyqtSlot(int)
    def episode_start(self, episode):
        try:
            self.episodeLabel.setText(str(episode))
        except Exception as e:
            self.log(e)

        return
