#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import os


class LED_Oval_Red(QtGui.QLabel):
    def __init__(self, id=0, size=30, color='r'):
        super(LED_Oval_Red, self).__init__()
        self.state = False
        self.id = id
        self.led_size = size
        self.color = color
        if ((color != 'r') and (color != 'g')):
            self.color = 'r'
        else:
            self.color = color

        self.get_pixmaps()
        self.initUI()

    def initUI(self):
        led_size = 30

        self.setFixedHeight(led_size)
        self.setScaledContents(True)
        self.setPixmap(self.pm_off)

    def get_pixmaps(self):
        if self.color == 'r':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-off-oval.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-on-oval.png')
        elif self.color == 'g':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-off-oval.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-on-oval.png')

    def set_state(self, state):
        self.state = state
        if state:
            self.setPixmap(self.pm_on)
        else:
            self.setPixmap(self.pm_off)

class Single_Oval_LED_Frame(QtGui.QFrame):
    def __init__(self, id=0):
        super(Single_Oval_LED_Frame, self).__init__()
        self.state = False
        self.id = id
        self.initUI()

    def initUI(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)

        self.frame_lbl = QtGui.QLabel("Relay "+str(self.id))
        self.frame_lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.frame_lbl.setFixedHeight(20)
        self.frame_lbl.setStyleSheet("QLabel {  text-decoration:underline; \
                                                font-size:14px; \
                                                font-weight:bold; \
                                                color:rgb(255,255,255);}")

        led_size = 30

        self.red_led = QtGui.QLabel()
        #self.red_led.setFixedWidth(led_size)
        self.red_led.setFixedHeight(led_size)
        self.red_led.setScaledContents(True)
        self.red_pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-off-oval.png')
        self.red_pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-on-oval.png')
        self.red_led.setPixmap(self.red_pm_off)

        self.grid =  QtGui.QGridLayout()
        self.grid.addWidget(self.frame_lbl ,0,0,1,1)
        self.grid.addWidget(self.red_led   ,1,0,1,1)
        self.grid.setRowStretch(0,1)
        #self.grid.setColumnStretch(3,10)
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(1,1,1,1)
        self.setLayout(self.grid)

    def set_state(self, state):
        self.state = state
        if state:
            self.red_led.setPixmap(self.red_pm_on)
        else:
            self.red_led.setPixmap(self.red_pm_off)


class Dual_LED_Frame(QtGui.QFrame):
    def __init__(self, id=0):
        super(LED_Frame, self).__init__()
        self.state = False
        self.id = id
        self.initUI()

    def initUI(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)

        self.frame_lbl = QtGui.QLabel("Relay "+str(self.id))
        self.frame_lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.frame_lbl.setFixedHeight(20)
        self.frame_lbl.setStyleSheet("QLabel {  text-decoration:underline; \
                                                font-size:14px; \
                                                font-weight:bold; \
                                                color:rgb(255,255,255);}")

        led_size = 30
        self.grn_led = QtGui.QLabel()
        self.grn_led.setFixedWidth(led_size)
        self.grn_led.setFixedHeight(led_size)
        self.grn_led.setScaledContents(True)
        self.gr_pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-off.png')
        self.gr_pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-on.png')
        self.grn_led.setPixmap(self.gr_pm_off)

        self.red_led = QtGui.QLabel()
        self.red_led.setFixedWidth(led_size)
        self.red_led.setFixedHeight(led_size)
        self.red_led.setScaledContents(True)
        self.red_pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-off.png')
        self.red_pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-on.png')
        self.red_led.setPixmap(self.red_pm_on)

        self.grid =  QtGui.QGridLayout()
        self.grid.addWidget(self.frame_lbl ,0,0,2,2)
        self.grid.addWidget(self.grn_led   ,2,0,1,1)
        self.grid.addWidget(self.red_led   ,2,1,1,1)
        self.grid.setRowStretch(0,1)
        #self.grid.setColumnStretch(3,10)
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(1,1,1,1)
        self.setLayout(self.grid)

    def set_state(self, state):
        self.state = state
        if state:
            self.grn_led.setPixmap(self.gr_pm_on)
            self.red_led.setPixmap(self.red_pm_off)
        else:
            self.grn_led.setPixmap(self.gr_pm_off)
            self.red_led.setPixmap(self.red_pm_on)
