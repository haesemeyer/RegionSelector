from PyQt5 import QtGui
import pyqtgraph as pg
import sys

from RegionSelector import RegionSelector



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RegionSelector()
    myapp.show()
    sys.exit(app.exec_())