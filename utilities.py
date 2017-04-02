import pyqtgraph as pg


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
# Class RegionROI
