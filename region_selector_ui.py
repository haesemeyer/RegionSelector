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
        self.btnLoad.setGeometry(QtCore.QRect(10, 606, 101, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.ROIView = ImageView(self.centralwidget)
        self.ROIView.setGeometry(QtCore.QRect(680, 10, 411, 371))
        self.ROIView.setObjectName("ROIView")
        self.btnAddROI = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddROI.setGeometry(QtCore.QRect(314, 606, 91, 31))
        self.btnAddROI.setObjectName("btnAddROI")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 646, 121, 16))
        self.label.setObjectName("label")
        self.lblROIName = QtWidgets.QLabel(self.centralwidget)
        self.lblROIName.setGeometry(QtCore.QRect(139, 648, 91, 16))
        self.lblROIName.setObjectName("lblROIName")
        self.leNewROI = QtWidgets.QLineEdit(self.centralwidget)
        self.leNewROI.setGeometry(QtCore.QRect(320, 656, 113, 22))
        self.leNewROI.setObjectName("leNewROI")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 636, 101, 16))
        self.label_2.setObjectName("label_2")
        self.cbRegions = QtWidgets.QComboBox(self.centralwidget)
        self.cbRegions.setGeometry(QtCore.QRect(450, 653, 151, 26))
        self.cbRegions.setEditable(False)
        self.cbRegions.setObjectName("cbRegions")
        self.sldrZ = QtWidgets.QSlider(self.centralwidget)
        self.sldrZ.setGeometry(QtCore.QRect(10, 570, 611, 22))
        self.sldrZ.setOrientation(QtCore.Qt.Horizontal)
        self.sldrZ.setObjectName("sldrZ")
        self.lbl_z = QtWidgets.QLabel(self.centralwidget)
        self.lbl_z.setGeometry(QtCore.QRect(629, 575, 21, 16))
        self.lbl_z.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_z.setObjectName("lbl_z")
        self.btnDelROI = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelROI.setGeometry(QtCore.QRect(12, 660, 91, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 104, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.btnDelROI.setPalette(palette)
        self.btnDelROI.setObjectName("btnDelROI")
        self.btnCopyROI = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopyROI.setGeometry(QtCore.QRect(470, 606, 121, 31))
        self.btnCopyROI.setObjectName("btnCopyROI")
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
        self.lbl_z.setText(_translate("RegionSelector", "0"))
        self.btnDelROI.setText(_translate("RegionSelector", "Delete ROI"))
        self.btnCopyROI.setText(_translate("RegionSelector", "Copy from prev."))

from pyqtgraph import GraphicsLayoutWidget, ImageView
