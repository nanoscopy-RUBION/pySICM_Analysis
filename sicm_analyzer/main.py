import os
import sys
import traceback
import numpy as np

from os import listdir
from os.path import join, isfile
from matplotlib.figure import Figure

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog

from sicm_analyzer.colormap_dialog import ColorMapDialog
from sicm_analyzer.enter_area_dialog import EnterAreaDialog
from sicm_analyzer.gui_main import MainWindow
from sicm_analyzer.graph_canvas import GraphCanvas
from sicm_analyzer.filter_dialog import FilterDialog
from sicm_analyzer.manipulate_data import transpose_z_data, subtract_z_minimum, crop
from sicm_analyzer.manipulate_data import filter_median_temporal, filter_median_spatial, filter_average_temporal, \
    filter_average_spatial
from sicm_analyzer.manipulate_data import level_data
from sicm_analyzer.mouse_events import MouseInteraction
from sicm_analyzer.sicm_data import SICMDataFactory, ApproachCurve, ScanBackstepMode
from sicm_analyzer.view import View
from sicm_analyzer.graph_canvas import SURFACE_PLOT, RASTER_IMAGE, APPROACH_CURVE

# APP CONSTANTS
APP_NAME = "pySICM Analysis"
APP_PATH = os.getcwd()
RESOURCE_DIRECTORY = "resources"
APP_ICON = "pySICMsplash.png"
APP_ICON_PATH = join(APP_PATH, RESOURCE_DIRECTORY, APP_ICON)
TITLE = f"{APP_NAME} (ver. 2022-09-01)"
DEFAULT_FILE_PATH = os.getcwd()

# FILTERS
MEDIAN_TEMPORAL = "Median (temporal)"
MEDIAN_SPATIAL = "Median (spatial)"
AVERAGE_TEMPORAL = "Average (temporal)"
AVERAGE_SPATIAL = "Average (spatial)"


class Controller:

    def __init__(self, main_window):
        self.main_window: MainWindow = main_window
        self.unsaved_changes = False
        self.views: dict[str, View] = {}
        self.currentView: View = None
        self.cmap_dialog = None
        self.figure_canvas_3d = GraphCanvas()
        self.figure_canvas_2d = GraphCanvas()
        self.mi = MouseInteraction()

    def add_canvases_to_main_window(self):
        self.main_window.add_canvas_for_3d_plot(self.figure_canvas_3d)
        self.main_window.add_canvas_for_2d_plot(self.figure_canvas_2d)

    def connect_actions(self):
        """Connect functions with actions in the main window's menu."""
        # File menu
        self.main_window.action_clear.triggered.connect(self.clear_lists)
        self.main_window.action_import_files.triggered.connect(self.import_files)
        self.main_window.action_import_directory.triggered.connect(self.import_directory)
        self.main_window.action_export_2d.triggered.connect(lambda: self.export_figure(self.figure_canvas_2d.figure))
        self.main_window.action_export_3d.triggered.connect(lambda: self.export_figure(self.figure_canvas_3d.figure))
        self.main_window.action_exit.triggered.connect(self.quit_application)

        # Edit menu
        self.main_window.action_undo.triggered.connect(self.undo)
        self.main_window.action_redo.triggered.connect(self.redo)

        # View menu
        self.main_window.action_toggle_axes.triggered.connect(self.toggle_axes)
        self.main_window.action_set_axis_labels_px.triggered.connect(self.update_figures_and_status)
        self.main_window.action_set_axis_labels_micron.triggered.connect(self.update_figures_and_status)
        self.main_window.action_store_angles.triggered.connect(self.store_viewing_angles)
        self.main_window.action_view_restore.triggered.connect(self.restore_current_view_settings)
        self.main_window.action_view_colormap.triggered.connect(self.open_color_map_dialog)
        self.main_window.action_view_ratio.triggered.connect(self.open_aspect_ratio_input_dialog)

        # Data manipulation
        self.main_window.action_data_transpose_z.triggered.connect(self.transpose_z_of_current_view)
        self.main_window.action_data_minimum.triggered.connect(self.subtract_minimum_in_current_view)
        self.main_window.action_data_reset.triggered.connect(self.reset_current_view_data)
        self.main_window.action_data_filter.triggered.connect(self.filter_current_view)
        self.main_window.action_data_level_plane.triggered.connect(self.plane_correction)
        self.main_window.action_data_crop_input.triggered.connect(self.crop_by_input)
        self.main_window.action_data_crop_select.triggered.connect(self.crop_by_selection)

        # Other
        self.main_window.imported_files_list.currentItemChanged.connect(self.item_selection_changed_event)
        # self.main_window.action_about.triggered.connect(self.about)
        self.main_window.closeEvent = self.quit_application

    def export_figure(self, figure: Figure):
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self.main_window,
                                                caption="Export figure as...",
                                                filter="All files (*.*);;BMP (*.bmp);;GIF (*.gif);;JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;SVG (*.svg);;TIF (*.tif);;TIFF (*.tiff)",
                                                directory=DEFAULT_FILE_PATH,
                                                initialFilter="SVG (*.svg)",
                                                options=options
                                                )
        if file_path:
            figure.savefig(fname=file_path[0])
            self.main_window.display_status_bar_message("Figure saved")

    def undo(self):
        self.currentView.undo_manipulation()
        self._undo_redo()

    def redo(self):
        self.currentView.redo_manipulation()
        self._undo_redo()

    def _undo_redo(self):
        self.update_figures_and_status()

    def _update_undo_redo_menu_items(self):
        self.main_window.set_undo_menu_items(
            self.currentView.is_undoable(),
            self.currentView.get_undo_text()
        )
        self.main_window.set_redo_menu_items(
            self.currentView.is_redoable(),
            self.currentView.get_redo_text()
        )

    def open_color_map_dialog(self):
        """Opens a dialog to choose a color map.
        The selected color map can be applied to the current view
        or to all view objects an once.
        """
        if not self.cmap_dialog:
            self.cmap_dialog = ColorMapDialog(controller=self, parent=self.main_window)
        self.cmap_dialog.open_window()

    def open_aspect_ratio_input_dialog(self):
        input_string, apply = QInputDialog.getText(
            self.main_window, "Aspect Ratio Dialog", "Enter an aspect ratio (X:Y:Z):"
        )
        aspect_r = self._extract_aspect_ratio_tuple_from_string(input_string)
        try:
            self.change_aspect_ratio_for_current_view(aspect_r)
        except ValueError:
            self.main_window.display_status_bar_message("Invalid input for aspect ratio")

    def _extract_aspect_ratio_tuple_from_string(self, input_string: str) -> tuple:
        """Returns a valid tuple for an aspect ratio of three axis.

        Input string should have the form X:Y:Z. The string is separated
        at ":" and freed from white spaces before conversion to a 3-tuple
        containing flaots.

        For invalid input strings an empty tuple is returned.
        """
        try:
            splitted = input_string.split(":")
            trimmed = [element.strip() for element in splitted]
            aspect_r = tuple([float(n) for n in trimmed])
        except ValueError as e:
            self.main_window.display_status_bar_message("Invalid input for aspect ratio")
            aspect_r = tuple()
        return aspect_r

    def change_aspect_ratio_for_current_view(self, aspect_r):
        self.currentView.aspect_ratio = aspect_r
        self.update_figures_and_status()

    def filter_current_view(self):
        filters = {
            MEDIAN_TEMPORAL: filter_median_temporal,
            MEDIAN_SPATIAL: filter_median_spatial,
            AVERAGE_TEMPORAL: filter_average_temporal,
            AVERAGE_SPATIAL: filter_average_spatial,
        }
        dialog = FilterDialog(self.main_window, filters.keys())
        if dialog.exec():
            selected_filter, radius = dialog.get_inputs()
            try:
                radius = int(radius)
            except ValueError:
                radius = 1
            self.undo_wrapper_test(filters.get(selected_filter), name=selected_filter)(self.currentView, radius)

    def plane_correction(self):
        """TODO: implement more functions"""
        self.undo_wrapper_test(level_data, "Leveling (plane)")(self.currentView)

    def quit_application(self, event):
        # TODO dialogue unsaved changes
        if self.unsaved_changes:
            pass
        sys.exit()

    def import_files(self):
        """Opens a file dialog to select sicm files."""
        files = self.get_filenames_from_selected_files()
        self.add_files_to_list(files)

    def import_directory(self):
        """Opens a file dialog to select a directory."""
        files = self.get_filenames_from_selected_directory()
        self.add_files_to_list(files)

    def get_filenames_from_selected_directory(self):
        """Opens a file dialog to choose a directory."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        filenames = []
        dirname = QFileDialog().getExistingDirectory(parent=self.main_window,
                                                     caption='Select Folder',
                                                     options=options
                                                     )
        if dirname:
            filenames = [
                join(dirname, f) for f in listdir(dirname)
                if (isfile(join(dirname, f)) and f.endswith('.sicm'))
            ]
        return filenames

    def get_filenames_from_selected_files(self, directory=DEFAULT_FILE_PATH):
        """Opens a directory to import all .sicm files (Does not search subdirectories)."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        filenames, _ = QFileDialog.getOpenFileNames(parent=self.main_window,
                                                    caption="Import pySICM Scan Files",
                                                    directory=directory,
                                                    filter="pySICM Files (*.sicm)",
                                                    options=options
                                                    )
        return filenames

    def add_files_to_list(self, files):
        """
        Adds file paths to the list widget.
        :param files: list of files
        """
        new_files = self.get_files_without_duplicates(files)
        if new_files:
            self.main_window.add_items_to_list(new_files)
            self._create_view_objects()
            self.main_window.set_menus_enabled(True)

            if len(new_files) > 1:
                message_end = " files."
            else:
                message_end = " file."
            self.main_window.display_status_bar_message("Imported " + str(len(new_files)) + message_end)
        else:
            self.main_window.display_status_bar_message("No files imported.")

    def get_files_without_duplicates(self, files):
        """Returns a list which only includes files that
        have not already been imported.

        A file is a new file if its full file path is not already
        a dictionary key in views."""
        new_files = []
        for file in files:
            if file not in self.views.keys():
                new_files.append(file)
        return new_files

    def get_all_views(self):
        """Returns all View objects as a list."""
        return self.views.values()

    def clear_lists(self):
        """Removes all items from list widget and disables menus."""
        self.main_window.clear_list_widgets()
        self.views.clear()
        self.currentView = None
        self.main_window.set_menus_enabled(False)
        self.main_window.set_undo_menu_items()
        self.main_window.set_redo_menu_items()
        self.main_window.display_status_bar_message("Files removed from the list.")

    def toggle_axes(self):
        """Shows or hides axes in figures.
        """
        self.currentView.toggle_axes()
        self.update_figures_and_status()

    def item_selection_changed_event(self, item):
        """Updates the figure canvas and menu availability when the
        list selection has changed.
        """
        if item:
            self.main_window.action_toggle_axes.setEnabled(True)
            self.currentView = self.views.get(item.text())
            self.main_window.action_toggle_axes.setChecked(self.currentView.axes_shown)
            self.update_figures_and_status()
        else:
            self.main_window.action_toggle_axes.setEnabled(False)

    def _create_view_objects(self):
        for i in range(self.main_window.get_item_list_count()):
            item = self.main_window.imported_files_list.item(i)
            self.views[item.text()] = View(SICMDataFactory().get_sicm_data(item.text()))

    def transpose_z_of_current_view(self):
        """Transposes z data of current measurement of all types
        except ApproachCurves.
        """
        if not isinstance(self.currentView.sicm_data, ApproachCurve):
            self.undo_wrapper_test(transpose_z_data, name="Transpose z")(self.currentView)

    def undo_wrapper_test(self, func, name: str = "action"):
        """This wrapper function is used to make other functions undo/redoable.
        Wrap the function and pass a name for that action.

        Before calling the function, store_undoable_action will be called to store the
        state of the current view object. After the function call, the readoable state
        will be stored and figures will be updated.

        Example to use the wrapper:
            undo_wrapper_test(function, name="Name for that function")(currentView, args)
        """
        self.currentView.store_undoable_action(name)

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            self.currentView.store_redoable_data()
            self.update_figures_and_status()

        return wrapper

    def subtract_minimum_in_current_view(self):
        self.undo_wrapper_test(subtract_z_minimum, "Subtract z minimum")(self.currentView)

    def update_figures_and_status(self, message=""):
        """Redraws figures on the canvas and updates statusbar message.

        An optional message will be concatenated to the status bar message.
        """
        self.currentView.show_as_px = self.main_window.action_set_axis_labels_px.isChecked()
        if isinstance(self.currentView.sicm_data, ScanBackstepMode):
            self.figure_canvas_3d.draw_graph(self.currentView, SURFACE_PLOT)
            self.figure_canvas_2d.draw_graph(self.currentView, RASTER_IMAGE)

        if isinstance(self.currentView.sicm_data, ApproachCurve):
            self.figure_canvas_3d.draw_graph(self.currentView)
            self.figure_canvas_2d.draw_graph(self.currentView, APPROACH_CURVE)

        self._update_undo_redo_menu_items()
        self.main_window.set_data_manipulation_list_items(self.currentView.get_undoable_manipulations_list())
        try:
            self.main_window.display_status_bar_message(
                "Max: %s  Min: %s, x_px: %s, x_size: %s µm, label px: %s  |  %s" % (
                    str(np.max(self.currentView.z_data)),
                    str(np.min(self.currentView.z_data)),
                    str(self.currentView.sicm_data.x_px),
                    str(self.currentView.sicm_data.x_size),
                    str(self.currentView.show_as_px),
                    message
                ))
        except:
            self.main_window.display_status_bar_message("approach curve")

    def store_viewing_angles(self):
        """Stores the two viewing angles in the View object.
        This is only possible for scans that are not of the type
        ApproachCurve. The viewing angles can only be obtained from surface plots.
        """
        try:
            self.currentView.set_viewing_angles(*self.figure_canvas_3d.get_viewing_angles_from_3d_plot())
        except AttributeError:
            self.main_window.display_status_bar_message("ApproachCurves have no viewing angles.")
            self.currentView.set_viewing_angles()

    def restore_current_view_settings(self):
        """Sets all viewing settings in the current View object
        to default values.
        """
        try:
            self.currentView.restore()
            self.update_figures_and_status()
            self.main_window.action_toggle_axes.setChecked(True)
        except Exception as e:
            print('No view to restore')
            print(str(e))
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    def reset_current_view_data(self):
        self.currentView.reset_data()
        self.update_figures_and_status()
        self.main_window.display_status_bar_message("Reset data of View object.")

    def crop_by_input(self):
        dialog = EnterAreaDialog(controller=self, parent=self.main_window)
        if dialog.exec():
            point1, point2 = dialog.get_input_as_points()
            self._crop_data(point1, point2)
        else:
            self.main_window.display_status_bar_message("Data not cropped.")

    def crop_by_selection(self):
        self.figure_canvas_2d.draw_rectangle_on_raster_image(current_view=self.currentView, func=self._crop_data)

    def _crop_data(self, point1: QPoint, point2: QPoint):
        if self._points_are_not_equal(point1, point2):
            self.undo_wrapper_test(crop, name="Crop data")(self.currentView, point1, point2)
        else:
            self.update_figures_and_status("Data not cropped.")

    def _points_are_not_equal(self, point1: QPoint, point2: QPoint) -> bool:
        """Checks if two points have the same coordinates."""
        return point1.x() != point2.x() and point1.y() != point2.y()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(APP_ICON_PATH))

    window = MainWindow()
    window.resource_dir = RESOURCE_DIRECTORY
    window.setWindowTitle(TITLE)

    controller = Controller(window)
    controller.add_canvases_to_main_window()
    controller.connect_actions()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()