#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import os


class LED(QtGui.QLabel):
    def __init__(self, id=0, size=30, color='r'):
        super(LED, self).__init__()
        self.state = False
        self.id = id
        self.led_size = size
        self.color = color
        if color not in ['r', 'a', 'y', 'g', 'b', 'p']:
            print 'WARNING: \'{:s}\' color not valid for LED, setting to \'r\' (red)'.format(color)
            self.color = 'r'
        else:
            self.color = color

        self.get_pixmaps()
        self.initUI()

    def initUI(self):
        self.setFixedWidth(self.led_size)
        self.setFixedHeight(self.led_size)
        self.setScaledContents(True)
        self.setPixmap(self.pm_off)
        self.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

    def get_pixmaps(self):
        if self.color == 'r':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-on.png')
        elif self.color == 'a':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-amber-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-amber-on.png')
        elif self.color == 'y':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-yellow-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-yellow-on.png')
        elif self.color == 'g':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-on.png')
        elif self.color == 'b':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-blue-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-blue-on.png')
        elif self.color == 'p':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-purple-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-purple-on.png')

    def set_state(self, state):
        self.state = state
        if state:
            print "Setting to true"
            self.setPixmap(self.pm_on)
        else:
            print "Setting to false"
            self.setPixmap(self.pm_off)


class LED_Oval(QtGui.QLabel):
    def __init__(self, id=0, size=30, color='r'):
        super(LED_Oval, self).__init__()
        self.state = False
        self.id = id
        self.led_size = size
        self.color = color
        if color not in ['r','g']:
            print 'WARNING: \'{:s}\' color not valid for LED, setting to \'r\' (red)'.format(color)
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
