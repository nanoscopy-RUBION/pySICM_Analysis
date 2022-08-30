import math
import sys
import time
import traceback
from os import listdir
from os.path import join, isfile

import numpy as np
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QFileDialog

from pySICM_Analysis.gui import MainWindow
from pySICM_Analysis.graph_canvas import GraphCanvas
from pySICM_Analysis.gui_filter_dialog import FilterDialog
from pySICM_Analysis.manipulate_data import transpose_data, subtract_minimum, crop
from pySICM_Analysis.manipulate_data import filter_median_temporal, filter_median_spatial, filter_average_temporal, filter_average_spatial
from pySICM_Analysis.sicm_data import SICMDataFactory, ApproachCurve
from pySICM_Analysis.view import View

# APP CONSTANTS
APP_NAME = "pySICM Analysis"
APP_ICON_PATH = '../resources/pySICMsplash.png'
TITLE = f"{APP_NAME} (ver. 2022-08-24)"
DEFAULT_FILE_PATH = "../"

# FILTERS
MEDIAN_TEMPORAL = "Median (temporal)"
MEDIAN_SPATIAL = "Median (spatial)"
AVERAGE_TEMPORAL = "Average (temporal)"
AVERAGE_SPATIAL = "Average (spatial)"


class Controller:

    def __init__(self, main_window):
        self.main_window = main_window
        self.unsaved_changes = False
        self.itemList = []
        self.viewList = []
        self.currentItem = None
        self.currentView = None
        self.cid = None
        self.figure_canvas = GraphCanvas()

    def add_canvas_to_main_window(self):
        self.main_window.add_canvas(self.figure_canvas)

    def connect_actions(self):
        """Connect functions with actions in the main window's menu."""
        # File menu
        self.main_window.action_clear.triggered.connect(self.clear_lists)
        self.main_window.action_import_files.triggered.connect(self.import_files)
        self.main_window.action_import_directory.triggered.connect(self.import_directory)

        self.main_window.action_exit.triggered.connect(self.quit_application)

        # View menu
        self.main_window.action_toggle_axes.triggered.connect(self.toggle_axes)
        self.main_window.action_set_axis_labels_px.triggered.connect(self.update_figures_and_status)
        self.main_window.action_set_axis_labels_micron.triggered.connect(self.update_figures_and_status)
        self.main_window.action_store_angles.triggered.connect(self.store_viewing_angles)
        self.main_window.action_view_restore.triggered.connect(self.restore_current_view_settings)

        # Data manipulation
        self.main_window.action_data_transpose_z.triggered.connect(self.transpose_z_of_current_view)
        self.main_window.action_data_minimum.triggered.connect(self.subtract_minimum_in_current_view)
        self.main_window.action_data_reset.triggered.connect(self.reset_current_view_data)
        self.main_window.action_data_filter.triggered.connect(self.filter_current_view)

        # Other
        self.main_window.imported_files_list.currentItemChanged.connect(self.item_selection_changed_event)
        self.main_window.action_about.triggered.connect(self.about)
        self.main_window.closeEvent = self.quit_application

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
            self.currentView.set_z_data(filters.get(selected_filter)(self.currentView.z_data, radius))
            self.update_figures_and_status()

    def quit_application(self, event):
        # TODO dialogue unsaved changes
        print("quit")
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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
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

    def get_filenames_from_selected_files(self, directory=".."):
        """Opens a directory to import all .sicm files (Does not search subdirectories)."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
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
        if files:
            if len(files) > 1:
                message_end = " files."
            else:
                message_end = " file."
            self.main_window.add_items_to_list(files)
            self.main_window.set_menus_enabled(True)
            self.main_window.display_status_bar_message("Imported " + str(len(files)) + message_end)
        else:
            self.main_window.display_status_bar_message("No files imported.")

    def clear_lists(self):
        """Removes all items from list widget and disables menus."""
        self.main_window.clear_list_widget()
        self.main_window.set_menus_enabled(False)
        self.currentItem = None
        self.currentView = None
        self.itemList.clear()
        self.viewList.clear()
        self.main_window.display_status_bar_message("Files removed from the list.")

    def toggle_axes(self):
        """Shows or hides axes in figures.
        """
        self.currentView.toggle_axes()
        self.figure_canvas.update_plots(self.currentView)

    def item_selection_changed_event(self, item):
        """Updates the figure canvas and menu availability when the
        list selection has changed.
        """
        if item:
            self.main_window.action_toggle_axes.setEnabled(True)
            self.currentItem = item

            if self.currentItem not in self.itemList:
                self.itemList.append(item)
                self.currentView = View(SICMDataFactory().get_sicm_data(item.text()))
                self.viewList.append(self.currentView)
            else:
                self.currentView = self.viewList[self.itemList.index(self.currentItem)]

            self.main_window.action_toggle_axes.setChecked(self.currentView.axes_shown)

            self.update_figures_and_status()
        else:
            self.main_window.action_toggle_axes.setEnabled(False)

    def transpose_z_of_current_view(self):
        """Transposes z data of current measurement of all types
        except ApproachCurves.
        """
        if not isinstance(self.currentView.sicm_data, ApproachCurve):
            self.currentView.set_z_data(transpose_data(self.currentView.z_data))
            self.update_figures_and_status()

    def subtract_minimum_in_current_view(self):
        self.currentView.set_z_data(subtract_minimum(self.currentView.get_z_data()))
        self.update_figures_and_status()

    def update_figures_and_status(self):
        """Redraws figures on the canvas and updates statusbar message.
        """
        self.currentView.show_as_px = self.main_window.action_set_axis_labels_px.isChecked()
        self.figure_canvas.update_plots(self.currentView)
        try:
            self.main_window.display_status_bar_message(
                "Max: %s  Min: %s, x_px: %s, x_size: %s µm, label px: %s" % (
                    str(np.max(self.currentView.get_z_data())),
                    str(np.min(self.currentView.get_z_data())),
                    str(self.currentView.sicm_data.x_px),
                    str(self.currentView.sicm_data.x_size),
                    str(self.currentView.show_as_px)
                ))
        except:
            self.main_window.display_status_bar_message("approach curve")

    def store_viewing_angles(self):
        """Stores the two viewing angles in the View object.
        This is only possible for scans that are not of the type
        ApproachCurve.
        """
        try:
            self.currentView.set_viewing_angles(*self.figure_canvas.get_viewing_angles_from_3d_plot())
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

    def about(self):

        if not self.cid:
            if len(self.figure_canvas.figure.get_axes()) > 1:
                self.cid_press = self.figure_canvas.figure.canvas.mpl_connect('button_press_event', self.origin_point)
                #self.cid = self.figure_canvas.figure.canvas.mpl_connect('button_press_event', self.click_on_raster_image)
                #self.cid = self.figure_canvas.figure.canvas.mpl_connect("motion_notify_event", self.mouse_over_value)
        else:
            self.figure_canvas.figure.canvas.mpl_disconnect(self.cid)
            self.cid = None

    def mouse_over_value(self, event):
        print("z: %s µm " % self.get_data_from_point(QPoint(int(event.xdata), int(event.ydata))))
        print("Coords: X %s | Y %s " % (event.xdata, event.ydata))
        time.sleep(0.2)

    def origin_point(self, event):
        if event.name == "button_press_event":
            self.P1 = QPoint(int(event.xdata), int(event.ydata))
            self.cid_release = self.figure_canvas.figure.canvas.mpl_connect('button_release_event', self.rectangle_test)
            self.cid_move = self.figure_canvas.figure.canvas.mpl_connect('motion_notify_event', self.rectangle_test)

    def rectangle_test(self, event):
        """TODO Clean up the code and move it to another class"""
        import matplotlib.patches as patches


        if event.name == "motion_notify_event":
        #    print("move..")

            self.update_figures_and_status()
            self.P2 = QPoint(int(event.xdata), int(event.ydata))
            print("P1: %s, P2: %s" % (self.P1, self.P2))
            width = abs(self.P1.x() - self.P2.x()) +1
            height = abs(self.P1.y() - self.P2.y()) +1
            if self.P1.x() < self.P2.x():
                orig_x = self.P1.x()
            else:
                orig_x = self.P2.x()
            if self.P1.y() < self.P2.y():
                orig_y = self.P1.y()
            else:
                orig_y = self.P2.y()
            origin = (orig_x, orig_y)
            rect = patches.Rectangle(xy=origin, width=width, height=height, linewidth=1, edgecolor='r', facecolor='none')
            self.figure_canvas.figure.get_axes()[1].add_patch(rect)
            self.figure_canvas.draw()
        if event.name == "button_release_event":
            self.figure_canvas.figure.canvas.mpl_disconnect(self.cid_move)
            crop(self.currentView, self.P1, self.P2)
            self.update_figures_and_status()
            self.cid_move = None
            self.P1 = None
            self.P2 = None
       # if event.name == 'button_press_event':
       #     self.P1 = QPoint(int(event.xdata), int(event.ydata))
       #     print(self.P1)
       # else:
       #     self.P2 = QPoint(int(event.xdata), int(event.ydata))
       #     print(self.P2)


    def get_data_from_point(self, point: QPoint):
        """"""
        return self.currentView.z_data[point.y(), point.x()]

    def click_on_raster_image(self, event):
        """A test function for getting the correct pixel after clicking on it.
        TODO Clean up and move to another class
        """
        from pySICM_Analysis.gui import SecondaryWindow
        axes = event.canvas.figure.get_axes()[0]
        print(event)
        if event.inaxes == axes:
            print("oben")
        else:

            self.w = SecondaryWindow(self.main_window)
            self.w.add_canvas(GraphCanvas())
            self.w.show()

            self.last_change = None
            self.X = None
            self.Y = None

            print("unten")
            print("x: %s, y: %s" % (event.xdata, event.ydata))
            # coordinates need to be adjusted when imshow is used
            # instead of pcolormesh for 2D plots
            x = int(event.xdata)# + 0.5)
            y = int(event.ydata)# + 0.5)

            self.w.canvas.figure.clear()
            self.w.canvas.axes = self.w.canvas.figure.add_subplot(111)
            self.w.canvas.axes.plot(self.currentView.x_data[y, :], self.currentView.z_data[y, :])

            if not self.last_change:
                self.X = x
                self.Y = y
                self.last_change = self.currentView.z_data[y, x]
                #self.currentView.z_data[y, x] = 0.0
                self.figure_canvas.update_plots(self.currentView)
            else:
                print("Last: %s" % self.last_change)
                self.currentView.z_data[self.Y, self.X] = self.last_change
                #self.last_change = self.currentView.z_data[y, x]
                self.currentView.z_data[y, x] = 0.0
                self.X = x
                self.Y = y
                self.figure_canvas.update_plots(self.currentView)
                print(self.X, self.Y)
            print(self.currentView.z_data[x, y])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(APP_ICON_PATH))

    window = MainWindow()
    window.setWindowTitle(TITLE)

    controller = Controller(window)
    controller.add_canvas_to_main_window()
    controller.connect_actions()

    sys.exit(app.exec())
