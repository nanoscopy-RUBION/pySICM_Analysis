
import matplotlib
from PyQt6.QtCore import QPoint

DEFAULT_COLOR_MAP = matplotlib.cm.YlGnBu_r


class View:
    """
    This class no longer contains data. It will only handle representation of data in figures.
    """

    def __init__(self):
        self.axes_shown: bool = True
        self.show_as_px: bool = True
        self.z_in_nm: bool = False
        self.color_bar_shown: bool = True
        self.aspect_ratio: tuple[int, int, int] = (4, 4, 3)  # Default value by matplotlib
        self.color_map = DEFAULT_COLOR_MAP
        self.rois = (QPoint(), QPoint())
        self.azim: float = -60.0
        self.elev: float = 30.0
        self.x_limits: tuple[float, float] | None = None
        self.y_limits: tuple[float, float] | None = None
        self.z_limits: tuple[float, float] | None = None

    def toggle_axes(self):
        """
        Changes the state of axis visibility.
        """
        self.axes_shown = not self.axes_shown

    def set_x_limits(self, limits: tuple[float, float] | None):
        self.x_limits = limits

    def set_y_limits(self, limits: tuple[float, float] | None):
        self.y_limits = limits

    def set_z_limits(self, limits: tuple[float, float] | None):
        self.z_limits = limits

    def toggle_color_bar(self):
        """
        Switches the color bar on or off.
        """
        self.color_bar_shown = not self.color_bar_shown

    def show_axes(self):
        return self.axes_shown

    def show_color_bar(self):
        return self.color_bar_shown

    def restore(self):
        """
        Resets all viewing options (graph limits, whether axes are shown, aspect ratio, etc.)
        to their default values.
        Does NOT reset any changes to the data being displayed in the graph.
        """
        self.axes_shown = True
        self.show_as_px = True
        self.x_limits = None
        self.y_limits = None
        self.z_limits = None
        self.aspect_ratio = (4, 4, 3)
        self.change_color_map()
        self.set_viewing_angles()

    def change_color_map(self, color_map=DEFAULT_COLOR_MAP):
        self.color_map = color_map

    def set_viewing_angles(self, azim: float = -60.0, elev: float = 30.0):
        """
        Sets the two viewing angles for a 3D plot.

        :param azim: Azimuthal viewing angle
        :param elev: Elevation viewing angle
        """
        self.azim = azim
        self.elev = elev
