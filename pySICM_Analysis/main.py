import sys
import traceback
from os import listdir
from os.path import join, isfile

import numpy as np

from PyQt5.QtWidgets import QApplication, QFileDialog

from gui import MainWindow
from graph_canvas import GraphCanvas
from manipulate_data import transpose_data, subtract_minimum
from sicm_data import SICMDataFactory, ApproachCurve
from view import View


class Controller:

    def __init__(self, main_window):
        self.main_window = main_window
        self.unsaved_changes = False
        self.itemList = []
        self.viewList = []
        self.currentItem = None
        self.currentView = None

        self.figure_canvas = GraphCanvas()

    def add_canvas_to_main_window(self):
        self.main_window.add_canvas(self.figure_canvas)

    def connect_actions(self):
        """Connect functions with actions in the main windows menu."""
        # File menu
        self.main_window.action_clear.triggered.connect(self.clear_lists)
        self.main_window.action_import_files.triggered.connect(self.import_files)
        self.main_window.action_import_directory.triggered.connect(self.import_directory)

        self.main_window.action_exit.triggered.connect(self.quit_application)

        # View menu
        self.main_window.action_toggle_axes.triggered.connect(self.toggle_axes)
        self.main_window.action_store_angles.triggered.connect(self.store_viewing_angles)
        self.main_window.action_view_restore.triggered.connect(self.restore_current_view_settings)

        # Data manipulation
        self.main_window.action_data_transpose_z.triggered.connect(self.transpose_z_of_current_view)
        self.main_window.action_data_minimum.triggered.connect(self.subtract_minimum_in_current_view)
        self.main_window.action_data_reset.triggered.connect(self.reset_current_view_data)

        # Other
        self.main_window.list_widget.currentItemChanged.connect(self.item_selection_changed_event)

    def quit_application(self):
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
        self.figure_canvas.update_plots(self.currentView)
        self.main_window.display_status_bar_message("Max: %s  Min: %s" % (
            str(np.max(self.currentView.get_z_data())),
            str(np.min(self.currentView.get_z_data()))
        ))

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = Controller(window)
    controller.add_canvas_to_main_window()
    controller.connect_actions()
    sys.exit(app.exec())
