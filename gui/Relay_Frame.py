#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt

class Relay_Frame(QtGui.QFrame):
    def __init__(self, cfg):
        super(Relay_Frame, self).__init__()
        #self.parent = parent
        self.rel_idx = cfg['idx']
        #self.value = value
        self.name = cfg['name']
        self.device = cfg['device']
        self.groups = cfg['groups']


        self.state = False

        self.initUI()

    def initUI(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.initWidgets()

    def initWidgets(self):
        #btn_hbox = QtGui.QHBoxLayout()
        self.on_btn = QtGui.QPushButton("ON")
        self.on_btn.setCheckable(True)
        self.on_btn.setFixedWidth(50)
        self.on_btn.setStyleSheet("QPushButton {font-size: 14px; \
                                                font-weight:bold; \
                                                background-color:rgb(0,255,0); \
                                                color:rgb(0,0,0);} ")

        self.off_btn = QtGui.QPushButton("OFF")
        self.off_btn.setCheckable(True)
        self.off_btn.setChecked(True)
        self.off_btn.setEnabled(False)
        self.off_btn.setFixedWidth(50)
        self.off_btn.setStyleSheet("QPushButton {font-size: 14px; \
                                                font-weight:bold; \
                                                background-color:rgb(255,0,0); \
                                                color:rgb(0,0,0);} ")

        self.on_btn.clicked.connect(self.onButtonClicked)
        self.off_btn.clicked.connect(self.offButtonClicked)

        self.idx_lbl = QtGui.QLabel(self.rel_idx)
        self.idx_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.idx_lbl.setStyleSheet("QLabel {font-size:18px; color:rgb(255,255,255);}")

        self.name_lbl = QtGui.QLabel(self.name)
        self.name_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.name_lbl.setStyleSheet("QLabel {font-size:18px; color:rgb(255,255,255);}")

        self.device_lbl = QtGui.QLabel(self.device)
        self.device_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.device_lbl.setStyleSheet("QLabel {font-size:18px; color:rgb(255,255,255);}")

        str_groups = ""
        if (type(self.groups) is list):
            str_groups = ",".join(self.groups)
        elif type(self.groups) is unicode:
            str_groups = self.groups
        self.groups_lbl = QtGui.QLabel(str_groups)
        self.groups_lbl.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groups_lbl.setStyleSheet("QLabel {font-size:18px; color:rgb(255,255,255);}")

        self.grid =  QtGui.QGridLayout()
        self.grid.addWidget(self.name_lbl   ,0,0,1,1)
        self.grid.addWidget(self.groups_lbl   ,0,1,1,1)
        self.grid.addWidget(self.on_btn     ,0,2,1,1)
        self.grid.addWidget(self.off_btn    ,0,3,1,1)
        #self.grid.setColumnStretch(1,1)
        #self.grid.setColumnStretch(0,10)
        #self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        #btn_hbox.addWidget(self.on_btn)
        #btn_hbox.addWidget(self.off_btn)
        #btn_hbox.setContentsMargins(0, 0, 0, 0)
        #self.setLayout(btn_hbox)

    def onButtonClicked(self):
        self.buttonClicked(True)

    def offButtonClicked(self):
        self.buttonClicked(False)

    def buttonClicked(self, btn_id):
        if btn_id: #ON
            #print "on btn clicked"
            self.on_btn.setEnabled(False)
            self.off_btn.setEnabled(True)
            self.off_btn.setChecked(False)
            self.state = True
        else:#OFF
            #print "off btn clicked"
            self.on_btn.setEnabled(True)
            self.off_btn.setEnabled(False)
            self.on_btn.setChecked(False)
            self.state = False

        print self.name, self.state
