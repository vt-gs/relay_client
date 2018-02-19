#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt

from LED import *

class Relay_Table(QtGui.QTableWidget):
    def __init__(self, parent):
        super(Relay_Table, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setColumnCount(6)

        self.setHorizontalHeaderLabels(["Relay \nIDX", \
                                        "Group", \
                                        "Device", \
                                        "Current\nState", \
                                        "Indicator", \
                                        "Control"])
        self.horizontalHeader().setStyleSheet('font-size: 10pt; font-weight: bold')# font-family: Courier;')
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        #self.setStyleSheet('font-size: 8pt')#; font-family: Courier;')
        self.setStyleSheet('QTableWidget {background-color:rgb(0,0,0);\
                                          gridline-color: gray;\
                                          color:rgb(255,255,255);}')

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setDisabled(True)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

    def add_relay(self, cfg, led, cb):
        #newitem = QtGui.QTableWidgetItem(item)
        #self.setItem(m, n, newitem)
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)
        # .setItem(row, column, item)

        #idx
        idx = QtGui.QTableWidgetItem(cfg['idx'])
        idx.setFlags(idx.flags() ^ QtCore.Qt.ItemIsSelectable)
        idx.setFlags(idx.flags() ^ QtCore.Qt.ItemIsEnabled )

        self.setItem(rowPosition, 0, idx)

        #groups
        str_groups = ""
        if (type(cfg['groups']) is list):
            str_groups = ",".join(cfg['groups'])
        elif type(cfg['groups']) is unicode:
            str_groups = cfg['groups']
        groups = QtGui.QTableWidgetItem(str_groups)
        groups.setFlags(groups.flags() ^ QtCore.Qt.ItemIsSelectable)
        groups.setFlags(groups.flags() ^ QtCore.Qt.ItemIsEnabled )
        self.setItem(rowPosition, 1, groups)

        #device_lbl
        device = QtGui.QTableWidgetItem(cfg['device'])
        device.setFlags(device.flags() ^ QtCore.Qt.ItemIsSelectable)
        device.setFlags(device.flags() ^ QtCore.Qt.ItemIsEnabled )
        self.setItem(rowPosition, 2, device)

        #device_lbl
        state = QtGui.QTableWidgetItem("False")
        state.setFlags(state.flags() ^ QtCore.Qt.ItemIsSelectable)
        state.setFlags(state.flags() ^ QtCore.Qt.ItemIsEnabled )
        self.setItem(rowPosition, 3, state)

        #LED Indicator
        cell_widget = QtGui.QWidget()
        lay_out = QtGui.QHBoxLayout(cell_widget)
        lay_out.addWidget(led)
        lay_out.setAlignment(QtCore.Qt.AlignCenter)
        lay_out.setContentsMargins(0,0,0,0)
        cell_widget.setLayout(lay_out)
        #cell_widget.setFlags(cell_widget.flags() ^ QtCore.Qt.ItemIsSelectable)
        self.setCellWidget(rowPosition, 4, cell_widget)

        #CheckBox
        cell_widget = QtGui.QWidget()
        lay_out = QtGui.QHBoxLayout(cell_widget)
        lay_out.addWidget(cb)
        lay_out.setAlignment(QtCore.Qt.AlignCenter)
        lay_out.setContentsMargins(0,0,0,0)
        cell_widget.setLayout(lay_out)
        self.setCellWidget(rowPosition, 5, cell_widget)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        #self.horizontalHeader().setStretchLastSection(True)
        #self.verticalHeader().setStretchLastSection(True)
        #self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)

    def updateTable(self, current):
        current.sort(key=lambda aircraft:aircraft.range, reverse=True)
        self.setRowCount(0)
        #self.setColumnCount(0)
        for a in current:
            self.add_msg(a)
