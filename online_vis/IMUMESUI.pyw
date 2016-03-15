#! /usr/bin/env python2
#
import sys
from PyQt4 import QtCore, QtGui
import IMUMESUI

def main():
	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('Multi-IMU data measurement system')
	form = IMUMESUI.IMUMESUI()
	form.showMaximized()
	app.exec_()

if __name__ == "__main__":
	sys.exit(main())
