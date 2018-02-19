#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import numpy as np
from datetime import datetime as date
import sys
from LED import *
class main_widget(QtGui.QWidget):
    def __init__(self):
        super(main_widget, self).__init__()
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()
        #self.setLayout(self.grid)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, cfg):
        #QtGui.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        #self.resize(1500, 650)
        self.setMinimumWidth(600)
        #self.setMaximumWidth(900)
        self.setMinimumHeight(300)
        #self.setMaximumHeight(700)
        self.setWindowTitle('CFT2 GS Command and Control, v1.0')
        #self.setContentsMargins(0,0,0,0)
        self.main_window = main_widget()
        self.setCentralWidget(self.main_window)

        self.cfg = cfg
        #print self.cfg

        self.resize(300, 500)
        #self.setFixedWidth(785)
        #self.setFixedHeight(275)
        #self.setMinimumWidth(275)
        self.setWindowTitle('Relay Control Client v1.0')
        self.setContentsMargins(0,0,0,0)

        self.relay_frames   = []   #list to hold spdt relay check boxes
        self.led_frames     = []
        self.relay_cb   = []   #list to hold spdt relay check boxes

        #------these might be old variables we don't need anymore--------
        self.spdt_cb        = []   #list to hold spdt relay check boxes
        self.dpdt_cb        = []   #list to hold dpdt relay check boxes
        self.spdt_a_value   = 0   #SPDT BANK A Value, 0-255
        self.spdt_b_value   = 0   #SPDT BANK B Value, 0-255
        self.dpdt_a_value   = 0   #DPDT BANK A Value, 0-255
        self.dpdt_b_value   = 0   #DPDT BANK B Value, 0-255
        self.relays_cmd     = 0   # Relay Register Value Commanded, 0-255, [SPDTA, SPDTB, DPDTA, DPDTB]
        self.relay_callback = None #Callback accessor for remote relay control
        self.set_relay_msg  = '' # '$,R,AAA,BBB,CCC,DDD'
        self.connected      = False  #Connection Status to remote relay control box
        self.adc_interval   = 1000 #ADC Auto Update Interval in milliseconds

        #----Keep these function calls----
        self.initUI()
        self.darken()
        self.setFocus()

    def initUI(self):
        self.initFrames()
        #self.initRelayFrames()
        self.initLEDs()

        self.initCheckBoxes()

        self.initNet()
        #self.initRelayCheckBoxes()

        #self.initSPDTCheckBoxes()
        #self.initDPDTCheckBoxes()
        #self.initADC()
        #self.initControls()
        #self.connectSignals()



    def initCheckBoxes(self):
        pass

    def initLEDs(self):
        hbox_led = QtGui.QHBoxLayout()
        hbox_cb = QtGui.QHBoxLayout()


        colors = ['r', 'a', 'y', 'g', 'b', 'p', 'r', 'a']
        self.test_cb = []
        self.leds = []
        for i in range(8):
            #self.relay_cb.append(Relay_QCheckBox(self, i+1, btn_name, 0, pow(2,i)))
            lbl = QtGui.QLabel("Relay "+str(i))
            lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            lbl.setFixedHeight(20)
            lbl.setStyleSheet("QLabel {  text-decoration:underline; \
                                                    font-size:14px; \
                                                    font-weight:bold; \
                                                    color:rgb(255,255,255);}")



            self.leds.append(LED(i, 60, 'g'))
            self.test_cb.append(QtGui.QCheckBox(str(i)))
            self.test_cb[i].clicked.connect(self.leds[i].set_state)

            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(self.leds[i])
            hbox_led.addLayout(vbox)
            hbox_cb.addWidget(self.test_cb[i])

        #vbox.addLayout(hbox_led)
        #vbox.addLayout(hbox_cb)

        #self.relay_fr.setLayout(hbox_led)
        self.relay_fr.setLayout(hbox_led)
        self.button_fr.setLayout(hbox_cb)


    def initFrames(self):
        self.relay_fr = QtGui.QFrame(self)
        self.relay_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.relay_fr.setFixedWidth(650)

        self.button_fr = QtGui.QFrame(self)
        self.button_fr.setFrameShape(QtGui.QFrame.StyledPanel)


        #self.button_fr.setFixedWidth(445)

        self.net_fr = QtGui.QFrame(self)
        self.net_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.net_fr.setFixedWidth(200)

        #vbox = QtGui.QVBoxLayout()
        #hbox1 = QtGui.QHBoxLayout()
        #hbox2 = QtGui.QHBoxLayout()

        #hbox2.addWidget(self.net_fr)
        #hbox2.addWidget(self.button_fr)


        #vbox.addLayout(hbox2)

        #hbox1.addLayout(vbox)
        #hbox1.addWidget(self.adc_fr)
        self.main_grid = QtGui.QGridLayout()
        self.main_grid.addWidget(self.relay_fr, 0,0,1,4)
        self.main_grid.addWidget(self.button_fr, 1,0,1,4)
        self.main_grid.addWidget(self.net_fr, 2,0,1,2)
        self.main_grid.setRowStretch(3,1)
        self.main_window.setLayout(self.main_grid)

    def initNet(self):
        lbl_width = 125

        ip_lbl = QtGui.QLabel('RMQ Broker IP:')
        ip_lbl.setFixedWidth(lbl_width)
        ip_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.ip_le = QtGui.QLineEdit()
        self.ip_le.setText("192.168.42.11")
        self.ip_le.setInputMask("000.000.000.000;")
        self.ip_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.ip_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
        self.ip_le.setMaxLength(15)

        port_lbl = QtGui.QLabel('RMQ Broker Port:')
        port_lbl.setFixedWidth(lbl_width)
        port_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.port_le = QtGui.QLineEdit()
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
        self.user_le = QtGui.QLineEdit()
        self.user_le.setText(self.cfg['broker']['user'])
        self.user_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.user_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")

        pass_lbl = QtGui.QLabel('Password:')
        pass_lbl.setFixedWidth(lbl_width)
        pass_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.pass_le = QtGui.QLineEdit()
        self.pass_le.setText(self.cfg['broker']['pass'])
        self.pass_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.pass_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")

        stat_lbl = QtGui.QLabel('Status:')
        stat_lbl.setFixedWidth(lbl_width)
        stat_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.net_stat_lbl = QtGui.QLabel('Disconnected')
        self.net_stat_lbl.setAlignment(QtCore.Qt.AlignLeft)
        self.net_stat_lbl.setFixedWidth(lbl_width)
        self.net_stat_lbl.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,0,0) ; }")

        self.connectButton = QtGui.QPushButton("Connect")

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
        grid.addWidget(self.net_stat_lbl ,4,1,1,1)
        grid.addWidget(self.connectButton,5,0,1,2)

        self.net_fr.setLayout(grid)

    def updateIPAddress(self):
        ip_addr = self.ip_le.text()
        self.service_callback.set_ip(ip_addr)

    def updatePort(self):
        port = self.port_le.text()
        self.service_callback.set_port(port)

    def initControls(self):
        self.updateButton = QtGui.QPushButton("Update")
        self.resetButton = QtGui.QPushButton("Reset")
        self.readRelayButton = QtGui.QPushButton("Read Relay")
        self.readVoltButton = QtGui.QPushButton("Read ADCs")
        self.readStatusButton = QtGui.QPushButton("Read Status")

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.readRelayButton)
        hbox1.addWidget(self.readStatusButton)
        hbox1.addWidget(self.readVoltButton)

        hbox2 = QtGui.QHBoxLayout()
        #hbox.addStretch(1)
        hbox2.addWidget(self.updateButton)
        hbox2.addWidget(self.resetButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.button_fr.setLayout(vbox)

    def set_service_callback(self, cb):
        """
        Provide the UI with access to the Service class.
        The 'Service Class' is expected to be a different thread handling network comms.
        The 'Service Class' in this case connects to the RMQ Broker.
        """
        self.service_callback = cb

    def darken(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text,QtCore.Qt.white)
        self.setPalette(palette)

    #--------OLD FUNCTIONS---------

    def connectSignals(self):
        self.resetButton.clicked.connect(self.resetButtonEvent)
        self.connectButton.clicked.connect(self.connectButtonEvent)
        #self.adc_auto_cb.stateChanged.connect(self.catchADCAutoEvent)
        self.readStatusButton.clicked.connect(self.readStatusButtonEvent)
        self.readRelayButton.clicked.connect(self.readRelayButtonEvent)
        self.readVoltButton.clicked.connect(self.readVoltButtonEvent)
        self.updateButton.clicked.connect(self.updateButtonEvent)
        #QtCore.QObject.connect(self.ADCtimer, QtCore.SIGNAL('timeout()'), self.readVoltButtonEvent)
        #QtCore.QObject.connect(self.adc_interval_le, QtCore.SIGNAL('editingFinished()'), self.updateADCInterval)
        QtCore.QObject.connect(self.ipAddrTextBox, QtCore.SIGNAL('editingFinished()'), self.updateIPAddress)
        QtCore.QObject.connect(self.portTextBox, QtCore.SIGNAL('editingFinished()'), self.updatePort)


    def updateButtonEvent(self):
        a = self.relay_callback.set_relays(self.relays_cmd)
        if (a != -1): self.updateRelayStatus(a)

    def catchCheckBoxEvent(self, relay_id, value):
        #Catches Relay_QCheckBox Event
        #print str(reltype) + str(relay_id) + " " + str(value)
        if (relay_id <= 8): self.relays_cmd += value #
        print self.relays_cmd
        #self.formatSetRelayMsg()

    def formatSetRelayMsg(self):
        self.set_relay_msg = '$,R,'
        #SPDT A
        if   (len(str(self.relays_cmd[0])) == 1): self.set_relay_msg += '00' + str(self.relays_cmd[0])
        elif (len(str(self.relays_cmd[0])) == 2): self.set_relay_msg += '0'  + str(self.relays_cmd[0])
        elif (len(str(self.relays_cmd[0])) == 3): self.set_relay_msg +=        str(self.relays_cmd[0])
        self.set_relay_msg += ','
        #SPDT B
        if   (len(str(self.relays_cmd[1])) == 1): self.set_relay_msg += '00' + str(self.relays_cmd[1])
        elif (len(str(self.relays_cmd[1])) == 2): self.set_relay_msg += '0'  + str(self.relays_cmd[1])
        elif (len(str(self.relays_cmd[1])) == 3): self.set_relay_msg +=        str(self.relays_cmd[1])
        self.set_relay_msg += ','
        #DPDT A
        if   (len(str(self.relays_cmd[2])) == 1): self.set_relay_msg += '00' + str(self.relays_cmd[2])
        elif (len(str(self.relays_cmd[2])) == 2): self.set_relay_msg += '0'  + str(self.relays_cmd[2])
        elif (len(str(self.relays_cmd[2])) == 3): self.set_relay_msg +=        str(self.relays_cmd[2])
        self.set_relay_msg += ','
        #DPDT B
        if   (len(str(self.relays_cmd[3])) == 1): self.set_relay_msg += '00' + str(self.relays_cmd[3])
        elif (len(str(self.relays_cmd[3])) == 2): self.set_relay_msg += '0'  + str(self.relays_cmd[3])
        elif (len(str(self.relays_cmd[3])) == 3): self.set_relay_msg +=        str(self.relays_cmd[3])

        print self.set_relay_msg

    def readVoltButtonEvent(self):
        a = self.relay_callback.get_adcs()
        if (a != -1): self.updateADC(a)

    def readRelayButtonEvent(self):
        a = self.relay_callback.get_relays()
        if (a != -1): self.updateRelayStatus(a)

    def readStatusButtonEvent(self):
        #print 'GUI|  Read Status Button Clicked'
        a,b = self.relay_callback.get_status()
        #print a,b
        if (a != -1): self.updateRelayStatus(a)
        if (b != -1): self.updateADC(b)
        #else:
        #    print 'GUI|  Not Connected to Relay Controller'
        #    print 'GUI|  Must Connect to Relay Controller before reading Status'

    def updateRelayStatus(self, rel):
        mask = 0b00000001
        for i in range(8):
            #SPDT A
            if ((rel[0]>>i) & mask): self.spdt_cb[i].setCheckState(QtCore.Qt.Checked)
            else: self.spdt_cb[i].setCheckState(QtCore.Qt.Unchecked)
            #SPDT B
            if ((rel[1]>>i) & mask): self.spdt_cb[i+8].setCheckState(QtCore.Qt.Checked)
            else: self.spdt_cb[i+8].setCheckState(QtCore.Qt.Unchecked)
            #DPDT A
            if ((rel[2]>>i) & mask): self.dpdt_cb[i].setCheckState(QtCore.Qt.Checked)
            else: self.dpdt_cb[i].setCheckState(QtCore.Qt.Unchecked)
            #DPDT B
            if ((rel[3]>>i) & mask): self.dpdt_cb[i+8].setCheckState(QtCore.Qt.Checked)
            else: self.dpdt_cb[i+8].setCheckState(QtCore.Qt.Unchecked)

    def updateADC(self,adcs):
        for i in range(len(adcs)):
            self.field_value[i] = str(adcs[i]) + 'V'
            self.adc_field_values_qlabels[i].setText(self.field_value[i])

    def catchADCAutoEvent(self, state):
        CheckState = (state == QtCore.Qt.Checked)
        if CheckState == True:
            self.ADCtimer.start()
            print self.getTimeStampGMT() + "GUI|  Started ADC Auto Update, Interval: " + str(self.adc_interval) + " [ms]"
        else:
            self.ADCtimer.stop()
            print self.getTimeStampGMT() + "GUI|  Stopped ADC Auto Update"

    def updateADCInterval(self):
        self.adc_interval = float(self.adc_interval_le.text()) * 1000.0
        self.ADCtimer.setInterval(self.adc_interval)
        print self.getTimeStampGMT() + "GUI|  Updated ADC Auto Interval to " + str(self.adc_interval) + " [ms]"

    def connectButtonEvent(self):
        if (not self.connected):  #Not connected, attempt to connect
            self.connected = self.relay_callback.connect()
            if (self.connected):
                self.connectButton.setText('Disconnect')
                self.net_label.setText("Connected")
                self.net_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(0,255,0) ; }")
                self.ipAddrTextBox.setStyleSheet("QLineEdit {background-color:rgb(225,225,225); color:rgb(0,0,0);}")
                self.portTextBox.setStyleSheet("QLineEdit {background-color:rgb(225,225,225); color:rgb(0,0,0);}")
                self.ipAddrTextBox.setEnabled(False)
                self.portTextBox.setEnabled(False)
        else:
            self.connected = self.relay_callback.disconnect()
            if (not self.connected):
                self.connectButton.setText('Connect')
                self.net_label.setText("Disconnected")
                self.net_label.setStyleSheet("QLabel {  font-weight:bold; color:rgb(255,0,0) ; }")
                self.ipAddrTextBox.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
                self.portTextBox.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
                self.ipAddrTextBox.setEnabled(True)
                self.portTextBox.setEnabled(True)

    def resetButtonEvent(self):
        for i in range(16):
            if self.spdt_cb[i].CheckState==True: self.spdt_cb[i].setCheckState(QtCore.Qt.Unchecked)
            if self.dpdt_cb[i].CheckState==True: self.dpdt_cb[i].setCheckState(QtCore.Qt.Unchecked)
        print self.getTimeStampGMT() + "GUI|  Cleared Relay Banks, Change Not Applied to RR Controller"

    def setCallback(self, callback):
        self.relay_callback = callback

    def initADC(self):
        field_name  = [ 'ADC1:', 'ADC2:', 'ADC3:', 'ADC4:', 'ADC5:', 'ADC6:', 'ADC7:', 'ADC8:']
        self.field_value = [ '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V' ]

        self.adc_auto_cb = QtGui.QCheckBox("Auto", self)  #Automatically update ADC voltages checkbox option
        self.adc_auto_cb.setStyleSheet("QCheckBox { font-size: 12px; \
                                                    background-color:rgb(0,0,0); \
                                                    color:rgb(255,255,255); }")

        self.adc_interval_le = QtGui.QLineEdit()
        self.adc_interval_le.setText("1")
        self.adc_validator = QtGui.QDoubleValidator()
        self.adc_interval_le.setValidator(self.adc_validator)
        self.adc_interval_le.setEchoMode(QtGui.QLineEdit.Normal)
        self.adc_interval_le.setStyleSheet("QLineEdit {background-color:rgb(255,255,255); color:rgb(0,0,0);}")
        self.adc_interval_le.setMaxLength(4)
        self.adc_interval_le.setFixedWidth(30)

        label = QtGui.QLabel('Interval[s]')
        label.setAlignment(QtCore.Qt.AlignRight)
        label.setAlignment(QtCore.Qt.AlignVCenter)
        label.setStyleSheet("QLabel { font-size: 12px; background-color: rgb(0,0,0); color:rgb(255,255,255) ; }")

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.adc_interval_le)
        hbox1.addWidget(label)

        self.adc_field_labels_qlabels = []        #List containing Static field Qlabels, do not change
        self.adc_field_values_qlabels = []       #List containing the value of the field, updated per packet

        self.ADCtimer = QtCore.QTimer(self)
        self.ADCtimer.setInterval(self.adc_interval)

        vbox = QtGui.QVBoxLayout()

        for i in range(len(field_name)):
            hbox = QtGui.QHBoxLayout()
            self.adc_field_labels_qlabels.append(QtGui.QLabel(field_name[i]))
            self.adc_field_labels_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            self.adc_field_values_qlabels.append(QtGui.QLabel(self.field_value[i]))
            self.adc_field_values_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            hbox.addWidget(self.adc_field_labels_qlabels[i])
            hbox.addWidget(self.adc_field_values_qlabels[i])
            vbox.addLayout(hbox)
        vbox.addWidget(self.adc_auto_cb)
        vbox.addLayout(hbox1)
        self.adc_fr.setLayout(vbox)



    def initControls(self):
        self.updateButton = QtGui.QPushButton("Update")
        self.resetButton = QtGui.QPushButton("Reset")
        self.readRelayButton = QtGui.QPushButton("Read Relay")
        self.readVoltButton = QtGui.QPushButton("Read ADCs")
        self.readStatusButton = QtGui.QPushButton("Read Status")

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.readRelayButton)
        hbox1.addWidget(self.readStatusButton)
        hbox1.addWidget(self.readVoltButton)

        hbox2 = QtGui.QHBoxLayout()
        #hbox.addStretch(1)
        hbox2.addWidget(self.updateButton)
        hbox2.addWidget(self.resetButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.button_fr.setLayout(vbox)



    def initDPDTCheckBoxes(self):
        hbox1 = QtGui.QHBoxLayout()
        for i in range(8):
            self.dpdt_cb.append(Relay_QCheckBox(self, i+1, 'DPDT'+str(i+1), 1, pow(2,i)))
            hbox1.addWidget(self.dpdt_cb[i])
        hbox2 = QtGui.QHBoxLayout()
        for i in range(8):
            self.dpdt_cb.append(Relay_QCheckBox(self, i+1+8, 'DPDT'+str(i+1+8), 1, pow(2,i)))
            hbox2.addWidget(self.dpdt_cb[i+8])

        #for i in range(16): print str(self.dpdt_cb[i].name)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.dpdt_fr.setLayout(vbox)

    def initFrames_old(self):
        self.spdt_fr = QtGui.QFrame(self)
        self.spdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.spdt_fr.setFixedWidth(650)

        self.dpdt_fr = QtGui.QFrame(self)
        self.dpdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.dpdt_fr.setFixedWidth(650)

        self.adc_fr = QtGui.QFrame(self)
        self.adc_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.button_fr = QtGui.QFrame(self)
        self.button_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.button_fr.setFixedWidth(445)

        self.net_fr = QtGui.QFrame(self)
        self.net_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.net_fr.setFixedWidth(200)

        vbox = QtGui.QVBoxLayout()
        hbox1 = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()

        hbox2.addWidget(self.net_fr)
        hbox2.addWidget(self.button_fr)

        vbox.addWidget(self.spdt_fr)
        vbox.addWidget(self.dpdt_fr)
        vbox.addLayout(hbox2)

        hbox1.addLayout(vbox)
        hbox1.addWidget(self.adc_fr)

        self.setLayout(hbox1)

    def initRelayFrames(self):
        hbox = QtGui.QHBoxLayout()

        for i in range(8):
            #self.relay_cb.append(Relay_QCheckBox(self, i+1, btn_name, 0, pow(2,i)))
            self.relay_frames.append(Relay_Frame_Vertical(self.cfg[i]))
            #self.relay_cb.append(QtGui.QPushButton(btn_name))
            #self.relay_cb[i].setCheckable(True)
            hbox.addWidget(self.relay_frames[i])

        self.relay_fr.setLayout(hbox)

    def initRelayCheckBoxes(self):
        hbox = QtGui.QHBoxLayout()

        for i in range(8):
            btn_name = self.cfg[i]['name']
            #self.relay_cb.append(Relay_QCheckBox(self, i+1, btn_name, 0, pow(2,i)))
            self.relay_cb.append(Relay_QPushButton(self, i, "On", pow(2,i)))
            #self.relay_cb.append(QtGui.QPushButton(btn_name))
            #self.relay_cb[i].setCheckable(True)
            hbox.addWidget(self.relay_cb[i])

    def getTimeStampGMT(self):
        return str(date.utcnow()) + " GMT | "
