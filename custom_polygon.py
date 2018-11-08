# custom_polygon.py
import numpy as np

from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path

def poly2mask(x,y,polypath,invert=True):
    ''' maskgrid = poly2mask(lat,lon,poly,invert=False)
    
    Return a mask for values within the given polygon
    USAGE: 
    '''
    ln,lt = np.meshgrid(x,y)
    lls = ln.shape
    xypts = np.hstack((ln.ravel()[:,np.newaxis], lt.ravel()[:,np.newaxis]))
    #tes = np.reshape(xypts[:,0],lls)
    truelist=polypath.contains_points(xypts)
    mask=np.asarray(truelist,dtype=np.bool8)
    maskgrid = np.reshape(mask, lls)
    if invert:
        maskgrid = ~maskgrid
    return maskgrid

class SelectFromArray(object):
    """Select indices from a matplotlib collection using `PolygonSelector`.

    Selected indices are saved in the `ind` attribute. This tool fades out the
    points that are not part of the selection (i.e., reduces their alpha
    values). If your collection has alpha < 1, this tool will permanently
    alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, x, y, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.x, self.y = x, y
        self.xys = np.vstack((x,y))
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object

        self.poly = PolygonSelector(ax, self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.poly_mask = poly2mask(self.x,self.y,path)
        self.canvas.draw_idle()

    def disconnect(self):
        self.poly.disconnect_events()
        self.canvas.draw_idle()