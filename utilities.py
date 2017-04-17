import pyqtgraph as pg
import matplotlib.path as mpath
import h5py
import numpy as np
import warnings


class RegionContainer:
    """
    Container for saving and loading RegionROI information
    """

    def __init__(self, positions, region_name: str, z_index: int):
        """
        Create a new RegionContainer
        :param positions: The polygon vertices of the ROI
        :param region_name: The name of this region
        :param z_index: The index of the z-plane that this ROI came from
        """
        self.positions = positions
        self.region_name = region_name
        self.z_index = z_index

    def point_in_region(self, point):
        """
        Tests whether a point is within the region or outside
        :param point: The test point
        :return: True if the point is within the region False if on a boundary or outside
        """
        # even when setting closed to True we still need to supply the first point twice
        poly_path = mpath.Path(self.positions + [self.positions[0]], closed=True)
        return poly_path.contains_point(point)

    @staticmethod
    def save_container_list(container_list, dfile: h5py.File):
        """
        Saves a list of RegionContainer objects to an hdf5 file
        :param container_list: The list of RegionContainer objects to save
        :param dfile: Handle of hdf5 file to which the list should be saved
        """
        key = 0
        for rc in container_list:
            while str(key) in dfile:
                key += 1
            dfile.create_group(str(key))
            dfile[str(key)].create_dataset(name="positions", data=np.vstack(rc.positions))
            dfile[str(key)].create_dataset(name="region_name", data=rc.region_name)
            dfile[str(key)].create_dataset(name="z_index", data=rc.z_index)

    @staticmethod
    def load_container_list(dfile: h5py.File):
        """
        Loads a list of RegionContainer objects from an hdf5 file
        :param dfile: Handle of hdf5 file from which list should be loaded
        :return: A list of RegionContainer objects
        """
        container_list = []
        for k in dfile.keys():
            try:
                pos = np.array(dfile[k]["positions"])
                pos = [(p[0], p[1]) for p in pos]
                rn = str(np.array(dfile[k]["region_name"]))
                zi = int(np.array(dfile[k]["z_index"]))
                rc = RegionContainer(pos, rn, zi)
                container_list.append(rc)
            except KeyError:
                warnings.warn("Found non RegionContainer object in file {0}".format(dfile.filename))
                continue
        return container_list

# Class RegionContainer


class RegionROI(pg.PolyLineROI):
    """
    Extension of pyqtgraph's PolyLineROI
    """

    def __init__(self, positions, tag_id, region_name: str, z_index: int, **args):
        """
        Create new region ROI
        :param positions: The vertex positions of the new ROI
        :param tag_id: A unique ROI id
        :param region_name: The name associated with this region
        :param z_index: The index of the z-plane that contains this ROI
        :param args: Other arguments passed to PolyLineROI
        """
        self.tag_id = tag_id
        self.z_index = z_index
        if region_name == "":
            region_name = str(tag_id)
        self.region_name = region_name
        super().__init__(positions, closed=True, **args)

    def get_vertex_list(self):
        """
        Obtain the handles/vertices of this ROI
        :return: list of (x, y) tuples with the image-vertex coordinates
        """
        plist = self.getLocalHandlePositions()
        transform = self.getGlobalTransform({'pos': pg.Point(0, 0), 'size': pg.Point(1, 1), 'angle': 0})
        assert transform.getAngle() == 0.0
        assert transform.getScale()[0] == 1
        assert transform.getScale()[1] == 1
        tx = transform.getTranslation()[0]
        ty = transform.getTranslation()[1]
        return [(p[1].x() + tx, p[1].y() + ty) for p in plist]

    def get_container(self):
        """
        Copies the non-ui related ROI information to a simple container object for saving
        :return: A RegionContainer object with all important information
        """
        return RegionContainer(self.get_vertex_list(), self.region_name, self.z_index)

    @staticmethod
    def from_container(container: RegionContainer, tag_id, **args):
        """
        Creates a new RegionROI from a container object
        :param container: The container with the ROI information
        :param tag_id: A unique ROI id
        :param args: Other arguments passed to PolyLineROI
        :return: A new RegionROI object corresponding to the container
        """
        return RegionROI(container.positions, tag_id, container.region_name, container.z_index, **args)
# Class RegionROI
