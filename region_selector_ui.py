# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'region_selector.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegionSelector(object):
    def setupUi(self, RegionSelector):
        RegionSelector.setObjectName("RegionSelector")
        RegionSelector.resize(1286, 738)
        self.centralwidget = QtWidgets.QWidget(RegionSelector)
        self.centralwidget.setObjectName("centralwidget")
        self.stackBox = GraphicsLayoutWidget(self.centralwidget)
        self.stackBox.setGeometry(QtCore.QRect(10, 10, 641, 561))
        self.stackBox.setObjectName("stackBox")
        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(10, 610, 101, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.ROIView = ImageView(self.centralwidget)
        self.ROIView.setGeometry(QtCore.QRect(680, 10, 411, 371))
        self.ROIView.setObjectName("ROIView")
        self.btnAddROI = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddROI.setGeometry(QtCore.QRect(310, 610, 91, 32))
        self.btnAddROI.setObjectName("btnAddROI")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 660, 121, 16))
        self.label.setObjectName("label")
        self.lblROIName = QtWidgets.QLabel(self.centralwidget)
        self.lblROIName.setGeometry(QtCore.QRect(140, 660, 91, 16))
        self.lblROIName.setObjectName("lblROIName")
        self.leNewROI = QtWidgets.QLineEdit(self.centralwidget)
        self.leNewROI.setGeometry(QtCore.QRect(320, 660, 113, 22))
        self.leNewROI.setObjectName("leNewROI")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 640, 101, 16))
        self.label_2.setObjectName("label_2")
        self.cbRegions = QtWidgets.QComboBox(self.centralwidget)
        self.cbRegions.setGeometry(QtCore.QRect(440, 660, 151, 26))
        self.cbRegions.setEditable(False)
        self.cbRegions.setObjectName("cbRegions")
        self.sldrZ = QtWidgets.QSlider(self.centralwidget)
        self.sldrZ.setGeometry(QtCore.QRect(10, 570, 641, 22))
        self.sldrZ.setOrientation(QtCore.Qt.Horizontal)
        self.sldrZ.setObjectName("sldrZ")
        RegionSelector.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RegionSelector)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1286, 22))
        self.menubar.setObjectName("menubar")
        RegionSelector.setMenuBar(self.menubar)

        self.retranslateUi(RegionSelector)
        QtCore.QMetaObject.connectSlotsByName(RegionSelector)

    def retranslateUi(self, RegionSelector):
        _translate = QtCore.QCoreApplication.translate
        RegionSelector.setWindowTitle(_translate("RegionSelector", "2P Stack analyzer"))
        self.btnLoad.setText(_translate("RegionSelector", "Load Stack"))
        self.btnAddROI.setText(_translate("RegionSelector", "Add ROI"))
        self.label.setText(_translate("RegionSelector", "Current ROI name:"))
        self.lblROIName.setText(_translate("RegionSelector", "TextLabel"))
        self.label_2.setText(_translate("RegionSelector", "New ROI name:"))
        self.cbRegions.setToolTip(_translate("RegionSelector", "Region Names"))

from pyqtgraph import GraphicsLayoutWidget, ImageView
