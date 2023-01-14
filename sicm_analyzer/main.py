import math
import os
import sys
sys.path.append("")

import traceback
import numpy as np

from pathlib import Path
from os.path import join
from matplotlib.figure import Figure
from skimage import measure

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog

from sicm_analyzer.data_manager import DataManager
from sicm_analyzer.results import ResultsWindow
from sicm_analyzer.colormap_dialog import ColorMapDialog
from sicm_analyzer.enter_area_dialog import EnterAreaDialog
from sicm_analyzer.gui_main import MainWindow
from sicm_analyzer.graph_canvas import GraphCanvas
from sicm_analyzer.filter_dialog import FilterDialog
from sicm_analyzer.manipulate_data import transpose_z_data, subtract_z_minimum, crop, invert_z_data
from sicm_analyzer.manipulate_data import filter_median_temporal, filter_median_spatial, filter_average_temporal, \
    filter_average_spatial
from sicm_analyzer.manipulate_data import level_data
from sicm_analyzer.mouse_events import MouseInteraction, points_are_not_equal, is_in_range, ROW, COLUMN, CROSS
from sicm_analyzer import sicm_data
from sicm_analyzer.sicm_data import ApproachCurve, ScanBackstepMode, export_sicm_file
from sicm_analyzer.view import View
from sicm_analyzer.graph_canvas import SURFACE_PLOT, RASTER_IMAGE, APPROACH_CURVE
from sicm_analyzer.set_rois_dialog import ROIsDialog
from sicm_analyzer.measurements import polynomial_fifth_degree
from sicm_analyzer.line_profile_window import LineProfileWindow


# APP CONSTANTS
APP_NAME = "pySICM Analysis"
APP_PATH = os.getcwd()
RESOURCE_DIRECTORY = "resources"
APP_ICON = "pySICMsplash.png"
APP_ICON_PATH = join(APP_PATH, RESOURCE_DIRECTORY, APP_ICON)
TITLE = f"{APP_NAME} (ver. 2023-01-13)"
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
        self.main_window.action_remove_selection.triggered.connect(self.remove_selection)
        self.main_window.action_import_files.triggered.connect(self.import_files)
        self.main_window.action_import_directory.triggered.connect(self.import_directory)
        self.main_window.action_export_2d.triggered.connect(lambda: self.export_figure(self.figure_canvas_2d.figure))
        self.main_window.action_export_3d.triggered.connect(lambda: self.export_figure(self.figure_canvas_3d.figure))
        self.main_window.action_export_sicm_data.triggered.connect(self.export_sicm_data)
        self.main_window.action_export_sicm_data_multi.triggered.connect(self.export_sicm_data_multi)
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
        self.main_window.action_data_invert_z.triggered.connect(self.invert_z_in_current_view)
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
        self.main_window.action_line_profile_xy.triggered.connect(self.show_xy_profile)
        self.main_window.action_line_profile_line.triggered.connect(self.select_line_profile_line)
        self.main_window.action_measure_dist.triggered.connect(self.measure_distance)

        # Other
        self.main_window.imported_files_list.currentItemChanged.connect(self.item_selection_changed_event)
        self.main_window.action_results.triggered.connect(self.show_results)
        # self.main_window.action_about.triggered.connect(self.about)
        self.main_window.set_drop_event_function(self.import_files_by_drag_and_drop)
        self.main_window.closeEvent = self.quit_application

        # Key Events
        self.main_window.delete_key = self.remove_selection
        self.main_window.escape_key = self.figure_canvas_2d.unbind_mouse_events

    def export_figure(self, figure: Figure):
        """Exports the current view of a figure."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self.main_window,
                                                caption="Export figure as...",
                                                filter="All files (*.*);;EPS (*.eps);;PDF (*.pdf);;JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;SVG (*.svg);;TIF (*.tif);;TIFF (*.tiff)",
                                                directory=DEFAULT_FILE_PATH,
                                                initialFilter="SVG (*.svg)",
                                                options=options
                                                )
        if file_path[0]:
            file, extension = self._get_file_name_with_extension(file_path)
            try:
                figure.savefig(fname=file, format=extension)
                self.main_window.display_status_bar_message(f"Figure saved as: {file}")
            except ValueError as e:
                message = str(e)
                self.main_window.display_status_bar_message(f"Figure not exported: {message}")

    def export_sicm_data(self):
        """Exports the z data of the current selection as a .sicm file.

        File extension is added when file name does not end with
        .sicm."""
        try:
            data = self.data_manager.get_data(self.current_selection)
            if data and (data.scan_mode == sicm_data.BACKSTEP or data.scan_mode == sicm_data.FLOATING_BACKSTEP):
                options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
                file_path = QFileDialog.getSaveFileName(parent=self.main_window,
                                                        caption="Export manipulated data as .sicm file",
                                                        filter="SICM (*.sicm)",
                                                        directory=DEFAULT_FILE_PATH,
                                                        initialFilter="SICM (*.sicm)",
                                                        options=options
                                                        )
                if file_path[0]:
                    file, _ = self._get_file_name_with_extension(file_path)
                    export_sicm_file(file, sicm_data=data)
            else:
                self.main_window.display_status_bar_message("No file exported.")
        except TypeError:
            self.main_window.display_status_bar_message("No file selected for export.")

    def export_sicm_data_multi(self):
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        directory = str(QFileDialog.getExistingDirectory(parent=self.main_window,
                                                         caption="Select Directory",
                                                         directory=DEFAULT_FILE_PATH,
                                                         options=options))
        for item in self.main_window.get_all_checked_items():
            data = self.data_manager.get_data(item)
            if data and (data.scan_mode == sicm_data.BACKSTEP or data.scan_mode == sicm_data.FLOATING_BACKSTEP):
                if directory and os.path.isdir(directory):
                    name = Path(item).name
                    full_path = os.path.join(directory, name)
                    export_sicm_file(full_path, data)


    def _get_file_name_with_extension(self, file_dialog_path: tuple[str, str]) -> (str, str):
        """Checks the file path from a QFileDialog and returns
        the full path of the file with the correct file extension.
        Additionally, the file extension without . is returned
        which can be used for matplotlib's savefig function.

        This function removes leading and trailing whitespaces.
        File extensions are always in lower case.
        """
        file = file_dialog_path[0].strip()
        if os.path.splitext(file_dialog_path[0])[1]:
            extension = os.path.splitext(file_dialog_path[0])[1][1:]
        else:
            extension = file_dialog_path[1][:file_dialog_path[1].index(" ")]
            file = file + "." + extension.lower()
        return file, extension

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
            if aspect_r:
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
        if self.current_selection:
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
        if self.current_selection:
            self.main_window.set_wait_cursor()
            self.data_manager.execute_func_on_current_data(
                level_data,
                key=self.current_selection,
                action_name="Leveling (plane)"
            )(self.data_manager.get_data(self.current_selection))
            self.main_window.set_default_cursor()

    def fit_to_polyXX(self):
        """TODO: implement more functions"""
        if self.current_selection:
            self.main_window.set_wait_cursor()
            self.data_manager.execute_func_on_current_data(
                self._helper_for_fit,
                key=self.current_selection,
                action_name="Leveling (polyXX)"
            )()
            self.main_window.set_default_cursor()

    def _helper_for_fit(self):
        data = self.data_manager.get_data(self.current_selection)
        fitted_z, fit_results = polynomial_fifth_degree(data.x, data.y, data.z)
        data.z = data.z - fitted_z
        data.fit_results = fit_results

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
        """Import all sicm files from a selected directory
        and its subfolders."""
        files = []
        dirname = self.get_filenames_from_selected_directory()
        if dirname:
            files = self.get_sicm_files_from_url_list([dirname])
        self.add_files_to_list(files)

    def import_files_by_drag_and_drop(self, urls):
        """Handles file import by drag and drop.
        Files and directories are supported.
        """
        files = self.get_sicm_files_from_url_list(urls)
        self.add_files_to_list(files)

    def get_sicm_files_from_url_list(self, urls):
        """Returns a list of .sicm file paths."""
        files = []
        for url in urls:
            if os.path.isdir(url):
                files = files + self.get_sicm_files_from_url_list([os.path.join(url, f) for f in os.listdir(url)])
            if os.path.isfile(url) and url.endswith(".sicm"):
                files.append(url)
        return files

    def get_filenames_from_selected_directory(self):
        """Opens a file dialog to choose a directory and
        return that directory path.
        Returns None if no directory has been selected."""
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        dirname = QFileDialog().getExistingDirectory(parent=self.main_window,
                                                     caption='Select Folder',
                                                     options=options
                                                     )
        if not dirname or not os.path.isdir:
            dirname = None
        return dirname

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
        """Remove selected item imported."""
        try:
            index = self.main_window.imported_files_list.selectionModel().currentIndex().row()
            item = self.main_window.imported_files_list.currentItem()
            data_key = item.text()
            self.data_manager.remove_data(data_key)
            self.main_window.imported_files_list.takeItem(index)
        except AttributeError:
            self.main_window.display_status_bar_message("No item selected.")

    def add_files_to_list(self, files):
        """
        Adds file paths to the list widget.

        :param files: list of files
        """
        self.main_window.set_wait_cursor()
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
        self.main_window.set_default_cursor()

    def clear_lists(self):
        """Removes all items from list widget and disables menus."""
        if self.main_window.imported_files_list.count() > 0:
            self.main_window.clear_list_widgets()
            self.data_manager.clear_all_data()
            self.main_window.set_menus_enabled(False)
            self.main_window.set_undo_menu_items()
            self.main_window.set_redo_menu_items()
            self.main_window.display_status_bar_message("Files removed from the list.")
        else:
            self.main_window.display_status_bar_message("No files to remove")

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
        if self.current_selection:
            if not isinstance(self.data_manager.get_data(self.current_selection), ApproachCurve):
                self.data_manager.execute_func_on_current_data(
                    transpose_z_data,
                    key=self.current_selection,
                    action_name="Transpose z"
                )(self.data_manager.get_data(self.current_selection))

    def subtract_minimum_in_current_view(self):
        if self.current_selection:
            self.data_manager.execute_func_on_current_data(
                subtract_z_minimum,
                key=self.current_selection,
                action_name="Subtract z minimum"
            )(self.data_manager.get_data(self.current_selection))

    def invert_z_in_current_view(self):
        if self.current_selection:
            self.data_manager.execute_func_on_current_data(
                invert_z_data,
                key=self.current_selection,
                action_name="Invert z values"
            )(self.data_manager.get_data(self.current_selection))

    def update_figures_and_status(self, message: str = ""):
        """Redraws figures on the canvas and updates statusbar message.

        An optional message will be concatenated to the status bar message.
        """
        try:
            if self.current_selection:
                current_data = self.data_manager.get_data(self.current_selection)
                self.view.show_as_px = self.main_window.action_set_axis_labels_px.isChecked()

                if isinstance(current_data, ScanBackstepMode):
                    self.figure_canvas_3d.draw_graph(current_data, SURFACE_PLOT, self.view)
                    self.figure_canvas_2d.draw_graph(current_data, RASTER_IMAGE, self.view)

                if isinstance(current_data, ApproachCurve):
                    self.figure_canvas_3d.draw_graph(current_data)
                    self.figure_canvas_2d.draw_graph(current_data, APPROACH_CURVE, self.view)

                self.main_window.update_info_labels(
                    scan_date=current_data.get_scan_date(),
                    scan_time=current_data.get_scan_time(),
                    scan_mode=current_data.scan_mode,
                    x_px=current_data.x_px,
                    y_px=current_data.y_px,
                    x_size=current_data.x_size,
                    y_size=current_data.y_size,
                    x_px_raw=current_data.x_px_raw,
                    y_px_raw=current_data.y_px_raw,
                    x_size_raw=current_data.x_size_raw,
                    y_size_raw=current_data.y_size_raw
                )

                self._update_undo_redo_menu_items()
                self.main_window.set_data_manipulation_list_items(
                    self.data_manager.get_undoable_manipulations_list(self.current_selection)
                )
                self.main_window.display_status_bar_message(message)
        except TypeError:
            print("No scan selected.")

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
            self.main_window.show_graphs()
        except TypeError as e:
            print('No view to restore')
            print(str(e))
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    def reset_current_data_manipulations(self):
        if self.current_selection:
            self.data_manager.reset_manipulations(self.current_selection)
            self.update_figures_and_status("Reset data of View object.")

    def select_roi_with_mouse(self):
        data = self.data_manager.get_data(self.current_selection)
        self.figure_canvas_2d.draw_rectangle_on_raster_image(data=data, view=self.view, func=self._select_area)

    def _select_area(self, point1: QPoint, point2: QPoint):
        print("TODO ROI selection")
        if points_are_not_equal(point1, point2):
            #self.current_selection.rois = (point1, point2)
            self.update_figures_and_status("ROI set")
        else:
            self.update_figures_and_status("No ROI set.")

    def crop_by_input(self):
        if self.current_selection:
            dialog = EnterAreaDialog(controller=self, parent=self.main_window)
            if dialog.exec():
                point1, point2 = dialog.get_input_as_points()
                z_array = self.data_manager.get_data(self.current_selection).z
                if is_in_range(point1, z_array) and is_in_range(point2, z_array):
                    self._crop_data(point1, point2)
                else:
                    self.main_window.display_status_bar_message("Invalid input: Data not cropped.")
            else:
                self.main_window.display_status_bar_message("Invalid input: Data not cropped.")

    def crop_by_selection(self):
        if self.current_selection:
            self.figure_canvas_2d.draw_rectangle_on_raster_image(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._crop_data
            )

    def _crop_data(self, point1: QPoint, point2: QPoint):
        if points_are_not_equal(point1, point2):
            self.data_manager.execute_func_on_current_data(
                crop,
                self.current_selection,
                action_name="Crop data"
            )(self.data_manager.get_data(self.current_selection), point1, point2)
        else:
            self.update_figures_and_status("Data not cropped.")

    def select_line_profile_row(self):
        """Show a window displaying a line plot which is
        updated on mouse movement over the 2D canvas.

        Selection mode is row.
        """
        if self.current_selection:
            self._show_line_profile_window()

            self.figure_canvas_2d.bind_mouse_events_for_showing_line_profile(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._show_line_profile,
                clean_up_func=self._focus_line_profile_widget,
                mode=ROW
            )

    def select_line_profile_column(self):
        """Show a window displaying a line plot which is
        updated on mouse movement over the 2D canvas.

        Selection mode is column.
        """
        if self.current_selection:
            self._show_line_profile_window()

            self.figure_canvas_2d.bind_mouse_events_for_showing_line_profile(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._show_line_profile,
                clean_up_func=self._focus_line_profile_widget,
                mode=COLUMN
            )

    def select_line_profile_line(self):
        """TODO EXPERIMENTAL"""
        if self.current_selection:
            self._show_line_profile_window()
            self.figure_canvas_2d.bind_mouse_events_for_draw_line(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._show_line_profile_of_drawn_line,
                clean_up_func=self._focus_line_profile_widget,
            )

    def show_xy_profile(self):
        """Show a window displaying a line plot which is
        updated on mouse movement over the 2D canvas.
        """
        if self.current_selection:
            self._show_line_profile_window()

            self.figure_canvas_2d.bind_mouse_events_for_showing_line_profile(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._show_xy_line_profiles,
                clean_up_func=self._focus_line_profile_widget,
                mode=CROSS
            )

    def _show_line_profile_window(self):
        """Show a small window including a line plot."""
        self.line_profile = LineProfileWindow(self.main_window)
        self.line_profile.add_canvas(GraphCanvas())
        self.line_profile.show()

    def _focus_line_profile_widget(self):
        self.line_profile.raise_()
        self.line_profile.show()

    def _show_line_profile(self, selection_mode: str, index: int = -1):
        if index >= 0:
            data = self.data_manager.get_data(self.current_selection)
            shape = data.z.shape
            if selection_mode == ROW and index <= shape[0]:
                x = data.x
                z = data.z
                self.line_profile.update_plot(x[index, :], z[index, :])
            if selection_mode == COLUMN and index <= shape[1]:
                y = data.y
                z = data.z
                self.line_profile.update_plot(y[:, index], z[:, index])

    def _show_line_profile_of_drawn_line(self, x_data: (int, int) = (-1, -1), y_data: (int, int) = (-1, -1)):
        data = self.data_manager.get_data(self.current_selection)
        try:
            src = (y_data[0], x_data[0])
            dst = (y_data[1], x_data[1])
            plot = measure.profile_line(image=data.z, src=src, dst=dst, linewidth=1, reduce_func=None)
            a = range(plot.shape[0])
            x = np.array(a)
            self.line_profile.update_plot(x=x, y=plot)
        except Exception as e:
            print(e)

    def measure_distance(self):
        if self.current_selection:
            self.figure_canvas_2d.bind_mouse_events_for_draw_line(
                data=self.data_manager.get_data(self.current_selection),
                view=self.view,
                func=self._calculate_distance_between_two_points,
            )

    def _calculate_distance_between_two_points(self, x_data, y_data):
        dist = math.dist((x_data[0], y_data[0]), (x_data[1], y_data[1]))
        print("Distance [px]: %s" % str(dist))

    def _show_xy_line_profiles(self, y_index: int = -1, x_index: int = -1):
        data = self.data_manager.get_data(self.current_selection)
        shape = data.z.shape
        if 0 <= x_index <= shape[0] and 0 <= y_index <= shape[1]:
            x = data.x
            y = data.y
            z = data.z
            self.line_profile.update_xy_line_profile_plot(x[x_index, :], z[x_index, :], y[:, y_index], z[:, y_index])

    def show_roi_dialog(self):
        """TODO not implemented yet"""
        self.roi_dialog = ROIsDialog(controller=self, parent=self.main_window)
        self.roi_dialog.open_window()

    def show_results(self):
        """Shows a small window displaying the results
        of roughness calculation and fit functions. Min and max values
        are also shown.
        """
        try:
            self.results_window = ResultsWindow(self,
                                                data=self.data_manager.get_data(self.current_selection),
                                                parent=self.main_window,
                                                )
            self.results_window.open_window()
        except TypeError:
            pass


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
