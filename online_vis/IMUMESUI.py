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
        for item in reversed(ports_info):
            self.cbPorts.addItem(item.device)
        # Making connections
        self.connect(self.pbStart, QtCore.SIGNAL('clicked()'), self.start_recording_slot)
        self.connect(self.pbStop, QtCore.SIGNAL('clicked()'), self.stop_recording_slot)
        self.connect(self.pbSave, QtCore.SIGNAL('clicked()'), self.save_recording_slot)
        
        self.thread = MeasurementThread()
        self.thread.newData.connect(self.update_plots_slot)
        
        self.signals = []
        print('Memory pre-allocation...')
        self.signals.append(np.zeros(200*10, dtype=np.int32))
        for i in range(12):
            self.signals.append(np.zeros(200*10, dtype=np.float16))
        self.samples_measured = 0
        self.connection_speed = 115200
        self.timeout = 4

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
        self.p1.setClipToView(True)

        self.p1.getAxis('left').setPen((0,0,0))
        self.p1.getAxis('bottom').setPen((0,0,0))
        self.p1.getAxis('left').setLabel('Accelerometer +-2g', units='Volts')


        self.p2 = pg.PlotWidget()
        self.p2.setMouseEnabled(x=True, y=False)
        self.p2.showGrid(x=True, y=True)
        self.p2.setClipToView(True)

        self.p2.getAxis('left').setPen((0,0,0))
        self.p2.getAxis('bottom').setPen((0,0,0))
        self.p2.getAxis('left').setLabel('Gyroscope', units='V')

        
        self.p3 = pg.PlotWidget()
        self.p3.setMouseEnabled(x=True, y=False)
        self.p3.showGrid(x=True, y=True)
        self.p3.setClipToView(True)
        
        self.p3.getAxis('left').setPen((0,0,0))
        self.p3.getAxis('bottom').setPen((0,0,0))
        self.p3.getAxis('left').setLabel('Accelerometer +-2g', units='Volts')


        self.p4 = pg.PlotWidget()
        self.p4.setMouseEnabled(x=True, y=False)
        self.p4.showGrid(x=True, y=True)
        self.p4.setClipToView(True)

        
        self.p4.getAxis('left').setPen((0,0,0))
        self.p4.getAxis('bottom').setPen((0,0,0))
        self.p4.getAxis('left').setLabel('Gyroscope angle', units='Degrees')
        self.p4.getAxis('bottom').setLabel('Time [s]')

        # Data curves
        self.acc1x = pg.PlotCurveItem(pen="r")
        self.acc1y = pg.PlotCurveItem(pen="g")
        self.acc1z = pg.PlotCurveItem(pen="b")

        self.gyro1x = pg.PlotCurveItem(pen="r")
        self.gyro1y = pg.PlotCurveItem(pen="g")
        self.gyro1z = pg.PlotCurveItem(pen="b")

        self.acc2x = pg.PlotCurveItem(pen="r")
        self.acc2y = pg.PlotCurveItem(pen="g")
        self.acc2z = pg.PlotCurveItem(pen="b")

        self.gyro2x = pg.PlotCurveItem(pen="r")
        self.gyro2y = pg.PlotCurveItem(pen="g")
        self.gyro2z = pg.PlotCurveItem(pen="b")

        self.p1.addItem(self.acc1x)
        self.p1.addItem(self.acc1y)
        self.p1.addItem(self.acc1z)

        self.p2.addItem(self.gyro1x)
        self.p2.addItem(self.gyro1y)
        self.p2.addItem(self.gyro1z)

        self.p3.addItem(self.acc2x)
        self.p3.addItem(self.acc2y)
        self.p3.addItem(self.acc2z)

        self.p4.addItem(self.gyro2x)
        self.p4.addItem(self.gyro2y)
        self.p4.addItem(self.gyro2z)
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
        print("Recording has stopped...")
        
        self.pbStop.setEnabled(False)
        self.pbStart.setEnabled(True)
        self.pbSave.setEnabled(True)
        self.thread.stop()

        
    def start_recording_slot(self):
        if self.samples_measured > 0:
            res = QtGui.QMessageBox.warning(self, "Some unsaved data...", "There are {} samples in the buffer. Erase and start again?".format(self.samples_measured),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if res == QtGui.QMessageBox.No:
                return
            self.samples_measured = 0
        print("Recording has started...")

        self.pbStop.setEnabled(True)
        self.pbStart.setEnabled(False)
        self.pbSave.setEnabled(False)
        
        self.thread.start(self.cbPorts.currentText(), self.connection_speed, self.timeout)
        
    def save_recording_slot(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save signals', directory=".")
        if not filename:
            return
        sigs_to_save = np.zeros((self.samples_measured, len(self.signals)))
        sigs_to_save[:, 0] = (self.signals[0][:self.samples_measured]-self.signals[0][0])/1000.
        for i in range(1, 12):
            sigs_to_save[:, i] = self.signals[i+1][:self.samples_measured]

        np.savetxt(filename, sigs_to_save, fmt="%.4f")
        del sigs_to_save
        print "Data has been saved"
        
    def update_plots_slot(self, data):
        shape = self.signals[0].shape[0]
        if self.samples_measured == shape:
            print("Increasing buffers size")
            self.signals[0] = np.concatenate((self.signals[0], np.zeros(shape, dtype=np.int32)))
            for i in range(12):
                self.signals[i+1] = np.concatenate((self.signals[i+1], np.zeros(shape, dtype=np.float16)))

        self.signals[0][self.samples_measured] = data[0]
        for i in range(12):
            self.signals[i+1][self.samples_measured] = data[1][i]
        self.samples_measured += 1
        if self.samples_measured % 25 == 0:
            start = self.samples_measured-400
            if start < 0:
                start = 0
            t = (self.signals[0][start:self.samples_measured]-self.signals[0][0])/1000.
            self.acc1x.setData(t, self.signals[1][start:self.samples_measured])
            self.acc1y.setData(t, self.signals[2][start:self.samples_measured])
            self.acc1z.setData(t, self.signals[3][start:self.samples_measured])

            self.gyro1x.setData(t, self.signals[4][start:self.samples_measured])
            self.gyro1y.setData(t, self.signals[5][start:self.samples_measured])
            self.gyro1z.setData(t, self.signals[6][start:self.samples_measured])
        
            self.acc2x.setData(t, self.signals[7][start:self.samples_measured])
            self.acc2y.setData(t, self.signals[8][start:self.samples_measured])
            self.acc2z.setData(t, self.signals[9][start:self.samples_measured])

            self.gyro2x.setData(t, self.signals[10][start:self.samples_measured])
            self.gyro2y.setData(t, self.signals[11][start:self.samples_measured])
            self.gyro2z.setData(t, self.signals[12][start:self.samples_measured])
        
        
        

