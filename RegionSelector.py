from PyQt5 import QtGui
from region_selector_ui import Ui_RegionSelector
import pyqtgraph as pg
import numpy as np
from PIL import Image

from utilities import RegionROI

class RegionSelector(QtGui.QMainWindow):

    def __init__(self, parent=None):
        # non-ui class members
        self.filename = ""
        self.currentStack = np.array([])
        self.roi_dict = {}
        self.current_z = 0
        self.current_ROI = None
        self.last_color = 0
        self.last_uid = 0
        # ui stuff
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_RegionSelector()
        self.ui.setupUi(self)
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
        self.roi_dict = {}
        self.current_z = 0
        self.current_ROI = None
        self.last_color = 0
        self.last_uid = 0
        self.ui.cbRegions.clear()
        self.ui.sldrZ.setMinimum(0)
        self.ui.sldrZ.setMaximum(self.NSlices - 1)

    @property
    def NSlices(self):
        st = self.guess_stack_type()
        if st == -1:
            return 0
        if st < 2:
            return 1
        return self.currentStack.shape[0]

    def display_slice(self):
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

    def next_roi_color(self):
        self.last_color += 1
        self.last_color %= 9
        return self.last_color

    def next_roi_uid(self):
        self.last_uid += 1
        return self.last_uid

    # Signals #
    def load_click(self):
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
        name = self.ui.leNewROI.text()
        new_r = RegionROI(self.create_default_roi(), self.next_roi_uid(), name, pen=(self.next_roi_color(), 12))
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

    def updateRoi(self, roi: RegionROI):
        if roi is None:
            # clear our details image and roi indicator
            self.ui.ROIView.getImageItem().setImage(np.zeros((10,10)))
            self.ui.lblROIName.setText("")
            return
        self.current_ROI = roi
        self.ui.lblROIName.setText(roi.region_name)
        arr = roi.getArrayRegion(self.stack_image.image, img=self.stack_image)
        self.ui.ROIView.getImageItem().setImage(arr)

    def regionNameSelChanged(self, index):
        if index >= 0:
            self.ui.leNewROI.setText(self.ui.cbRegions.itemText(index))

    def sliderZChanged(self, value):
        # decommission al ROI's of the current plane
        if self.current_z in self.roi_dict:
            for r in self.roi_dict[self.current_z]:
                self.stack_vbox.removeItem(r)
        # update z-plane
        self.current_z = value
        # load any existing ROI's of that plane and select the first
        if self.current_z in self.roi_dict:
            for i, r in enumerate(self.roi_dict[self.current_z]):
                self.stack_vbox.addItem(r)
                if i == 0:
                    self.updateRoi(r)
        else:
            self.updateRoi(None)
        # display the new slice
        self.display_slice()

    @staticmethod
    def OpenStack(filename):
        """
        Load image stack from tiff-file
        """
        im = Image.open(filename)
        stack = np.empty((im.n_frames, im.size[1], im.size[0]), dtype=np.float32)
        # loop over frames and assign
        for i in range(im.n_frames):
            im.seek(i)
            stack[i, :, :] = np.array(im)
        im.close()
        return stack
#Class RegionSelector