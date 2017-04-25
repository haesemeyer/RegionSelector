# RegionSelector
Program for selecting brain regions in stacks and saving their descriptors to file written in python using qt5.

The program allows loading 8-bit grayscale and RGB(A) stacks (currently only tiff-stacks are supported). Regions can be named and selected
in indivdual slices of the stack. To aid in segmenting, regions can be copied between consecutive slices.

## Region files
All segmentations can be saved from the user interface to hdf5 files. Saving/loading of regions outside of the RegionSelector program is
easily done using the `RegionContainer` class in *utilities.py*. Otherwise information can be loaded by parsing the file structure listed
below.

### HDF5 File structure
Keys are listed in italics, groups in bold.
- RootNode
  - **1**
    - *positions* 2D `numpy.ndarray` of vertex coordinates for region 1
    - *region_name* `str` with the name given to the region
    - *z_index* `int` with the z plane index of the region in the stack
  - **2**
    - *positions*
    - ...

## Installation
No installation except for python and dependencies is required (easiest is to install a scientific python distribution such as Anaconda).
Simply copy all repository files into one folder and then run

`python start_regionSelector.py`

from the command line.

## Dependencies
Python 3.x

Numpy

Scipy

Pillow

Qt5

PyQt5

Pyqtgraph

Tested on Windows and OsX with python 3.5 and 3.6
