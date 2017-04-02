from PyQt5 import QtGui
from region_selector_ui import Ui_RegionSelector
import pyqtgraph as pg
import numpy as np
from PIL import Image

from utilities import RegionROI


class RegionSelector(QtGui.QMainWindow):
    """
    User interface logic to select stack regions
    """

    def __init__(self, parent=None):
        """
        Creates a new RegionSelector window
        :param parent: The window's parent
        """
        # init of ui
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_RegionSelector()
        self.ui.setupUi(self)
        # non-ui class members
        self.__current_z = 0
        self.filename = ""
        self.currentStack = np.array([])
        self.roi_dict = {}
        self.current_z = 0
        self.current_ROI = None
        self.last_color = 0
        self.last_uid = 0
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
            self.__current_z = current_z
            self.ui.lbl_z.setText(str(current_z))

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


    # Signals #
    def load_click(self):
        """
        Handles event of clicking the load stack button 
        """
        diag = QtGui.QFileDialog()
        fname = diag.getOpenFileName(self, "Select stack", "E:/Dropbox/2P_Data", "*.tif")[0]
        if fname is not None and fname != "":
            assert isinstance(fname, str)
            self.currentStack = self.OpenStack(fname)
            self.filename = fname
            self.reset_after_load()
            self.display_slice()
        else:
            print("No file selected")

    def addroi_click(self):
        """
        Handles event of clicking the add ROI button 
        """
        name = self.ui.leNewROI.text()
        new_r = RegionROI(self.create_default_roi(), self.next_roi_uid(), name, self.current_z,
                          pen=(self.next_roi_color(), 12))
        if self.current_z in self.roi_dict:
            self.roi_dict[self.current_z].append(new_r)
        else:
            self.roi_dict[self.current_z] = [new_r]
        # add the name of the created region to our list if it doesn exist yet
        found = False
        for i in range(self.ui.cbRegions.count()):
            if self.ui.cbRegions.itemText(i) == new_r.region_name:
                found = True
        if not found:
            self.ui.cbRegions.addItem(new_r.region_name)
        # add the ROI to the display
        self.stack_vbox.addItem(new_r)
        self.updateRoi(new_r)
        new_r.sigRegionChanged.connect(self.updateRoi)
        # clear the name field and combo box selection
        self.ui.leNewROI.setText("")
        self.ui.cbRegions.setCurrentIndex(-1)

    def delroi_click(self):
        """
        Handles event of clicking the delete ROI button 
        """
        self.delete_current_roi()

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
        # decommission all ROI's of the current plane
        if self.current_z in self.roi_dict:
            for r in self.roi_dict[self.current_z]:
                self.stack_vbox.removeItem(r)
        # update z-plane
        self.current_z = value
        # load any existing ROI's of that plane and select the first
        self.select_default_roi()
        # display the new slice
        self.display_slice()

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