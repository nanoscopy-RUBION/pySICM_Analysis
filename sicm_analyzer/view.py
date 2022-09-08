import copy
import matplotlib
import numpy as np
from PyQt6.QtCore import QPoint

from sicm_analyzer.undo_redo import UndoRedoData
from sicm_analyzer.sicm_data import ApproachCurve, ScanBackstepMode, SICMdata

DEFAULT_COLOR_MAP = matplotlib.cm.YlGnBu_r


class View:
    """
    This class contains the data and viewing settings for SICM data. One instance of the view class is linked to each file imported.
    This relationship starts when the item is first selected from the list. The relationship is preversed , although certain 
    features (such as rotation of )
    """

    def __init__(self, data: SICMdata):
        self.sicm_data = data
        self.axes_shown = True
        self.show_as_px = True
        self.color_bar_shown = True
        self.aspect_ratio = (4, 4, 3)  # Default value by matplotlib
        self.color_map = DEFAULT_COLOR_MAP
        self.rois = (QPoint(), QPoint())

        # These two lists should be treated as stacks
        # for undo (data_manipulations) and redo (redoable_manipulations)
        self.data_manipulations: list[UndoRedoData] = list()
        self.redoable_manipulations: list[UndoRedoData] = list()

        if isinstance(self.sicm_data, ScanBackstepMode):
            self.x_data, self.y_data, self.z_data = data.set_data()
            self.x_data = np.array(self.x_data)
            self.y_data = np.array(self.y_data)
            self.z_data = np.array(self.z_data)

            self.azim = -60.0
            self.elev = 30.0
        elif isinstance(self.sicm_data, ApproachCurve):
            self.x_data, self.z_data = data.set_data()
            self.x_data = np.array(self.x_data)
            self.z_data = np.array(self.z_data)
        else:
            self.x_data = np.zeros((2, 2))
            self.y_data = np.zeros((2, 2))
            self.z_data = np.zeros((2, 2))

    # Undo/Redo section
    # ---------------------------------------------------------------------------------------------
    def store_undoable_action(self, action_name="action"):
        data = self._make_undoredoable_data_object()
        undoable = UndoRedoData(name=action_name, data=data)
        self.data_manipulations.append(undoable)

    def _make_undoredoable_data_object(self):
        if isinstance(self.sicm_data, ScanBackstepMode):
            data = (
                copy.deepcopy(self.x_data),
                copy.deepcopy(self.y_data),
                copy.deepcopy(self.z_data)
            )
        else:
            data = (
                copy.deepcopy(self.x_data),
                copy.deepcopy(self.z_data)
            )
        return data

    def store_redoable_data(self):
        data = self._make_undoredoable_data_object()
        self.data_manipulations[-1].redodata = data

    def undo_manipulation(self):
        undoredoable = self.data_manipulations.pop()
        self._restore_data_from_undoable(undoredoable.undodata)
        self.redoable_manipulations.append(undoredoable)

    def redo_manipulation(self):
        undoredoable = self.redoable_manipulations.pop()
        self._restore_data_from_undoable(undoredoable.redodata)
        self.data_manipulations.append(undoredoable)

    def _restore_data_from_undoable(self, undoredoable_data: tuple):
        """This function copies data obtained from the undo
        or redo stack to the x, y, and z_data fields to restore
        a previous state."""
        if isinstance(self.sicm_data, ScanBackstepMode):
            self.x_data = copy.deepcopy(undoredoable_data[0])
            self.y_data = copy.deepcopy(undoredoable_data[1])
            self.z_data = copy.deepcopy(undoredoable_data[2])

        if isinstance(self.sicm_data, ApproachCurve):
            self.x_data = copy.deepcopy(undoredoable_data[0])
            self.z_data = copy.deepcopy(undoredoable_data[1])

    def is_undoable(self):
        return len(self.data_manipulations) > 0

    def is_redoable(self):
        return len(self.redoable_manipulations) > 0

    def get_undo_text(self):
        try:
            return self.data_manipulations[-1].name
        except IndexError:
            return ""

    def get_redo_text(self):
        try:
            return self.redoable_manipulations[-1].name
        except IndexError:
            return ""

    def get_undoable_manipulations_list(self) -> list[str]:
        items = []
        for item in self.data_manipulations:
            items.append(item.name)
        return items
    # Undo/Redo section END
    # ---------------------------------------------------------------------------------------------

    def get_raw_data(self):
        """
        Returns the underlying data from the SICMFactory class used to build the class. Notably, this data is NOT
        modified by data manipulation. To obtain the manipulated data, use get_modified_data instead.

        :returns: Unmodified data extracted from imported file. For approach curves
        x and z are returned; for data from backstep mode scans x, y, and z.
        """
        return self.sicm_data.set_data()

    def get_modified_data(self):
        """Returns modified data for plotting.

        :return: Manipulated data, e.g. filtered data. For approach curves
        x and z are returned; for data from backstep mode scans x, y, and z.
        """
        if isinstance(self.sicm_data, ScanBackstepMode):
            return self.x_data, self.y_data, self.z_data
        else:
            return self.x_data, self.z_data

    def set_data(self, data):
        self.x_data, self.y_data, self.z_data = np.array(data)

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

    def reset_data(self):
        """Restores the original sicm data."""
        self.set_data(self.sicm_data.set_data())
        self.data_manipulations = []

