
import matplotlib
from PyQt6.QtCore import QPoint

DEFAULT_COLOR_MAP = matplotlib.cm.YlGnBu_r


class View:
    """
    A class to store settings for displaying SICMdata.
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
        self.z_in_nm = False

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

    def get_view_as_dict(self):
        return self.__dict__

    def apply_view_settings(self, view: "View"):
        settings = self.get_view_as_dict().keys()
        for field in settings:
            self.get_view_as_dict()[field] = view.get_view_as_dict().get(field)


class ViewManager:
    """This class manages View objects for SICMdata objects."""
    def __init__(self):
        self.views = {}

    def get_all_views(self):
        """Returns an iterable containing all View objects."""
        return self.views.values()

    def reset_list(self, keys: list[str]):
        """Resets Views to its default values for each element
        in the list of keys."""
        for key in keys:
            self.views.get(key).restore()

    def reset_all_views(self):
        """Resets all Views to its default values."""
        for view in self.get_all_views():
            view.restore()

    def apply_selected_view_to_all(self, key: str):
        """Apply View settings to all other View objects."""
        _view = self.views[key]
        for view in self.get_all_views():
            view.apply_view_settings(_view)

    def apply_selected_to_list(self, key: str, keys: list[str]):
        """
        Apply View settings to all View objects in the list.

        :param key: key of View of which the settings should be applied to
        other views
        :param keys: list of keys of View objects to which the settings
        should be applied
        """
        _view = self.views[key]
        for view in self.get_views_of_list(keys):
            view.apply_view_settings(_view)

    def get_view(self, key) -> View | None:
        """Instantiates a new View object which is associated with
        a SICMData object.

        :param key: a unique string to reference an SICMdata object
        :return: Returns the View object associated with a SICMdata object that
        is reference by a key string
        """
        return self.views.get(key, None)

    def get_views_of_list(self, keys: list[str]) -> list[View]:
        """Returns a list of View objects for a list of associated keys."""
        views = []
        for key in keys:
            views.append(self.views.get(key))
        return views

    def create_view(self, key: str):
        """Instantiates a new View object which is associated with
        a SICMData object.

        :param key: a unique string to reference a SICMdata object
        """
        self.views[key] = View()

    def create_views(self, keys: list[str]):
        """Instantiates a new View object which is associated with
        a SICMData object for each element in a list of keys.

        :param keys: a list of unique strings referencing SICMdata objects
        """
        for key in keys:
            self.create_view(key)

    def remove_view(self, key: str):
        """Instantiates a new View object which is associated with
        a SICMData object.

        :param key: a unique string to reference a SICMdata object
        """
        del self.views[key]

    def clear_all_views(self):
        """Delete all View objects."""
        self.views.clear()
