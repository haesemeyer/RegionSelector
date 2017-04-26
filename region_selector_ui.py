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
        RegionSelector.resize(1105, 707)
        self.centralwidget = QtWidgets.QWidget(RegionSelector)
        self.centralwidget.setObjectName("centralwidget")
        self.stackBox = GraphicsLayoutWidget(self.centralwidget)
        self.stackBox.setGeometry(QtCore.QRect(10, 10, 641, 561))
        self.stackBox.setObjectName("stackBox")
        self.ROIView = ImageView(self.centralwidget)
        self.ROIView.setGeometry(QtCore.QRect(770, 10, 300, 300))
        self.ROIView.setObjectName("ROIView")
        self.sldrZ = QtWidgets.QSlider(self.centralwidget)
        self.sldrZ.setGeometry(QtCore.QRect(10, 570, 611, 22))
        self.sldrZ.setOrientation(QtCore.Qt.Horizontal)
        self.sldrZ.setObjectName("sldrZ")
        self.lbl_z = QtWidgets.QLabel(self.centralwidget)
        self.lbl_z.setGeometry(QtCore.QRect(629, 575, 21, 16))
        self.lbl_z.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_z.setObjectName("lbl_z")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(660, 313, 436, 206))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.lblSaveName = QtWidgets.QLabel(self.groupBox)
        self.lblSaveName.setGeometry(QtCore.QRect(8, 183, 304, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.lblSaveName.setFont(font)
        self.lblSaveName.setObjectName("lblSaveName")
        self.lblIsSaved = QtWidgets.QLabel(self.groupBox)
        self.lblIsSaved.setGeometry(QtCore.QRect(320, 180, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.lblIsSaved.setFont(font)
        self.lblIsSaved.setObjectName("lblIsSaved")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(5, 24, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lblROIName = QtWidgets.QLabel(self.groupBox)
        self.lblROIName.setGeometry(QtCore.QRect(140, 25, 288, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblROIName.setFont(font)
        self.lblROIName.setObjectName("lblROIName")
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(6, 170, 423, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.btnDelROI = QtWidgets.QPushButton(self.groupBox)
        self.btnDelROI.setGeometry(QtCore.QRect(6, 143, 91, 31))
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
        self.leNewROI = QtWidgets.QLineEdit(self.groupBox)
        self.leNewROI.setGeometry(QtCore.QRect(150, 51, 113, 22))
        self.leNewROI.setObjectName("leNewROI")
        self.cbRegions = QtWidgets.QComboBox(self.groupBox)
        self.cbRegions.setGeometry(QtCore.QRect(280, 48, 151, 26))
        self.cbRegions.setEditable(False)
        self.cbRegions.setObjectName("cbRegions")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(7, 55, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setGeometry(QtCore.QRect(5, 40, 423, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btnAddROI = QtWidgets.QPushButton(self.groupBox)
        self.btnAddROI.setGeometry(QtCore.QRect(5, 77, 91, 31))
        self.btnAddROI.setObjectName("btnAddROI")
        self.btnCopyROI = QtWidgets.QPushButton(self.groupBox)
        self.btnCopyROI.setGeometry(QtCore.QRect(6, 107, 125, 31))
        self.btnCopyROI.setObjectName("btnCopyROI")
        self.btnCopyROInext = QtWidgets.QPushButton(self.groupBox)
        self.btnCopyROInext.setGeometry(QtCore.QRect(140, 108, 121, 31))
        self.btnCopyROInext.setObjectName("btnCopyROInext")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(200, 600, 402, 80))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 383, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 384, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 60, 384, 16))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 640, 73, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.dialMax = QtWidgets.QSlider(self.centralwidget)
        self.dialMax.setGeometry(QtCore.QRect(30, 660, 124, 20))
        self.dialMax.setMinimum(1)
        self.dialMax.setMaximum(255)
        self.dialMax.setProperty("value", 255)
        self.dialMax.setOrientation(QtCore.Qt.Horizontal)
        self.dialMax.setObjectName("dialMax")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 590, 68, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.dialMin = QtWidgets.QSlider(self.centralwidget)
        self.dialMin.setGeometry(QtCore.QRect(29, 605, 122, 20))
        self.dialMin.setMaximum(255)
        self.dialMin.setOrientation(QtCore.Qt.Horizontal)
        self.dialMin.setObjectName("dialMin")
        self.stackBox.raise_()
        self.ROIView.raise_()
        self.sldrZ.raise_()
        self.lbl_z.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.label_7.raise_()
        self.dialMax.raise_()
        self.label_6.raise_()
        self.dialMin.raise_()
        self.label_3.raise_()
        RegionSelector.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RegionSelector)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1105, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        RegionSelector.setMenuBar(self.menubar)
        self.actionOpen_Stack = QtWidgets.QAction(RegionSelector)
        self.actionOpen_Stack.setObjectName("actionOpen_Stack")
        self.actionLoad_regions = QtWidgets.QAction(RegionSelector)
        self.actionLoad_regions.setObjectName("actionLoad_regions")
        self.actionSave_regions = QtWidgets.QAction(RegionSelector)
        self.actionSave_regions.setObjectName("actionSave_regions")
        self.actionSave_regions_as = QtWidgets.QAction(RegionSelector)
        self.actionSave_regions_as.setObjectName("actionSave_regions_as")
        self.menu_File.addAction(self.actionOpen_Stack)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionLoad_regions)
        self.menu_File.addAction(self.actionSave_regions)
        self.menu_File.addAction(self.actionSave_regions_as)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(RegionSelector)
        QtCore.QMetaObject.connectSlotsByName(RegionSelector)

    def retranslateUi(self, RegionSelector):
        _translate = QtCore.QCoreApplication.translate
        RegionSelector.setWindowTitle(_translate("RegionSelector", "Brain Segmenter"))
        self.lbl_z.setText(_translate("RegionSelector", "0"))
        self.groupBox.setTitle(_translate("RegionSelector", "Region commands"))
        self.lblSaveName.setText(_translate("RegionSelector", "TextLabel"))
        self.lblIsSaved.setText(_translate("RegionSelector", "Changes saved"))
        self.label.setText(_translate("RegionSelector", "Current ROI name:"))
        self.lblROIName.setText(_translate("RegionSelector", "TextLabel"))
        self.btnDelROI.setText(_translate("RegionSelector", "Delete ROI"))
        self.cbRegions.setToolTip(_translate("RegionSelector", "Region Names"))
        self.label_2.setText(_translate("RegionSelector", "New ROI name:"))
        self.btnAddROI.setText(_translate("RegionSelector", "Add ROI"))
        self.btnCopyROI.setText(_translate("RegionSelector", "Copy from prev."))
        self.btnCopyROInext.setText(_translate("RegionSelector", "Copy from next"))
        self.groupBox_2.setTitle(_translate("RegionSelector", "Navigation"))
        self.label_3.setText(_translate("RegionSelector", "Arrow left/right: Previous/Next slice  "))
        self.label_4.setText(_translate("RegionSelector", "Arrow up/down: Go back/Advance 5 slices  "))
        self.label_5.setText(_translate("RegionSelector", "Space bar: Cycle regions in current slice  "))
        self.label_7.setText(_translate("RegionSelector", "Maximum"))
        self.label_6.setText(_translate("RegionSelector", "Minimum"))
        self.menu_File.setTitle(_translate("RegionSelector", "&File"))
        self.actionOpen_Stack.setText(_translate("RegionSelector", "Open Stack"))
        self.actionLoad_regions.setText(_translate("RegionSelector", "Load regions..."))
        self.actionSave_regions.setText(_translate("RegionSelector", "Save regions"))
        self.actionSave_regions_as.setText(_translate("RegionSelector", "Save regions as..."))

from pyqtgraph import GraphicsLayoutWidget, ImageView
