#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import numpy as np

import sys

class Relay_QPushButton(QtGui.QPushButton):
    def __init__(self, parent=None, relay_id = 0, name = '', value = 0):
        super(Relay_QPushButton, self).__init__()
        self.parent = parent
        self.relay_id = relay_id
        self.value = value
        self.name = ''
        if (name != ''): self.name = name
        else: self.name = str(relay_id)

        self.setText(self.name)
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {  font-size: 14px; \
                                        font-weight:bold; \
                                        background-color:rgb(100,100,100); \
                                        color:rgb(0,0,0); }")

        self.toggled.connect(self.state_change)
        #self.parent.catchCheckBoxEvent(self.reltype, self.relay_id, self.value)

    def state_change(self, state):
        if state == True:
            self.setStyleSheet("QPushButton {  font-size: 14px; \
                                        font-weight:bold; \
                                        background-color:rgb(255,0,0); \
                                        color:rgb(0,0,0); }")
        else:
            self.setStyleSheet("QPushButton {  font-size: 14px; \
                                        font-weight:bold; \
                                        background-color:rgb(100,100,100); \
                                        color:rgb(0,0,0); }")
