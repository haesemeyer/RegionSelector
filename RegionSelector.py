from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget, QMainWindow
from PyQt5 import QtCore
from region_selector_ui import Ui_RegionSelector
import pyqtgraph as pg
import numpy as np
from PIL import Image
import pickle
import os

from utilities import RegionROI, RegionContainer


class RegionSelector(QMainWindow):
    """
    User interface logic to select stack regions
    """

    def __init__(self, parent=None):
        """
        Creates a new RegionSelector window
        :param parent: The window's parent
        """
        # init of ui
        QWidget.__init__(self, parent)
        self.ui = Ui_RegionSelector()
        self.ui.setupUi(self)
        # non-ui class members
        self.__current_z = 0
        self.__last_save = ""
        self.__save_current = False
        self.filename = ""
        self.currentStack = np.array([])
        self.roi_dict = {}
        self.current_z = 0
        self.current_ROI = None
        self.last_color = 0
        self.last_uid = 0
        self.last_save = ""
        self.save_current = True
        # ui stuff settings
        self.ui.lblROIName.setText("")
        # create our view-box and image view inside stackBox
        self.stack_vbox = self.ui.stackBox.addViewBox()
        self.stack_vbox.invertY(True)  # since image display inverts the Y-axis
        self.stack_vbox.setAspectLocked(True)
        self.stack_image = pg.ImageItem()
        self.stack_vbox.addItem(self.stack_image)
        # hide menu and roi button on image views
        self.ui.ROIView.ui.roiBtn.hide()
        self.ui.ROIView.ui.menuBtn.hide()
        # connect signals
        self.ui.btnLoad.clicked.connect(self.load_click)
        self.ui.btnAddROI.clicked.connect(self.addroi_click)
        self.ui.btnDelROI.clicked.connect(self.delroi_click)
        self.ui.btnCopyROI.clicked.connect(self.copy_from_above)
        self.ui.btnCopyROInext.clicked.connect(self.copy_from_below)
        self.ui.btnSave.clicked.connect(self.save_click)
        self.ui.btnSaveAs.clicked.connect(self.save_as_click)
        self.ui.btnLoadROI.clicked.connect(self.load_roi_click)
        self.ui.cbRegions.currentIndexChanged.connect(self.regionNameSelChanged)
        self.ui.sldrZ.sliderMoved.connect(self.sliderZChanged)

        # for easy testing, create and display test-image stack
        test_image = np.abs(np.random.randn(10, 100, 100, 3)*50).astype(np.uint8)
        test_image[:, 50, :, :] = 255
        test_image[:, :, 50, :] = 255
        self.currentStack = test_image
        self.reset_after_load()
        self.display_slice()

    def guess_stack_type(self):
        """
        Uses simple heuristics to determine the type (2D, 3D, grayscale, color) of the current stack
        :return: Integer identifying the stack type
        """
        if self.currentStack.size == 0 or self.currentStack.ndim < 2:
            # stack invalid
            return -1
        if self.currentStack.ndim == 2:
            # grayscale 2D image
            return 0
        if self.currentStack.ndim == 3:
            if self.currentStack.shape[2] <= 4:
                # RGB(A) 2D image (or very thin stack...)
                return 1
            else:
                # greyscale 3D stack
                return 2
        if self.currentStack.ndim == 4:
            if self.currentStack.shape[3] > 4:
                # invalid color model
                return -1
            else:
                # color 3D stack
                return 3
        # no idea
        return -1

    def reset_after_load(self):
        """
        Resets user-interface elements and internal counters after a new stack has been loaded
        """
        self.roi_dict = {}
        self.current_z = 0
        self.current_ROI = None
        self.last_color = 0
        self.last_uid = 0
        self.ui.cbRegions.clear()
        self.ui.sldrZ.setMinimum(0)
        self.ui.sldrZ.setMaximum(self.NSlices - 1)
        self.ui.sldrZ.setValue(0)
        self.last_save = ""
        self.save_current = True

    @property
    def NSlices(self):
        """
        The number of slices in the currently loaded stack 
        """
        st = self.guess_stack_type()
        if st == -1:
            return 0
        if st < 2:
            return 1
        return self.currentStack.shape[0]

    @property
    def current_z(self):
        return self.__current_z

    @current_z.setter
    def current_z(self, current_z):
        if current_z >= 0:
            self.decommission_rois()
            self.__current_z = current_z
            self.display_slice()
            # load any existing ROI's of that plane and select the first
            self.select_default_roi()
            self.ui.lbl_z.setText(str(current_z))

    @property
    def last_save(self):
        return self.__last_save

    @last_save.setter
    def last_save(self, fname):
        self.__last_save = fname
        self.ui.lblSaveName.setText(os.path.basename(fname))

    @property
    def save_current(self):
        return self.__save_current

    @save_current.setter
    def save_current(self, value):
        self.__save_current = value
        if value:
            self.ui.lblIsSaved.setText("Changes saved")
        else:
            self.ui.lblIsSaved.setText("Unsaved changes")

    def decommission_rois(self):
        """
        Removes all ROIs of the current plane from the viewbox 
        """
        if self.current_z in self.roi_dict:
            for r in self.roi_dict[self.current_z]:
                self.stack_vbox.removeItem(r)

    def display_slice(self):
        """
        Displays the current slice 
        """
        st = self.guess_stack_type()
        if st == -1:
            print("No valid stack loaded")
            return
        if st == 0 or st == 1:
            self.stack_image.setImage(self.currentStack)
        elif st == 2 or st == 3:
            if self.NSlices > self.current_z:
                self.stack_image.setImage(self.currentStack[self.current_z])
            else:
                print("Improper slice index for stack")

    def create_default_roi(self, n_vert=6):
        """
        Create a point list for the default roi when adding a new roi
        :param n_vert: The initial number of vertices in the ROI
        :return: A list of (x,y) tuples for the vertices of the roi
        """
        st = self.guess_stack_type()
        if st == -1:
            return
        if st < 2:
            width = self.currentStack.shape[0]
            height = self.currentStack.shape[1]
        else:
            width = self.currentStack.shape[1]
            height = self.currentStack.shape[2]
        center_x = width / 2
        center_y = height / 2
        radius = min([width, height]) / 10
        point_list = []
        for i in range(n_vert):
            a = 2*np.pi / n_vert * i
            x = np.cos(a)*radius + center_x
            y = np.sin(a)*radius + center_y
            point_list.append((x, y))
        return point_list

    def select_default_roi(self):
        """
        If available makes the first ROI of the current
         plane the current roi
        """
        if self.current_z in self.roi_dict:
            for i, r in enumerate(self.roi_dict[self.current_z]):
                self.stack_vbox.addItem(r)
                if i == 0:
                    self.updateRoi(r)
        else:
            self.updateRoi(None)

    def cycle_roi(self):
        """
        Cycles through the ROI list of the current z-plane selecting each ROI in turn 
        """
        if self.current_ROI is None:
            self.select_default_roi()
            return
        r_list = self.roi_dict[self.current_z]
        try:
            ix = r_list.index(self.current_ROI)
        except ValueError:
            # this means that self.current_ROI is stale. We really should never end up here
            self.select_default_roi()
            return
        # select the next ROI in this plane's list, cycling around
        self.updateRoi(r_list[(ix + 1) % len(r_list)])

    def next_roi_color(self):
        """
        Updates our ROI pen color cycle
        :return: The color of the next roi
        """
        self.last_color += 1
        self.last_color %= 9
        return self.last_color

    def next_roi_uid(self):
        """
        Updates the unique id of roi's
        :return: The uid of the next roi
        """
        self.last_uid += 1
        return self.last_uid

    def clear_all(self):
        """
        Deletes all ROIs 
        """
        # First remove ROI's in the current z-plane from view
        self.decommission_rois()
        # Re-init our dictionary
        self.roi_dict = {}
        self.current_ROI = None
        self.select_default_roi()
        self.last_uid = 0
        self.save_current = True
        self.last_save = ""

    def delete_current_roi(self):
        """
        Deletes the currently selected ROI 
        """
        if self.current_ROI is None:
            return
        if self.current_ROI.z_index != self.current_z:
            raise UserWarning("current_ROI belongs to different z-plane")
            return
        if self.current_z not in self.roi_dict:
            raise UserWarning("current_ROI was not cleared when changing planes")
            return
        # delete ROI from roi_dict, set current ROI to None and select remaining default ROI
        rlist = self.roi_dict[self.current_z]
        rlist.remove(self.current_ROI)
        self.stack_vbox.removeItem(self.current_ROI)
        self.current_ROI = None
        self.select_default_roi()
        self.save_current = False

    def add_roi(self, new_r: RegionROI):
        """
        Adds a new region in the current plane to our dictionary as well as to the display
        :param new_r: The new region to add
        """
        if self.current_z in self.roi_dict:
            self.roi_dict[self.current_z].append(new_r)
        else:
            self.roi_dict[self.current_z] = [new_r]
        # add the ROI to the display
        self.stack_vbox.addItem(new_r)
        self.updateRoi(new_r)
        new_r.sigRegionChanged.connect(self.updateRoi)
        new_r.sigClicked.connect(self.updateRoi)
        self.save_current = False

    def copy_from_zindex(self, z_index):
        """
        Copies all ROI's from the indicated z-plane to the current one
         but avoids name colisions with ROIs that already exist in the current plane
        :param z_index: The z-plane from which to copy ROI's
        """
        if z_index in self.roi_dict:
            rlist = self.roi_dict[z_index]
        else:
            return
        if self.current_z in self.roi_dict:
            names = [r.region_name for r in self.roi_dict[self.current_z]]
        else:
            names = []
        for r in rlist:
            if r.region_name in names:
                # do not copy over regions for which there is already a region with the same name
                # in the current plane
                continue
            new_r = RegionROI(r.get_vertex_list(), self.next_roi_uid(), r.region_name, self.current_z, pen=r.pen)
            self.add_roi(new_r)

    def copy_from_above(self):
        """
        Copies all ROI's from the z-plane above the current one to the current one
        """
        if self.current_z <= 0:
            return
        self.copy_from_zindex(self.current_z - 1)

    def copy_from_below(self):
        """
        Copies all ROI's from the z-plane below the current one to the current one 
        """
        if self.current_z >= self.NSlices - 1:
            return
        self.copy_from_zindex(self.current_z + 1)

    def save_rois(self, filename):
        """
        Pickle all created roi's to file
        :param filename: The name of the file
        """
        f = open(filename, 'wb')
        r_list = []
        try:
            for k in self.roi_dict:
                r_list += [r.get_container() for r in self.roi_dict[k]]
            pickle.dump(r_list, f)
            print(len(pickle.dumps(r_list)))
            self.save_current = True
        finally:
            f.close()

    def add_name_to_combo(self, name):
        """
        Adds a new name to the combo box iff that name isn't already existing
        """
        found = False
        for i in range(self.ui.cbRegions.count()):
            if self.ui.cbRegions.itemText(i) == name:
                found = True
        if not found:
            self.ui.cbRegions.addItem(name)

    # Signals #
    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        a0.accept()
        if a0.key() == QtCore.Qt.Key_Left:
            if self.current_z > 0:
                self.ui.sldrZ.setValue(self.current_z - 1)
                self.sliderZChanged(self.current_z - 1)
        elif a0.key() == QtCore.Qt.Key_Right:
            if self.current_z < self.NSlices - 1:
                self.ui.sldrZ.setValue(self.current_z + 1)
                self.sliderZChanged(self.current_z + 1)
        elif a0.key() == QtCore.Qt.Key_Up:
            if self.current_z >= 5:
                self.ui.sldrZ.setValue(self.current_z - 5)
                self.sliderZChanged(self.current_z - 5)
            else:
                self.ui.sldrZ.setValue(0)
                self.sliderZChanged(0)
        elif a0.key() == QtCore.Qt.Key_Down:
            if self.current_z < self.NSlices - 6:
                self.ui.sldrZ.setValue(self.current_z + 5)
                self.sliderZChanged(self.current_z + 5)
            else:
                self.ui.sldrZ.setValue(self.NSlices - 1)
                self.sliderZChanged(self.NSlices - 1)
        elif a0.key() == QtCore.Qt.Key_Space:
            self.cycle_roi()

    def load_click(self):
        """
        Handles event of clicking the load stack button 
        """
        diag = QFileDialog()
        fname = diag.getOpenFileName(self, "Select stack", "", "*.tif")[0]
        if fname is not None and fname != "":
            self.decommission_rois()
            self.currentStack = self.OpenStack(fname)
            self.filename = fname
            self.reset_after_load()
            self.display_slice()
        else:
            print("No file selected")

    def save_click(self):
        """
        Handles event of clicking the save roi button 
        """
        if self.last_save == "":
            self.save_as_click()
        else:
            self.save_rois(self.last_save)

    def save_as_click(self):
        """
        Handles event of clicking the save_as roi button 
        """
        diag = QFileDialog()
        fname = diag.getSaveFileName(self, "Save ROIs to file", "", "*.pickle")[0]
        if fname != "":
            self.save_rois(fname)
            self.last_save = fname

    def load_roi_click(self):
        """
        Handles event of clicking the load roi button
        """
        if not self.save_current:
            # warn user that there are unsaved changes
            dg = QMessageBox()
            dg.setText("There are unsaved changes that will be lost when loading ROIs. Continue?")
            dg.setWindowTitle("Unsaved changes")
            dg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            dg.setDefaultButton(QMessageBox.Cancel)
            dg.setIcon(QMessageBox.Warning)
            ret = dg.exec()
            if ret == QMessageBox.Cancel:
                return
        diag = QFileDialog()
        fname = diag.getOpenFileName(self, "Load ROIs from file", "", "*.pickle")[0]
        if fname == "":
            return
        f = open(fname, "rb")
        try:
            rlist = pickle.load(f)
            if type(rlist) is not list or len(rlist) == 0 or type(rlist[0]) is not RegionContainer:
                raise ValueError("Did not recognize contents of pickle file")
            # remove all current rois
            self.clear_all()
            # add the new rois
            for r in rlist:
                new_r = RegionROI.from_container(r, self.next_roi_uid(), pen=(self.next_roi_color(), 12))
                if r.z_index in self.roi_dict:
                    self.roi_dict[r.z_index].append(new_r)
                else:
                    self.roi_dict[r.z_index] = [new_r]
                # connect signals of the new roi
                new_r.sigRegionChanged.connect(self.updateRoi)
                new_r.sigClicked.connect(self.updateRoi)
                # populate our combo-box
                self.add_name_to_combo(new_r.region_name)
            self.last_save = fname
            self.display_slice()
            self.select_default_roi()
        finally:
            f.close()

    def addroi_click(self):
        """
        Handles event of clicking the add ROI button 
        """
        name = self.ui.leNewROI.text()
        new_r = RegionROI(self.create_default_roi(), self.next_roi_uid(), name, self.current_z,
                          pen=(self.next_roi_color(), 12))
        self.add_roi(new_r)
        # add the name of the created region to our list if it doesn exist yet
        self.add_name_to_combo(new_r.region_name)
        # clear the name field and combo box selection
        self.ui.leNewROI.setText("")
        self.ui.cbRegions.setCurrentIndex(-1)

    def delroi_click(self):
        """
        Handles event of clicking the delete ROI button 
        """
        self.delete_current_roi()

    def copyroi_above_click(self):
        """
        Handles event of clicking the copy ROI prev button 
        """
        self.copy_from_above()

    def copyroi_below_click(self):
        """
        Handles event of clicking the copy ROI next button 
        """
        self.copy_from_below()

    def updateRoi(self, roi: RegionROI):
        """
        Handles the event whenever an ROI is updated on-screen or programmatically
        :param roi: The roi which got updated
        """
        if roi is None:
            # clear our details image and roi indicator
            self.ui.ROIView.getImageItem().setImage(np.zeros((10,10)))
            self.ui.lblROIName.setText("")
            self.current_ROI = roi
            return
        self.current_ROI = roi
        self.ui.lblROIName.setText(roi.region_name)
        arr = roi.getArrayRegion(self.stack_image.image, img=self.stack_image)
        self.ui.ROIView.getImageItem().setImage(arr)

    def regionNameSelChanged(self, index):
        """
        Handles the event whenever a new region is selected in the combo box of previous region names
        :param index: The new index selection
        """
        if index >= 0:
            self.ui.leNewROI.setText(self.ui.cbRegions.itemText(index))

    def sliderZChanged(self, value):
        """
        Handles the event when our z-position slider was adjusted
        :param value: The new slider position
        """
        # update z-plane
        self.current_z = value

    @staticmethod
    def OpenStack(filename):
        """
        Load image stack from tiff file
        :param filename: The name of the tiff file
        :return: A (z, x, y) numpy array
        """
        im = Image.open(filename)
        # NOTE: In the follwoing im.size[1] is the height of the image (0-ymax) and im.size[0]
        # is the width (0-xmax). Increasing y are along rows, increasing x along columns
        if im.mode == 'RGB':
            stack = np.empty((im.n_frames, im.size[1], im.size[0], 3), dtype=np.uint8)
        else:
            stack = np.empty((im.n_frames, im.size[1], im.size[0]), dtype=np.uint8)
        # loop over frames and assign
        for i in range(im.n_frames):
            im.seek(i)
            stack[i, :, :] = np.array(im)
        im.close()
        return stack
#Class RegionSelector