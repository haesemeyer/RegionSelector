import pyqtgraph as pg

class RegionROI(pg.PolyLineROI):

    def __init__(self, positions, tag_id, region_name, **args):
        self.tag_id = tag_id
        if region_name == "":
            region_name = str(tag_id)
        self.region_name = region_name
        super().__init__(positions, closed=True, **args)

    def get_vertex_list(self):
        plist = self.getLocalHandlePositions()
        return [(p[1].x(), p[1].y()) for p in plist]
# Class RegionROI
