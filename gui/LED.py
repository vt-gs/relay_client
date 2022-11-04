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
        # Default to LEDs being off on startup
#        self.someFunctionCalledFromAnotherThread(self.pm_off)
        self.load_image_handler(self.pm_off)
#        self.setPixmap(self.pm_off)
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
#            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-off.png')
#            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-on.png')
            self.pm_off = os.getcwd()+'/gui/icons/led-green-off.png'
            self.pm_on = os.getcwd()+'/gui/icons/led-green-on.png'
        elif self.color == 'b':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-blue-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-blue-on.png')
        elif self.color == 'p':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-purple-off.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-purple-on.png')

    def set_state(self, state):
        self.state = state
        if state:
#            print "Setting to true"
#            self.setPixmap(self.pm_on)
#            self.showImage(self.pm_on)
            self.load_image_handler(self.pm_on)
        else:
#            print "Setting to false"
#            self.setPixmap(self.pm_off)
            self.load_image_handler(self.pm_off)

    def load_image_handler(self,filename):
        thread = LoadImageThread(file=filename)
        self.connect(thread, QtCore.SIGNAL("showImage(QString)"), self.showImage)
        thread.start()

    def showImage(self, filename):
        pixmap = QtGui.QPixmap(filename)
        self.setPixmap(pixmap)
        self.repaint()


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
#        self.setPixmap(self.pm_off)
        self.load_image_handler(self.pm_off)

    def get_pixmaps(self):
        if self.color == 'r':
            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-off-oval.png')
            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-red-on-oval.png')
        elif self.color == 'g':
#            self.pm_off = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-off-oval.png')
#            self.pm_on = QtGui.QPixmap(os.getcwd()+'/gui/icons/led-green-on-oval.png')
            self.pm_off = os.getcwd()+'/gui/icons/led-green-off-oval.png'
            self.pm_on = os.getcwd()+'/gui/icons/led-green-on-oval.png'

    def set_state(self, state):
        self.state = state
        if state:
#            self.setPixmap(self.pm_on)
            self.load_image_handler(self.pm_on)
        else:
#            self.setPixmap(self.pm_off)
            self.load_image_handler(self.pm_off)

###############################################################
# Added same as reg LED, but not sure of where 'Oval's matter #
# so it's possible this code could be cleaned up              #
###############################################################

    def load_image_handler(self,filename):
        thread = LoadImageThread(file=filename)
        self.connect(thread, QtCore.SIGNAL("showImage(QString)"), self.showImage)
        thread.start()

    def showImage(self, filename):
        pixmap = QtGui.QPixmap(filename)
        self.setPixmap(pixmap)
        self.repaint()


class LoadImageThread(QtCore.QThread):
    def __init__(self, file):
        '''
            Short lived thread that acts as if it is a QThread.  This was
            sourced from website:
            euanfreeman.co.uk/pyqt-qpixmap-and-threads/
            This allows a QThread to be generated to modify the image in
            a PyQT4 GUI and avoid an error of 'QPixmap: It is not safe to
            use pixmaps outside of the GUI thread.'
        '''
        QtCore.QThread.__init__(self)
        self.file = file

    def __del__(self):
        self.wait()

    def run(self):
        self.emit(QtCore.SIGNAL('showImage(QString)'), self.file)

