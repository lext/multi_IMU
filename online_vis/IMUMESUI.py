from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import os
import serial
from serial.tools.list_ports import comports
from MeasurementThread import MeasurementThread


pg.setConfigOption('background', 'w')
pg.setConfigOptions(antialias=True)

class IMUMESUI(QtGui.QMainWindow):

    def __init__(self):
        super(IMUMESUI, self).__init__()
        # Building GUI
        self.build_gui()
        # Initializing the list of ports
        ports_info = comports()
        for item in ports_info:
            self.cbPorts.addItem(item.device)
        # Making connections
        self.connect(self.pbStart, QtCore.SIGNAL('clicked()'), self.start_recording_slot)
        self.connect(self.pbStop, QtCore.SIGNAL('clicked()'), self.stop_recording_slot)
        self.connect(self.pbSave, QtCore.SIGNAL('clicked()'), self.save_recording_slot)
        
        self.thread = MeasurementThread()
        self.thread.newData.connect(self.update_plots_slot)
        

    def build_gui(self):
        self.setWindowTitle('Multi-IMU data measurement system')
        centralwidget = QtGui.QWidget()
        self.pbStart = QtGui.QPushButton("Start recording")
        self.pbStop = QtGui.QPushButton("Stop recording")
        self.pbSave = QtGui.QPushButton("Save results")
        
        self.pbStart.setEnabled(True)
        self.pbStop.setEnabled(False)
        self.pbSave.setEnabled(False)
        self.labPorts =  QtGui.QLabel("Ports")
        self.cbPorts = QtGui.QComboBox();
        
        # Plot widget
        self.p1 = pg.PlotWidget()
        self.p1.setMouseEnabled(x=True, y=False)
        self.p1.showGrid(x=True, y=True)
        
        self.p2 = pg.PlotWidget()
        self.p2.setMouseEnabled(x=True, y=False)
        self.p2.showGrid(x=True, y=True)

        # axes
        self.p1.getAxis('left').setPen((0,0,0))
        self.p1.getAxis('bottom').setPen((0,0,0))
        self.p1.getAxis('left').setLabel('Accelerometer +-2g', units='Volts')
        
        self.p2.getAxis('left').setPen((0,0,0))
        self.p2.getAxis('bottom').setPen((0,0,0))
        self.p2.getAxis('left').setLabel('Gyroscope', units='V')
        
        
        self.p3 = pg.PlotWidget()
        self.p3.setMouseEnabled(x=True, y=False)
        self.p3.showGrid(x=True, y=True)
        
        self.p4 = pg.PlotWidget()
        self.p4.setMouseEnabled(x=True, y=False)
        self.p4.showGrid(x=True, y=True)

        # axess
        self.p3.getAxis('left').setPen((0,0,0))
        self.p3.getAxis('bottom').setPen((0,0,0))
        self.p3.getAxis('left').setLabel('Accelerometer +-2g', units='Volts')
        
        self.p4.getAxis('left').setPen((0,0,0))
        self.p4.getAxis('bottom').setPen((0,0,0))
        self.p4.getAxis('left').setLabel('Gyroscope', units='V')
        
        self.p4.getAxis('bottom').setLabel('Time [s]')

        # Main Layout
        self.layout = QtGui.QVBoxLayout(centralwidget)
        
        # Panel with control elements
        self.l1 = QtGui.QHBoxLayout()
        self.layout.addLayout(self.l1)
        
        self.l1.addWidget(self.pbStart)
        self.l1.addWidget(self.pbStop)
        self.l1.addWidget(self.pbSave)
        self.l1.addStretch(1)
        self.l1.addWidget(self.labPorts)
        self.l1.addWidget(self.cbPorts)
        
        # Groupbox for the first IMU
        self.gbIMU1 = QtGui.QGroupBox("First IMU")
        self.layout.addWidget(self.gbIMU1)
        
        self.l2 = QtGui.QVBoxLayout()
        self.gbIMU1.setLayout(self.l2)
        
        
        self.l2.addWidget(self.p1)
        self.l2.addWidget(self.p2)
        
        # Groupbox for the second IMU
        self.gbIMU2 = QtGui.QGroupBox("Second IMU")
        self.layout.addWidget(self.gbIMU2)
        
        self.l3 = QtGui.QVBoxLayout()
        self.gbIMU2.setLayout(self.l3)
        
        self.l3.addWidget(self.p3)
        self.l3.addWidget(self.p4)



        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        # Setting central widget
        self.setCentralWidget(centralwidget)
              
    def stop_recording_slot(self):
        print "Recording has been stopped..."
        
        self.pbStop.setEnabled(False)
        self.pbStart.setEnabled(True)
        self.pbSave.setEnabled(True)

        
    def start_recording_slot(self):
        print "Recording has been started..."
        
        self.pbStop.setEnabled(True)
        self.pbStart.setEnabled(False)
        self.pbSave.setEnabled(False)
        
        self.thread.start()
        
    def save_recording_slot(self):
        print "Data have been saved..."
        
    def update_plots_slot(self, data):
        self.p1.plot(data)
        

