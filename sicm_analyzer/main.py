import os
import sys

from sicm_analyzer.line_profile_window import LineProfileWindow

sys.path.append("")
import traceback
import numpy as np

from os import listdir
from os.path import join, isfile
from matplotlib.figure import Figure

from PyQt6.QtCore import QPoint, QEvent, Qt
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QListWidget

from sicm_analyzer.data_manager import DataManager
from sicm_analyzer.results import ResultsWindow
from sicm_analyzer.colormap_dialog import ColorMapDialog
from sicm_analyzer.enter_area_dialog import EnterAreaDialog
from sicm_analyzer.gui_main import MainWindow, SecondaryWindow
from sicm_analyzer.graph_canvas import GraphCanvas
from sicm_analyzer.filter_dialog import FilterDialog
from sicm_analyzer.manipulate_data import transpose_z_data, subtract_z_minimum, crop
from sicm_analyzer.manipulate_data import filter_median_temporal, filter_median_spatial, filter_average_temporal, \
    filter_average_spatial
from sicm_analyzer.manipulate_data import level_data
from sicm_analyzer.mouse_events import MouseInteraction
from sicm_analyzer.sicm_data import ApproachCurve, ScanBackstepMode, export_sicm_file
from sicm_analyzer.view import View
from sicm_analyzer.graph_canvas import SURFACE_PLOT, RASTER_IMAGE, APPROACH_CURVE
from sicm_analyzer.set_rois_dialog import ROIsDialog
from sicm_analyzer.measurements import polynomial_fifth_degree

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
        self.data_manager = DataManager()
        self.unsaved_changes = False
        self.current_selection: str = ""
        self.cmap_dialog = None
        self.results_window: ResultsWindow = None
        self.view = View()
        self.figure_canvas_3d = GraphCanvas()
        self.figure_canvas_2d = GraphCanvas()
        self.mi = MouseInteraction()

    def set_listener_function_in_data_manager(self):
        self.data_manager.listener_function = self.update_figures_and_status

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
        self.main_window.action_export_sicm_data.triggered.connect(self.export_sicm_data)
        self.main_window.action_exit.triggered.connect(self.quit_application)

        # Edit menu
        self.main_window.action_undo.triggered.connect(self.undo)
        self.main_window.action_redo.triggered.connect(self.redo)

        # View menu
        self.main_window.action_toggle_axes.triggered.connect(self.toggle_axes)
        self.main_window.action_set_axis_labels_px.triggered.connect(self.update_figures_and_status)
        self.main_window.action_set_axis_labels_micron.triggered.connect(self.update_figures_and_status)
        self.main_window.action_store_angles.triggered.connect(self.store_viewing_angles)
        self.main_window.action_view_restore.triggered.connect(self.restore_view_settings)
        self.main_window.action_view_colormap.triggered.connect(self.open_color_map_dialog)
        self.main_window.action_view_ratio.triggered.connect(self.open_aspect_ratio_input_dialog)

        # Data manipulation
        self.main_window.action_data_transpose_z.triggered.connect(self.transpose_z_of_current_view)
        self.main_window.action_data_minimum.triggered.connect(self.subtract_minimum_in_current_view)
        self.main_window.action_data_reset.triggered.connect(self.reset_current_data_manipulations)
        self.main_window.action_data_filter.triggered.connect(self.filter_current_view)
        self.main_window.action_data_level_plane.triggered.connect(self.plane_correction)
        self.main_window.action_data_crop_input.triggered.connect(self.crop_by_input)
        self.main_window.action_data_crop_select.triggered.connect(self.crop_by_selection)
        self.main_window.action_data_poly.triggered.connect(self.fit_to_polyXX)

        # Measurement
        self.main_window.action_set_rois.triggered.connect(self.show_roi_dialog)
        self.main_window.action_set_roi.triggered.connect(self.select_roi_with_mouse)
        self.main_window.action_line_profile_row.triggered.connect(self.select_line_profile_row)
        self.main_window.action_line_profile_column.triggered.connect(self.select_line_profile_column)

        # Other
        self.main_window.imported_files_list.currentItemChanged.connect(self.item_selection_changed_event)
        self.main_window.action_roughness.triggered.connect(self.show_results)
        # self.main_window.action_about.triggered.connect(self.about)
        self.main_window.closeEvent = self.quit_application

        # Key Events
        self.main_window.delete_key = self.remove_selection

    def export_figure(self, figure: Figure):
        """Exports the current view of a figure."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self.main_window,
                                                caption="Export figure as...",
                                                filter="All files (*.*);;BMP (*.bmp);;GIF (*.gif);;JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;SVG (*.svg);;TIF (*.tif);;TIFF (*.tiff)",
                                                directory=DEFAULT_FILE_PATH,
                                                initialFilter="SVG (*.svg)",
                                                options=options
                                                )
        if file_path[0]:
            figure.savefig(fname=file_path[0])
            self.main_window.display_status_bar_message("Figure saved")

    def export_sicm_data(self):
        """Exports the z data of the current selection as a .sicm file."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self.main_window,
                                                caption="Export manipulated data as .sicm file",
                                                filter="All files (*.*);;SICM (*.sicm)",
                                                directory=DEFAULT_FILE_PATH,
                                                initialFilter="SICM (*.sicm)",
                                                options=options
                                                )
        if file_path[0]:
            if file_path[0].lower().endswith(".sicm"):
                file_path = file_path[0]
            else:
                file_path = file_path[0] + ".sicm"
            export_sicm_file(file_path, self.data_manager.get_data(self.current_selection))

    def undo(self):
        self.data_manager.undo_manipulation(self.current_selection)
        self._undo_redo()

    def redo(self):
        self.data_manager.redo_manipulation(self.current_selection)
        self._undo_redo()

    def _undo_redo(self):
        self.update_figures_and_status()

    def _update_undo_redo_menu_items(self):
        self.main_window.set_undo_menu_items(
            self.data_manager.is_undoable(self.current_selection),
            self.data_manager.get_undo_text(self.current_selection)
        )
        self.main_window.set_redo_menu_items(
            self.data_manager.is_redoable(self.current_selection),
            self.data_manager.get_redo_text(self.current_selection)
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
        self.view.aspect_ratio = aspect_r
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
            self.data_manager.execute_func_on_current_data(
                filters.get(selected_filter),
                key=self.current_selection,
                action_name=f"selected_filter (px-size: {radius})"
            )(self.data_manager.get_data(self.current_selection), radius)

    def plane_correction(self):
        """TODO: implement more functions"""
        self.data_manager.execute_func_on_current_data(
            level_data,
            key=self.current_selection,
            action_name="Leveling (plane)"
        )(self.data_manager.get_data(self.current_selection))

    def fit_to_polyXX(self):
        """TODO: implement more functions"""
        self.data_manager.execute_func_on_current_data(
            self._helper_for_fit,
            key=self.current_selection,
            action_name="Leveling (polyXX)"
        )()

    def _helper_for_fit(self):
        data = self.data_manager.get_data(self.current_selection)
        data.z = data.z - polynomial_fifth_degree(data.x, data.y, data.z)

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

    def remove_selection(self):
        """TODO doc"""
        try:
            index = self.main_window.imported_files_list.selectionModel().currentIndex().row()
            item = self.main_window.imported_files_list.currentItem()
            data_key = item.text()
            self.data_manager.remove_data(data_key)
            self.main_window.imported_files_list.takeItem(index)
        except:
            pass

    def add_files_to_list(self, files):
        """
        Adds file paths to the list widget.
        :param files: list of files
        """
        new_files = self.data_manager.get_files_without_duplicates(files)
        self.data_manager.import_files(files)
        if new_files:
            self.main_window.add_items_to_list(new_files)
            self.main_window.set_menus_enabled(True)

            if len(new_files) > 1:
                message_end = " files."
            else:
                message_end = " file."
            self.main_window.display_status_bar_message("Imported " + str(len(new_files)) + message_end)
        else:
            self.main_window.display_status_bar_message("No files imported.")

    def clear_lists(self):
        """Removes all items from list widget and disables menus."""
        self.main_window.clear_list_widgets()
        self.data_manager.clear_all_data()
        self.main_window.set_menus_enabled(False)
        self.main_window.set_undo_menu_items()
        self.main_window.set_redo_menu_items()
        self.main_window.display_status_bar_message("Files removed from the list.")

    def toggle_axes(self):
        """Shows or hides axes in figures.
        """
        self.view.toggle_axes()
        self.update_figures_and_status()

    def item_selection_changed_event(self, item):
        """Updates the figure canvas and menu availability when the
        list selection has changed.
        """
        if item:
            self.main_window.action_toggle_axes.setEnabled(True)
            self.current_selection = item.text()
            self.main_window.set_menus_enabled(isinstance(self.data_manager.get_data(self.current_selection), ScanBackstepMode))

            self.main_window.action_toggle_axes.setChecked(self.view.axes_shown)
            self.update_figures_and_status()
        else:
            self.main_window.action_toggle_axes.setEnabled(False)

    def transpose_z_of_current_view(self):
        """Transposes z data of current measurement of all types
        except ApproachCurves.
        """
        if not isinstance(self.data_manager.get_data(self.current_selection), ApproachCurve):
            self.data_manager.execute_func_on_current_data(
                transpose_z_data,
                key=self.current_selection,
                action_name="Transpose z"
            )(self.data_manager.get_data(self.current_selection))

    def subtract_minimum_in_current_view(self):
        self.data_manager.execute_func_on_current_data(
            subtract_z_minimum,
            key=self.current_selection,
            action_name="Subtract z minimum"
        )(self.data_manager.get_data(self.current_selection))

    def update_figures_and_status(self, message: str = ""):
        """Redraws figures on the canvas and updates statusbar message.

        An optional message will be concatenated to the status bar message.
        """
        try:
            current_data = self.data_manager.get_data(self.current_selection)
            self.view.show_as_px = self.main_window.action_set_axis_labels_px.isChecked()

            if isinstance(current_data, ScanBackstepMode):
                self.figure_canvas_3d.draw_graph(current_data, SURFACE_PLOT, self.view)
                self.figure_canvas_2d.draw_graph(current_data, RASTER_IMAGE, self.view)

            if isinstance(current_data, ApproachCurve):
                self.figure_canvas_3d.draw_graph(current_data)
                self.figure_canvas_2d.draw_graph(current_data, APPROACH_CURVE, self.view)

            self._update_undo_redo_menu_items()
            self.main_window.set_data_manipulation_list_items(
                self.data_manager.get_undoable_manipulations_list(self.current_selection)
            )
        except:
            pass
        try:
            self.main_window.display_status_bar_message(
                "Max: %s  Min: %s, x_px: %s, x_size: %s µm, Message:  %s" % (
                    str(np.max(current_data.z)),
                    str(np.min(current_data.z)),
                    str(current_data.x_px),
                    str(current_data.x_size),
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
            self.view.set_viewing_angles(*self.figure_canvas_3d.get_viewing_angles_from_3d_plot())
        except AttributeError:
            self.main_window.display_status_bar_message("ApproachCurves have no viewing angles.")
            self.view.set_viewing_angles()

    def restore_view_settings(self):
        """Sets all viewing settings in the current View object
        to default values.
        """
        try:
            self.view.restore()
            self.main_window.action_toggle_axes.setChecked(True)
            self.main_window.action_set_axis_labels_px.setChecked(True)
            self.update_figures_and_status()
        except Exception as e:
            print('No view to restore')
            print(str(e))
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    def reset_current_data_manipulations(self):
        self.data_manager.reset_manipulations(self.current_selection)
        self.update_figures_and_status("Reset data of View object.")

    def select_roi_with_mouse(self):
        data = self.data_manager.get_data(self.current_selection)
        self.figure_canvas_2d.draw_rectangle_on_raster_image(data=data, view=self.view, func=self._select_area)

    def _select_area(self, point1: QPoint, point2: QPoint):
        print("TODO ROI selection")
        if self._points_are_not_equal(point1, point2):
            #self.current_selection.rois = (point1, point2)
            self.update_figures_and_status("ROI set")
        else:
            self.update_figures_and_status("No ROI set.")

    def crop_by_input(self):
        dialog = EnterAreaDialog(controller=self, parent=self.main_window)
        if dialog.exec():
            point1, point2 = dialog.get_input_as_points()
            self._crop_data(point1, point2)
        else:
            self.main_window.display_status_bar_message("Data not cropped.")

    def crop_by_selection(self):
        self.figure_canvas_2d.draw_rectangle_on_raster_image(
            data=self.data_manager.get_data(self.current_selection),
            view=self.view,
            func=self._crop_data
        )

    def _crop_data(self, point1: QPoint, point2: QPoint):
        if self._points_are_not_equal(point1, point2):
            self.data_manager.execute_func_on_current_data(
                crop,
                self.current_selection,
                action_name="Crop data"
            )(self.data_manager.get_data(self.current_selection), point1, point2)
        else:
            self.update_figures_and_status("Data not cropped.")

    def _points_are_not_equal(self, point1: QPoint, point2: QPoint) -> bool:
        """Checks if two points have the same coordinates."""
        return point1.x() != point2.x() and point1.y() != point2.y()

    def select_line_profile_row(self):
        """TODO"""
        self.figure_canvas_2d.draw_line_profile(
            data=self.data_manager.get_data(self.current_selection),
            view=self.view,
            func=self._show_line_profile_row
        )

    def select_line_profile_column(self):
        """TODO"""
        self.figure_canvas_2d.draw_line_profile(
            data=self.data_manager.get_data(self.current_selection),
            view=self.view,
            func=self._show_line_profile_column
        )

    def _show_line_profile_row(self, index: int = -1, selection_mode: str = "row"):
        """TODO"""
        if index >= 0:
            x = self.data_manager.get_data(self.current_selection).x
            z = self.data_manager.get_data(self.current_selection).z
            shape = z.shape
            if selection_mode == "row" and index <= shape[0]:

                self.line_profile = SecondaryWindow(self.main_window)
                canvas = GraphCanvas()
                self.line_profile.add_canvas(canvas)
                self.line_profile.show()
                canvas.plot_line_profile(x[index, :], z[index, :])

    def _show_line_profile_column(self, index: int, selection_mode: str = "column"):
        """TODO"""
        if index and index >= 0:
            x = self.data_manager.get_data(self.current_selection).x
            z = self.data_manager.get_data(self.current_selection).z
            shape = z.shape
            if selection_mode == "column" and index <= shape[0]:
                self.line_profile = SecondaryWindow(self.main_window)
                canvas = GraphCanvas()
                self.line_profile.add_canvas(canvas)
                self.line_profile.show()
                canvas.plot_line_profile(x[index, :], z[index, :])


    def show_roi_dialog(self):
        self.roi_dialog = ROIsDialog(controller=self, parent=self.main_window)
        self.roi_dialog.open_window()

    def show_results(self):
        self.results_window = ResultsWindow(self,
                                            data=self.data_manager.get_data(self.current_selection),
                                            parent=self.main_window)
        self.results_window.open_window()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(APP_ICON_PATH))

    window = MainWindow()
    window.resource_dir = RESOURCE_DIRECTORY
    window.setWindowTitle(TITLE)

    controller = Controller(window)
    controller.add_canvases_to_main_window()
    controller.set_listener_function_in_data_manager()
    controller.connect_actions()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
