#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Date: 2022-04-09
Author: Wang Hang
Email: PKUWangHang@gmail.com
Description: Tool for time recording and other automation tasks.
Version: 1.1
'''

from datetime import datetime
from PyQt5.QtWidgets import  QComboBox,QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QSystemTrayIcon, QMenu, QAction, QCheckBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QFont, QIcon
import sys, os, time
from Util import getTasks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Tomato(QWidget):
    def __init__(self):
        super().__init__()
        self.work = 25  # 番茄钟时间25分钟
        self.second_passed = 0
        self.round = 0
        self.rest = 5  # 休息时间5分钟
        self.current_status = "Work"
        self.currentStartTime:datetime
        self.currentEndTime:datetime
        self.initUI()

    def initUI(self):
        self.setWindowTitle("番茄工作法计时器")
        self.setGeometry(0, 0, 400, 250)
        # 设置番茄图标（程序和托盘）
        self.icon = QIcon(os.path.join(BASE_DIR, 'tomato.svg'))
        self.setWindowIcon(self.icon)
        # 设置托盘功能（显示计时、还原窗体和退出程序）
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray_menu = QMenu(QApplication.desktop())
        self.restoreAction = QAction('显示', self, triggered=self.show)
        self.quitAction = QAction('退出', self, triggered=app.quit)

        self.tipAction = QAction("%s/%d > %2d:%02d" % (self.current_status, self.round + 1, self.second_passed // 60, self.second_passed % 60), self, triggered=self.show)
        self.tray_menu.addAction(self.tipAction)
        self.tray_menu.addAction(self.restoreAction)
        self.tray_menu.addAction(self.quitAction)
        self.tray.setContextMenu(self.tray_menu)
        # 设置定时器
        self.timer = QTimer()  # 初始化计时器
        self.timer.setInterval(1000)  # 每秒跳1次
        self.timer.timeout.connect(self.onTimer)  # 绑定定时触发事件

        vbox = QVBoxLayout()
        # 提示标签
        self.labelRound = QLabel(self)  # 提示标签
        self.labelRound.setText("准备开始番茄钟")
        self.labelRound.setFixedHeight(50)
        self.labelRound.setAlignment(Qt.AlignCenter)
        self.pe = QPalette()
        self.pe.setColor(QPalette.Window, Qt.darkRed)  # 蓝底白字
        self.pe.setColor(QPalette.WindowText, Qt.white)
        self.labelRound.setAutoFillBackground(True)
        self.labelRound.setPalette(self.pe)
        self.labelRound.setFont(QFont("Courier", 20, QFont.Courier))

        vbox.addWidget(self.labelRound)
        # 倒计时显示器
        self.clock = QLCDNumber(self)  # 剩余时间显示组件
        self.clock.display("%02d:%02d" % (self.second_passed, 0))
        vbox.addWidget(self.clock)

        hbox = QHBoxLayout()
        hbox2=QHBoxLayout()
        hbox3=QHBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        
        # 功能按钮
        self.startButton = QPushButton("开始")
        self.startButton.clicked.connect(self.start)
        hbox.addWidget(self.startButton)

        self.stopButton = QPushButton("停止")
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop)
        hbox.addWidget(self.stopButton)

        self.pauseButton = QPushButton("暂停")
        self.pauseButton.setEnabled(False)
        self.pauseButton.clicked.connect(self.pause)
        hbox.addWidget(self.pauseButton)
        
        # 时间调整按钮
        self.plusButton= QPushButton("+")
        self.plusButton.setEnabled(True)
        self.plusButton.clicked.connect(lambda:self.add(1))
        hbox2.addWidget(self.plusButton)

        self.pplusButton= QPushButton("++")
        self.pplusButton.setEnabled(True)
        self.pplusButton.clicked.connect(lambda:self.add(2))
        hbox2.addWidget(self.pplusButton)

        self.subButton= QPushButton("-")
        self.subButton.setEnabled(True)
        self.subButton.clicked.connect(lambda:self.add(-1))
        hbox2.addWidget(self.subButton)

        self.ssubButton= QPushButton("--")
        self.ssubButton.setEnabled(True)
        self.ssubButton.clicked.connect(lambda:self.add(-2))
        hbox2.addWidget(self.ssubButton)

        #任务选择栏
        self.taskCb = QComboBox(self)
        #添加条目
        self.taskCb.addItems(getTasks())
        hbox3.addWidget(self.taskCb)
        #模式选择
        self.modeChk = QCheckBox("正计时")
        self.modeChk.setChecked(True)
        hbox3.addWidget(self.modeChk)

        self.setLayout(vbox)
        self.tray.show()
        self.show()

    def closeEvent(self, event):
        # 禁止关闭按钮退出程序
        event.ignore()
        # 点击关闭按钮即隐藏主窗体
        self.hide()

    def onTimer(self):
        # 工作状态
        self.second_passed += 1
        self.labelRound.setPalette(self.pe)
        self.labelRound.setText("Round {0}-{1}".format(self.round + 1, self.current_status))
        self.clock.display("%02d:%02d" % (self.second_passed // 60, self.second_passed % 60))
        self.tipAction.setText("%s/%d > %2d:%02d" % (self.current_status, self.round + 1, self.second_passed // 60, self.second_passed % 60))

    def start(self):
        # 启动定时器
        self.currentStartTime=time.time()
        self.timer.start()
        # 设置功能按钮
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.plusButton.setEnabled(False)
        self.subButton.setEnabled(False)
        self.pplusButton.setEnabled(False)
        self.ssubButton.setEnabled(False)
        self.taskCb.setEnabled(False)
        
    def stop(self):
        self.round = 0
        self.second_passed = 0
        self.current_status = 'Work'
        self.clock.display("%02d:%02d" % (self.second_passed // 60, self.second_passed % 60))
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.plusButton.setEnabled(True)
        self.subButton.setEnabled(True)
        self.pplusButton.setEnabled(True)
        self.ssubButton.setEnabled(True)
        self.taskCb.setEnabled(True)
        with open(os.path.join(BASE_DIR, 'log.csv'), encoding="utf-8",mode="a") as file:
            self.currentEndTime=time.time()
            self.currentTimeSpan=self.currentEndTime-self.currentStartTime
            file.write("\n{0},{1},{2},{3}".format(self.taskCb.currentText(),self.currentStartTime.strftime('%Y/%m/%d %H:%M:%S'),self.currentEndTime.strftime('%Y/%m/%d %H:%M:%S'),self.currentTimeSpan))
        self.timer.stop()
        
    def pause(self):
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.plusButton.setEnabled(False)
        self.subButton.setEnabled(False)
        self.pplusButton.setEnabled(False)
        self.ssubButton.setEnabled(False)
        self.timer.stop()
   
    def add(self,interval):
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.pplusButton.setEnabled(True)
        self.ssubButton.setEnabled(True)
        self.work+=interval
        self.second_passed = self.work * 60
        self.clock.display("%02d:%02d" % (self.work, 0))
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tomato = Tomato()
    sys.exit(app.exec_())
