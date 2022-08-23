"""
TODO add module documentation
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QListWidget, QLabel, QAction, QWidget, QVBoxLayout, QSplitter

import matplotlib
matplotlib.use('Qt5Agg')

TITLE = "pySICM Analyzer (2022_08_22_1)"


class SecondaryWindow(QWidget):
    """
    This widget will appear as a free-floating window if
    it has no parent.
    CURRENTLY UNUSED AND NOT WORKING..
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        # for testing click events
        self.last_change = None
        self.X = None
        self.Y = None
        # GUI elements
        self.central_widget = QtWidgets.QWidget(self)
        self.list_widget = QListWidget(self)

        self.init_ui()
        self.set_menus_enabled(False)

    def init_ui(self):
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()
        self.splitter = QSplitter(Qt.Horizontal)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        self.splitter.addWidget(self.list_widget)
        layout.addWidget(self.splitter)
        self.central_widget.setLayout(layout)

        self.action_clear = QtWidgets.QAction('&Clear', self)
        self.action_import_files = QAction("&Import Files...", self)
        self.action_import_directory = QAction('&Import Directory...', self)
        self.action_export_file = QAction('&Export to file', self)
        self.action_export_bitmap = QAction('&As bitmap (png)', self)
        self.action_export_vector = QAction('&as vector (pdf)', self)
        self.action_exit = QtWidgets.QAction('&Exit', self)

        file_menu.addAction(self.action_clear)
        file_menu.addSeparator()
        file_menu.addAction(self.action_import_files)
        file_menu.addAction(self.action_import_directory)
        clipboard_menu = file_menu.addMenu('Export as image')
        clipboard_menu.addAction(self.action_export_bitmap)
        clipboard_menu.addAction(self.action_export_vector)
        file_menu.addAction(self.action_export_file)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        self.action_toggle_axes = QAction('&Show axes', self)
        self.action_toggle_axes.setCheckable(True)
        self.action_toggle_axes.setChecked(True)
        self.action_view_restore = QAction('&Restore view', self)
        action_view_ratio = QAction('&Aspect ratio', self)
        action_view_surface = QAction('&Interpolate surface', self)
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_ylimits = QAction('&Adjust y limits', self)
        action_view_colormap = QAction('&Colormap', self)
        self.action_store_angles = QAction('Store viewing angles', self)


        self.view_menu = menubar.addMenu("&View")
        self.view_menu.addAction(self.action_toggle_axes)
        self.view_menu.addAction(self.action_store_angles)
        self.view_menu.addAction(action_view_ratio)
        # view_menu.addAction(action_view_surface)
        self.view_menu.addAction(action_view_xlimits)
        self.view_menu.addAction(action_view_ylimits)
        self.view_menu.addAction(action_view_colormap)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.action_view_restore)

        action_data_crop = QAction('&Crop', self)
        action_data_default = QAction('&Apply default scale', self)
        self.action_data_minimum = QAction('&Subtract minimum', self)
        self.action_data_transpose_z = QAction('&Transpose Z', self)
        self.action_data_median = QAction('&Temporal Median', self)
        action_data_average = QAction('&Temporal Average', self)
        action_data_smedian = QAction('&Spatial Median', self)
        action_data_saverage = QAction('&Spatial Average', self)
        self.action_data_plane = QAction('&Plane', self)
        action_data_paraboloid = QAction('&Paraboloid', self)
        action_data_line = QAction('&Linewise', self)
        action_data_linemean = QAction('&Linewise (mean)', self)
        action_data_liney = QAction('&Linewise Y', self)
        action_data_poly = QAction('&polyXX', self)
        action_data_splines = QAction('&by cubic splines', self)
        action_data_neighbor = QAction('&by nearest neighbor', self)
        self.action_data_reset = QAction('&Reset data manipulations', self)

        self.data_menu = menubar.addMenu("&Manipulate data")
        simple_menu = self.data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(action_data_crop)
        simple_menu.addAction(action_data_default)
        simple_menu.addAction(self.action_data_minimum)
        simple_menu.addAction(self.action_data_transpose_z)
        filter_menu = self.data_menu.addMenu('Filter')
        filter_menu.addAction(self.action_data_median)
        filter_menu.addAction(action_data_average)
        filter_menu.addAction(action_data_smedian)
        filter_menu.addAction(action_data_saverage)
        flatten_menu = self.data_menu.addMenu('Leveling')
        flatten_menu.addAction(self.action_data_plane)
        flatten_menu.addAction(action_data_paraboloid)
        flatten_menu.addAction(action_data_line)
        flatten_menu.addAction(action_data_linemean)
        flatten_menu.addAction(action_data_liney)
        flatten_menu.addAction(action_data_poly)
        interpolation_menu = self.data_menu.addMenu('Interpolation')
        interpolation_menu.addAction(action_data_splines)
        interpolation_menu.addAction(action_data_neighbor)
        self.data_menu.addAction(self.action_data_reset)

        action_measure_dist = QAction('&Measure distance', self)
        action_measure_profile = QAction('&Measure profile', self)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(action_measure_dist)
        self.measure_menu.addAction(action_measure_profile)

        self.properties_menu = menubar.addMenu("&Properties")

        self.about_menu = menubar.addMenu("&About")
        action_about = QAction('click test', self)

        self.about_menu.addAction(action_about)

        self.setGeometry(700, 350, 800, 800)
        self.setWindowTitle(TITLE)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def set_menus_enabled(self, enable):
        self.view_menu.setEnabled(enable)
        self.data_menu.setEnabled(enable)
        self.measure_menu.setEnabled(enable)
        self.properties_menu.setEnabled(enable)
        self.about_menu.setEnabled(enable)

    def add_canvas(self, canvas):
        self.splitter.addWidget(canvas)

    def display_status_bar_message(self, message):
        self.statusBar().showMessage(message)

    def add_items_to_list(self, items):
        self.list_widget.addItems(items)

    def clear_list_widget(self):
        self.list_widget.clear()

    def about(self):
        w = SecondaryWindow()
        w.show()
        if len(self.canvas.figure.get_axes()) > 1:
            self.cid = self.canvas.figure.canvas.mpl_connect('button_press_event', self.click_on_raster_image)

    def click_on_raster_image(self, event):
        """A test function for getting the correct pixel after clicking on it.

        """
        axes = event.canvas.figure.get_axes()[0]
        if event.inaxes == axes:
            print("oben")
        else:
            print("unten")
            print("x: %s, y: %s" % (event.xdata, event.ydata))
            x = int(event.xdata + 0.5)
            y = int(event.ydata + 0.5)
            if not self.last_change:
                self.X = x
                self.Y = y
                self.last_change = self.currentView.z_data[y, x]
                self.currentView.z_data[y, x] = 0.0
                self.update_plots(self.currentView, self.currentData)
            else:
                print("Last: %s" % self.last_change)
                self.currentView.z_data[self.Y, self.X] = self.last_change
                self.last_change = self.currentView.z_data[y, x]
                self.currentView.z_data[y, x] = 0.0
                self.X = x
                self.Y = y
                self.update_plots(self.currentView, self.currentData)
                print(self.X, self.Y)
            print(self.currentView.z_data[x, y])
