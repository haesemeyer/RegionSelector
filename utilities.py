import pyqtgraph as pg

class RegionROI(pg.PolyLineROI):

    def __init__(self, positions, tag_id, region_name, **args):
        self.tag_id = tag_id
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
