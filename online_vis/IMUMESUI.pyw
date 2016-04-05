#! /usr/bin/env python3
#

"""
multi_IMU software main file.

(c) Aleksei Tiulpin, 2016

Center for Machine Vision and Signal Analysis,
University of Oulu, Finland

"""

import sys
from PyQt4 import QtCore, QtGui
import IMUMESUI

def main():
	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('Multi-IMU data measurement system')
	form = IMUMESUI.IMUMESUI()
	form.showMaximized()
	app.exec()

if __name__ == "__main__":
	sys.exit(main())
