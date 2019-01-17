#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import numpy as np
from datetime import datetime as date
import sys
from Queue import Queue
from functools import partial

from LED import *
from relay_table import *
from state_handler import *


class main_widget(QtGui.QWidget):
    def __init__(self):
        super(main_widget, self).__init__()
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()
        #self.setLayout(self.grid)

class relay_callback():
    def __init__(self, config):

        self.statehand = state_handler(config)

    def connect(self, config):
#        statehand = state_handler(config)
        print "Connecting"
        self.statehand.stateQueue.put("ACTIVE")
#        print self.state
        return True

    def disconnect(self):
        print "Disconnecting"
        self.statehand.stateQueue.put("STANDBY")
#        print self.state
        return False

    def send_msg(self, msg):
        print "Sending msg in relay_callback"
        self.statehand.msgQueue.put(msg)



class MainWindow(QtGui.QMainWindow):
    def __init__(self, cfg):
        #QtGui.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        #self.resize(1500, 650)
        self.setMinimumWidth(575)
        #self.setMaximumWidth(900)
        self.setMinimumHeight(550)
        #self.setMaximumHeight(700)
        self.setWindowTitle('Relay Control Client v1.0')
        self.setContentsMargins(0,0,0,0)
        self.main_window = main_widget()
        self.setCentralWidget(self.main_window)
        self.resize(575, 550)
        self.cfg = cfg
        self.connected = False
        self.relay_callb = relay_callback(self.cfg)

        self.led_frames     = []
        self.relay_cb       = []   #list to hold spdt relay check boxes
        self.relay_rb_on    = []
        self.relay_rb_off   = []
        self.leds           = []
        self.table_led      = []

        self.tx_reg = 0

        #----Keep these function calls----
        self.initUI()
        self.darken()
        self.setFocus()

    def initUI(self):
        self.initFrames()
        #self.initRelayFrames()
        self.initLEDs()
        self.initTXRegFrame()
        self.initRXRegFrame()
        self.initGroupFrame()
        self.initTable()
        self.initNet()
        self.initControls()
        self.connectSignals()

    def initControls(self):
        self.allOffButton = QtGui.QPushButton("All OFF")
        self.allOnButton = QtGui.QPushButton("All ON")


        self.btn_fr_grid.addWidget(self.allOffButton, 4,0,1,1)
        self.btn_fr_grid.addWidget(self.allOnButton, 4,1,1,1)
        self.btn_fr_grid.setRowStretch(4,1)

    def initGroupFrame(self):
        self.group_combo = QtGui.QComboBox(self)
        groups = []
        for rel in self.cfg['relay']['map']:
            if (type(rel['groups']) is list):
                for grp in rel['groups']:
                    if grp not in groups:
                        groups.append(grp)
            elif type(rel['groups']) is unicode:
                    if rel['groups'] not in groups:
                        groups.append(rel['groups'])

        for grp in groups:
            self.group_combo.addItem(grp)
        self.group_combo.addItem('ALL')

        self.device_combo = QtGui.QComboBox(self)
        devices = []
        for rel in self.cfg['relay']['map']:
            if rel['device'] not in devices:
                devices.append(rel['device'])

        for dev in devices:
            self.device_combo.addItem(dev)
        self.device_combo.addItem('ALL')

        self.grpEnableButton = QtGui.QPushButton("Enable")
        self.grpDisableButton = QtGui.QPushButton("Disable")

        grid = QtGui.QGridLayout()
        grid.addWidget(self.group_combo,   0, 0, 1, 1)
        grid.addWidget(self.device_combo,  0, 1, 1, 1)
        grid.addWidget(self.grpDisableButton,  1, 0, 1, 1)
        grid.addWidget(self.grpEnableButton,  1, 1, 1, 1)


        self.grpdev_fr.setLayout(grid)

    def initTable(self):
        self.relay_table=Relay_Table(self.main_window)
        self.cb_group = QtGui.QButtonGroup()
        self.cb_group.setExclusive(False)
        self.rb_group = QtGui.QButtonGroup()
        self.rb_group.setExclusive(False)
# Hardcoded place that assumes 8 channel relay
        for i in range(8):
            #cb = QtGui.QCheckBox("Relay " + str(i))
            cb = QtGui.QCheckBox("{:03d}".format(pow(2,i)))
            cb.setStyleSheet("QCheckBox {   font-size:14px; \
                                            background-color:rgb(0,0,0); \
                                            color:rgb(255,255,255) ; }")
            self.cb_group.addButton(cb, i)
            rb_on = QtGui.QRadioButton("ON")
            rb_on.setStyleSheet("QRadioButton { font-size:14px; \
                                                background-color:rgb(0,0,0); \
                                                color:rgb(255,255,255) ; }")
            rb_off = QtGui.QRadioButton("OFF")
            rb_off.setStyleSheet("QRadioButton { font-size:14px; \
                                                 background-color:rgb(0,0,0); \
                                                 color:rgb(255,255,255) ; }")
            rb_off.setChecked(True)
            self.rb_group.addButton(rb_on, i)
# Hardcoded place that assumes 8 channel relay
            self.rb_group.addButton(rb_off, i+8)

            self.relay_rb_on.append(rb_on)
            self.relay_rb_off.append(rb_off)
            self.relay_cb.append(cb)

            self.table_led.append(LED(i, 20, 'g'))
            self.relay_table.add_relay( self.cfg['relay']['map'][i], \
                                        self.table_led[i], \
                                        self.relay_cb[i], \
                                        self.relay_rb_on[i], \
                                        self.relay_rb_off[i] )

            self.relay_cb[i].clicked.connect(self.table_led[i].set_state)
# Rely on immediate write and response to update LEDs
#            self.relay_rb_on[i].clicked.connect(self.table_led[i].set_state)
#            self.relay_rb_off[i].clicked.connect(self.table_led[i].set_state)

        self.cb_group.buttonClicked.connect(self.cbClicked)
        self.rb_group.buttonClicked.connect(self.rbClicked)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.relay_table,0,0,2,2)
        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        grid.setRowStretch(0,1)
        self.table_fr.setLayout(grid)

    def cbClicked(self,id):
        id_num = self.cb_group.id(id)
        self.tx_reg = 0
        for cb in self.cb_group.buttons():
            if cb.isChecked():
                self.tx_reg += pow(2,self.cb_group.id(cb))
        #hex_str = "{:d}\n(0x{:02X})".format(self.tx_reg, self.tx_reg)
        hex_str = "0x{:02X}".format(self.tx_reg)
        self.rel_reg_lbl_tx.setText(hex_str)

    def rbClicked(self, id):
        id_num = self.rb_group.id(id)
        print id_num
        if id_num >= 8:
#            print "Off"
            id_num = id_num-8
            self.relay_rb_on[id_num].setChecked(False)
        else:
#            print "On"
            self.relay_rb_off[id_num].setChecked(False)

    def initTXRegFrame(self):
        vbox = QtGui.QVBoxLayout()

        reg_lbl_tx = QtGui.QLabel('TX Register:')
        reg_lbl_tx.setFixedHeight(20)
        reg_lbl_tx.setStyleSheet("QLabel {  font-size:14px; \
                                            font-weight:bold; \
                                            color:rgb(255,255,255) ; }")
        #text-decoration:underline; \
        #reg_lbl_tx.setFixedWidth(85)
        reg_lbl_tx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.rel_reg_lbl_tx = QtGui.QLabel('0x00')
        self.rel_reg_lbl_tx.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        #self.rel_reg_lbl_tx.setFixedWidth(100)
        self.rel_reg_lbl_tx.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,255,255) ; }")
        hbox_tx = QtGui.QHBoxLayout()
        hbox_tx.addWidget(reg_lbl_tx)
        hbox_tx.addWidget(self.rel_reg_lbl_tx)

        self.writeAllButton = QtGui.QPushButton("Write All")
        hbox_tx.addWidget(self.writeAllButton)

        self.tx_reg_fr.setLayout(hbox_tx)


    def initRXRegFrame(self):
        vbox = QtGui.QVBoxLayout()

        reg_lbl_rx = QtGui.QLabel('RX Register:')
        reg_lbl_rx.setFixedHeight(20)
        reg_lbl_rx.setStyleSheet("QLabel {  font-size:14px; \
                                            font-weight:bold; \
                                            color:rgb(255,255,255) ; }")
        #reg_lbl_rx.setFixedWidth(85)
        reg_lbl_rx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.rel_reg_lbl_rx = QtGui.QLabel('0x00')
        self.rel_reg_lbl_rx.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        #self.rel_reg_lbl_rx.setFixedWidth(100)
        self.rel_reg_lbl_rx.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,255,255) ; }")
        hbox_rx = QtGui.QHBoxLayout()
        hbox_rx.addWidget(reg_lbl_rx)
        hbox_rx.addWidget(self.rel_reg_lbl_rx)

        self.readAllButton = QtGui.QPushButton("Read All")
        hbox_rx.addWidget(self.readAllButton)

        self.rx_reg_fr.setLayout(hbox_rx)

    def initLEDs(self):
        hbox_led = QtGui.QHBoxLayout()
        hbox_cb = QtGui.QHBoxLayout()

        colors = ['r', 'a', 'y', 'g', 'b', 'p', 'r', 'a']
        for i in range(8):
            #self.relay_cb.append(Relay_QCheckBox(self, i+1, btn_name, 0, pow(2,i)))
            lbl = QtGui.QLabel("Relay "+str(i))
            lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            lbl.setFixedHeight(20)
            lbl.setStyleSheet("QLabel { text-decoration:underline; \
                                        font-size:14px; \
                                        font-weight:bold; \
                                        color:rgb(255,255,255);}")

            self.leds.append(LED(i, 50, 'g'))
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(self.leds[i])
            self.leds[i].setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            hbox_led.addLayout(vbox)
            #hbox_led.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            hbox_led.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)


        #hbox_led.addLayout(vbox_rx)
        self.led_fr.setLayout(hbox_led)

    def initFrames(self):
        self.led_fr = QtGui.QFrame(self)
        self.led_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.table_fr = QtGui.QFrame(self)
        self.table_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.button_fr = QtGui.QFrame(self)
        self.button_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.tx_reg_fr = QtGui.QFrame(self)
        self.tx_reg_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.rx_reg_fr = QtGui.QFrame(self)
        self.rx_reg_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.grpdev_fr = QtGui.QFrame(self)
        self.grpdev_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.net_fr = QtGui.QFrame(self)
        self.net_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.btn_fr_grid = QtGui.QGridLayout()
        self.btn_fr_grid.addWidget(self.tx_reg_fr, 0,0,1,2)
        self.btn_fr_grid.addWidget(self.rx_reg_fr, 1,0,1,2)
        self.btn_fr_grid.addWidget(self.grpdev_fr, 2,0,1,2)
        self.button_fr.setLayout(self.btn_fr_grid)

        self.main_grid = QtGui.QGridLayout()
        self.main_grid.addWidget(self.led_fr,   0,0,1,4)
        self.main_grid.addWidget(self.table_fr, 1,0,1,4)
        self.main_grid.addWidget(self.net_fr,   2,0,1,3)
        self.main_grid.addWidget(self.button_fr,   2,3,1,1)
        #self.main_grid.setRowStretch(1,2)
        #self.main_grid.setRowStretch(2,1)
        self.main_grid.setColumnStretch(3,1)
        self.main_window.setLayout(self.main_grid)

    def initNet(self):
        lbl_width = 125
        le_height = 22

        ip_lbl = QtGui.QLabel('RMQ Broker IP:')
        ip_lbl.setFixedWidth(lbl_width)
        ip_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        ip_lbl.setFixedHeight(le_height)
        self.ip_le = QtGui.QLineEdit()
        self.ip_le.setFixedHeight(le_height)
#        self.ip_le.setText("0.0.0.0")
        self.ip_le.setText(self.cfg['broker']['ip'])
        self.ip_le.setInputMask("000.000.000.000;")
        self.ip_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.ip_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
        self.ip_le.setMaxLength(15)

        port_lbl = QtGui.QLabel('RMQ Broker Port:')
        port_lbl.setFixedWidth(lbl_width)
        port_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        port_lbl.setFixedHeight(le_height)
        self.port_le = QtGui.QLineEdit()
        self.port_le.setFixedHeight(le_height)
        self.port_le.setText(str(self.cfg['broker']['port']))
        self.port_validator = QtGui.QIntValidator()
        self.port_validator.setRange(0,65535)
        self.port_le.setValidator(self.port_validator)
        self.port_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.port_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
        self.port_le.setMaxLength(5)
        #self.port_le.setFixedWidth(50)

        user_lbl = QtGui.QLabel('Username:')
        user_lbl.setFixedWidth(lbl_width)
        user_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        user_lbl.setFixedHeight(le_height)
        self.user_le = QtGui.QLineEdit()
        self.user_le.setFixedHeight(le_height)
        self.user_le.setText(self.cfg['broker']['user'])
        self.user_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.user_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")

        pass_lbl = QtGui.QLabel('Password:')
        pass_lbl.setFixedWidth(lbl_width)
        pass_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        pass_lbl.setFixedHeight(le_height)
        self.pass_le = QtGui.QLineEdit()
        self.pass_le.setFixedHeight(le_height)
        self.pass_le.setText(self.cfg['broker']['pass'])
        self.pass_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.pass_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")

        stat_lbl = QtGui.QLabel('Conn Status:')
        stat_lbl.setFixedWidth(lbl_width)
        stat_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        stat_lbl.setFixedHeight(le_height)
        self.net_state_label = QtGui.QLabel('Disconnected')
        self.net_state_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.net_state_label.setFixedWidth(lbl_width)
        self.net_state_label.setFixedHeight(le_height)
        self.net_state_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,0,0) ; }")

        state_lbl = QtGui.QLabel('Daemon State:')
        state_lbl.setFixedWidth(lbl_width)
        state_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        state_lbl.setFixedHeight(le_height)
        self.daemon_state_label = QtGui.QLabel('IDLE')
        self.daemon_state_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.daemon_state_label.setFixedWidth(lbl_width)
        self.daemon_state_label.setFixedHeight(le_height)
        self.daemon_state_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,0,0) ; }")

        self.connectButton = QtGui.QPushButton("Connect")
        self.startButton   = QtGui.QPushButton("Start")

        grid =  QtGui.QGridLayout()
        #                           ,r,c,r,c
        grid.addWidget(ip_lbl       ,0,0,1,1)
        grid.addWidget(self.ip_le   ,0,1,1,1)
        grid.addWidget(port_lbl     ,1,0,1,1)
        grid.addWidget(self.port_le ,1,1,1,1)
        grid.addWidget(user_lbl     ,2,0,1,1)
        grid.addWidget(self.user_le ,2,1,1,1)
        grid.addWidget(pass_lbl     ,3,0,1,1)
        grid.addWidget(self.pass_le ,3,1,1,1)
        grid.addWidget(stat_lbl     ,4,0,1,1)
        grid.addWidget(self.net_state_label ,4,1,1,1)
        grid.addWidget(state_lbl    ,5,0,1,1)
        grid.addWidget(self.daemon_state_label ,5,1,1,1)
        grid.addWidget(self.startButton,6,0,1,1)
        grid.addWidget(self.connectButton,6,1,1,1)
        grid.setSpacing(1)
        grid.setRowStretch(7,1)
        self.net_fr.setLayout(grid)

    def updateIPAddress(self):
        ip_addr = self.ip_le.text()
        self.service_callback.set_ip(ip_addr)

    def updatePort(self):
        port = self.port_le.text()
        self.service_callback.set_port(port)

    def updateLED(self,id,state):
#        print "Let's update an LED?"
#        print id
#        print state

# Moved this to main thread to keep this to update a
# single LED instead of inputting the whole state of
# LEDs/relays
#        id = int(id, 16)
#        binid = format(id, 'b').zfill(8)
#        revbinid = binid[::-1]
#        print revbinid
#        for i in range(len(revbinid)):
#            print i
#            print binid[i]
#            print revbinid[i]

        self.leds[id].set_state(state)
        self.table_led[id].set_state(state)

    def update_relay_cb(self,id,state):
        '''
        Update to checkbox (cb) in the relay
        table.
        '''
        self.relay_cb[id].setChecked(state)

    def update_relay_rb(self,id,state):
        '''
        Update to radio button (rb) in the relay
        table.
        '''
        if state is True:
            self.relay_rb_on[id].setChecked(True)
            self.relay_rb_off[id].setChecked(False)
        else:
            self.relay_rb_on[id].setChecked(False)
            self.relay_rb_off[id].setChecked(True)

    def update_RXRegFrame(self,hex_value):
#        print "updating RXRegFrame?"
        self.rel_reg_lbl_rx.setText(hex_value)

    def update_TXRegFrame(self,hex_value):
        '''
        There's a few ways the TX Register Frame is updated.
        One already covered is when the checkbox (cb) is
        clicked with cbClicked().  This is called (for now)
        from the main thread whenever a read all is
        returned from the relay_daemon.
        '''
#        print "updating TXRegFrame"
        self.rel_reg_lbl_tx.setText(hex_value)

    def set_service_callback(self, cb):
        """
        Provide the UI with access to the Service class.
        The 'Service Class' is expected to be a different thread handling network comms.
        The 'Service Class' in this case connects to the RMQ Broker.
        """
# not sure how this is supposed to work, but would be useful for buttons to send messages
# directly to service_thread rather than back up to the main_thread through the
# state_handler
        self.service_callback = cb

    def connectButtonEvent(self):
        if (not self.connected):  #Not connected, attempt to connect
#            print self.cfg
            self.connected = self.relay_callb.connect(self.cfg)
            if (self.connected):
                self.connectButton.setText('Disconnect')
                self.net_state_label.setText("Connected")
                self.net_state_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(0,255,0) ; }")
                # Gray out RMQ IP address and port text boxes and disable them
                self.ip_le.setStyleSheet("QLineEdit {background-color:rgb(225,225,225); color:rgb(0,0,0);}")
                self.port_le.setStyleSheet("QLineEdit {background-color:rgb(225,225,225); color:rgb(0,0,0);}")
                self.ip_le.setEnabled(False)
                self.port_le.setEnabled(False)
        else:
            self.connected = self.relay_callb.disconnect()
            if (not self.connected):
                self.connectButton.setText('Connect')
                self.net_state_label.setText("Disconnected")
                self.net_state_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,0,0) ; }")
                # Re-enable RMQ IP address and port text boxes
                self.ip_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
                self.port_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
                self.ip_le.setEnabled(True)
                self.port_le.setEnabled(True)

    def readAllButtonEvent(self):
#        print "Read all buttoned"
        self.relay_callb.send_msg("READ,RELAY,ALL")
#        self.service_callback.tx_q.put("READ,RELAY,ALL")
#        self.service_thread.tx_q.put("READ,RELAY,ALL")

    def writeAllButtonEvent(self):
        print "Write all buttoned"
#        hex_str = "0x{:02X}".format(self.tx_reg)
        print self.tx_reg
#        hex_val = int(str(self.tx_reg), 16)
        hex_val = "%0.2X" % self.tx_reg
        hex_val = hex_val.lower()
        print hex_val
        print type(hex_val)
        self.relay_callb.send_msg("WRITE,RELAY,"+hex_val)

    def darken(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text,QtCore.Qt.white)
        self.setPalette(palette)

    def connectSignals(self):
#####
# TO DO: Get the rest of these working or figure out which ones still matter
#####

#        self.resetButton.clicked.connect(self.resetButtonEvent)
        self.connectButton.clicked.connect(self.connectButtonEvent)
        self.readAllButton.clicked.connect(self.readAllButtonEvent)
        self.writeAllButton.clicked.connect(self.writeAllButtonEvent)
        #self.adc_auto_cb.stateChanged.connect(self.catchADCAutoEvent)
#        self.readStatusButton.clicked.connect(self.readStatusButtonEvent)
#        self.readRelayButton.clicked.connect(self.readRelayButtonEvent)
#        self.readVoltButton.clicked.connect(self.readVoltButtonEvent)
#        self.updateButton.clicked.connect(self.updateButtonEvent)
        #QtCore.QObject.connect(self.ADCtimer, QtCore.SIGNAL('timeout()'), self.readVoltButtonEvent)
        #QtCore.QObject.connect(self.adc_interval_le, QtCore.SIGNAL('editingFinished()'), self.updateADCInterval)
#        QtCore.QObject.connect(self.ip_le, QtCore.SIGNAL('editingFinished()'), self.updateIPAddress)
#        QtCore.QObject.connect(self.port_le, QtCore.SIGNAL('editingFinished()'), self.updatePort)
