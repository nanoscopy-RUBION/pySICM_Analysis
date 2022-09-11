
import matplotlib
from PyQt6.QtCore import QPoint

DEFAULT_COLOR_MAP = matplotlib.cm.YlGnBu_r


class View:
    """
    This class no longer contains data. It will only handle representation of data in figures.
    """

    def __init__(self):

        self.axes_shown = True
        self.show_as_px = True
        self.color_bar_shown = True
        self.aspect_ratio = (4, 4, 3)  # Default value by matplotlib
        self.color_map = DEFAULT_COLOR_MAP
        self.rois = (QPoint(), QPoint())
        self.azim: float = -60.0
        self.elev: float = 30.0

    def get_xlim(self):
        return self.xlims

    def get_ylim(self):
        return self.ylims

    def toggle_axes(self):
        """
        Changes the state of axis visibility.
        """
        self.axes_shown = not self.axes_shown

    def toggle_color_bar(self):
        """
        Switches the color bar on or off.
        """
        self.color_bar_shown = not self.color_bar_shown

    def show_axes(self):
        return self.axes_shown

    def show_color_bar(self):
        return self.color_bar_shown

    def set_xlims(self, lims):
        """
        Sets x-axis limits for the visual display of the data. This does not crop the data and the rest can still be
        viewed by panning. Will check to ensure the values are floats but does not check that the lower bound is first.

        :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
        :returns: 1 upon successful setting and 0 upon failure
        """
        if len(lims) == 2:
            if (isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.xlims = lims
                return 1
            else:
                # print("Please choose numbers for both") #Check input elsewhere?
                return 0

    def set_ylims(self, lims):
        """
        Set Y-limits for the visual display of the data. This does not crop the data and the rest can still be viewed by panning.
        Will check to ensure the values are floats but does not check that the lower bound is first.

        :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
        :returns: this is a description of what is returned
        """
        if len(lims) == 2:
            if (isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.ylims = lims
                return 1
            else:
                print("Please choose numbers for both")  # Check input elsewhere?
                return 0

    def restore(self):
        """
        Resets all viewing options (graph limits, whether axises are shown, aspect ratio, etc) to their default values.
        Does NOT reset any changes to the data being displayed in the graph. The 'reset_data' function in the View package
        should be used for that purpose.
        """
        self.axes_shown = True
        self.show_as_px = True
        #self.set_xlims(self.default_xlim)
        #self.set_ylims(self.default_ylim)
        self.aspect_ratio = (4, 4, 3)
        self.change_color_map()
        self.set_viewing_angles()

    def change_color_map(self, color_map=DEFAULT_COLOR_MAP):
        self.color_map = color_map

    def set_viewing_angles(self, azim=-60.0, elev=30.0):
        """
        Sets the two viewing angles for a 3D plot.

        :param azim: Azimuthal viewing angle
        :param elev: Elevation viewing angle
        """
        self.azim = azim
        self.elev = elev
