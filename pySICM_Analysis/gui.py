"""
TODO add module documentation
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QHBoxLayout, QListWidget, QLabel, QAction, QWidget, QVBoxLayout, QSplitter, QStyle, \
    QActionGroup, QMainWindow

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class SecondaryWindow(QWidget):
    """
    This widget will appear as a free-floating window if
    it has no parent.
    """

    def __init__(self, parent=None):
        super().__init__()
        self.toolbar = None
        self.canvas = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        print(self.parent())

    def add_canvas(self, canvas):
        self.canvas = canvas
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()
        self.close_window = pyqtSignal()
        self.central_widget = QtWidgets.QWidget(self)
        self.imported_files_list = QListWidget(self)
        self.data_manipulation_list = QListWidget(self)
        self.init_ui()
        self.set_menus_enabled(False)

    def init_ui(self):
        pixmap = QStyle.SP_FileIcon
        icon_files = self.style().standardIcon(pixmap)
        pixmap = QStyle.SP_DriveFDIcon
        icon_export = self.style().standardIcon(pixmap)
        pixmap = QStyle.SP_DirOpenIcon
        icon_directory = self.style().standardIcon(pixmap)

        label_imported_files = QLabel("Imported files:")
        label_data_manipulations = QLabel("Data manipulations on selected view:")
        self.setCentralWidget(self.central_widget)
        horizontal_layout = QHBoxLayout()

        vertical_layout_top = QVBoxLayout()
        vertical_layout_top.addWidget(label_imported_files)
        vertical_layout_top.addWidget(self.imported_files_list)
        top = QWidget()
        top.setLayout(vertical_layout_top)

        vertical_layout_bottom = QVBoxLayout()
        vertical_layout_bottom.addWidget(label_data_manipulations)
        vertical_layout_bottom.addWidget(self.data_manipulation_list)
        bottom = QWidget()
        bottom.setLayout(vertical_layout_bottom)

        self.horizontal_splitter = QSplitter(Qt.Horizontal)

        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.vertical_splitter.addWidget(top)
        self.vertical_splitter.addWidget(bottom)
        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        self.horizontal_splitter.addWidget(self.vertical_splitter)
        horizontal_layout.addWidget(self.horizontal_splitter)
        self.central_widget.setLayout(horizontal_layout)

        # File menu
        self.action_clear = QtWidgets.QAction('&Clear', self)
        self.action_import_files = QAction(icon_files, "&Import Files...", self)
        self.action_import_directory = QAction(icon_directory, '&Import Directory...', self)
        self.action_export_file = QAction(icon_export, '&Export to file', self)
        self.action_export_bitmap = QAction('&As bitmap (png)', self)
        self.action_export_vector = QAction('&as vector (pdf)', self)
        self.action_exit = QtWidgets.QAction('&Exit', self)

        file_menu.addAction(self.action_clear)
        file_menu.addSeparator()
        file_menu.addAction(self.action_import_files)
        file_menu.addAction(self.action_import_directory)
        clipboard_menu = file_menu.addMenu(icon_export, 'Export as image')
        clipboard_menu.addAction(self.action_export_bitmap)
        clipboard_menu.addAction(self.action_export_vector)
        file_menu.addAction(self.action_export_file)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        # Edit menu
        self.action_undo = QAction("Undo", self)
        self.action_redo = QAction("Redo", self)
        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)

        # View menu
        self.action_toggle_axes = QAction('&Show axes', self)
        self.action_toggle_axes.setCheckable(True)
        self.action_toggle_axes.setChecked(True)
        self.action_view_restore = QAction('&Restore view', self)
        self.action_view_ratio = QAction('Aspect ratio', self)
        action_view_surface = QAction('&Interpolate surface', self)
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_ylimits = QAction('&Adjust y limits', self)
        self.action_view_colormap = QAction('Colormap', self)
        self.action_store_angles = QAction('Store viewing angles', self)

        self.action_set_axis_labels_px = QAction("pixels", self)
        self.action_set_axis_labels_px.setCheckable(True)

        self.action_set_axis_labels_micron = QAction("µm", self)
        self.action_set_axis_labels_micron.setCheckable(True)

        self.view_menu = menubar.addMenu("&View")
        self.view_menu.addAction(self.action_toggle_axes)
        axis_label_menu = self.view_menu.addMenu('Set axis labels to...')
        axis_label_menu.addAction(self.action_set_axis_labels_px)
        axis_label_menu.addAction(self.action_set_axis_labels_micron)

        action_group_axis_labels = QActionGroup(self)
        action_group_axis_labels.addAction(self.action_set_axis_labels_px)
        action_group_axis_labels.addAction(self.action_set_axis_labels_micron)
        action_group_axis_labels.setExclusive(True)
        self.action_set_axis_labels_px.setChecked(True)

        self.view_menu.addAction(self.action_store_angles)
        self.view_menu.addAction(self.action_view_ratio)
        # view_menu.addAction(action_view_surface)
        self.view_menu.addAction(action_view_xlimits)
        self.view_menu.addAction(action_view_ylimits)
        self.view_menu.addAction(self.action_view_colormap)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.action_view_restore)

        # Manipulate data menu
        self.action_data_crop = QAction('Crop', self)
        self.action_data_default = QAction('Apply default scale', self)
        self.action_data_minimum = QAction('Subtract minimum', self)
        self.action_data_transpose_z = QAction('Transpose Z', self)
        self.action_data_filter = QAction("Filter data", self)
        self.action_data_plane = QAction('Plane', self)
        action_data_paraboloid = QAction('Paraboloid', self)
        action_data_line = QAction('Linewise', self)
        action_data_linemean = QAction('Linewise (mean)', self)
        action_data_liney = QAction('Linewise Y', self)
        action_data_poly = QAction('polyXX', self)
        action_data_splines = QAction('by cubic splines', self)
        action_data_neighbor = QAction('by nearest neighbor', self)
        self.action_data_reset = QAction('Reset data manipulations', self)

        self.data_menu = menubar.addMenu("&Manipulate data")
        simple_menu = self.data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(self.action_data_crop)
        simple_menu.addAction(self.action_data_default)
        simple_menu.addAction(self.action_data_minimum)
        simple_menu.addAction(self.action_data_transpose_z)
        self.data_menu.addAction(self.action_data_filter)
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
        self.data_menu.addSeparator()
        self.data_menu.addAction(self.action_data_reset)

        # Measurements menu
        action_measure_dist = QAction('&Measure distance', self)
        action_measure_profile = QAction('&Measure profile', self)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(action_measure_dist)
        self.measure_menu.addAction(action_measure_profile)

        # Properties menu
        self.properties_menu = menubar.addMenu("&Properties")

        # About menu
        self.about_menu = menubar.addMenu("&About")
        self.action_about = QAction('click test', self)

        self.about_menu.addAction(self.action_about)

        # Help menu
        # this menu should contain instruction how to use the software
        # and information about algorithms used in data analysis

        self.setGeometry(700, 350, 800, 800)
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
        self.horizontal_splitter.addWidget(canvas)

    def display_status_bar_message(self, message):
        self.statusBar().showMessage(message)

    def add_items_to_list(self, items):
        self.imported_files_list.addItems(items)

    def clear_list_widget(self):
        self.imported_files_list.clear()

    def get_item_list_count(self):
        """Returns the number of items
        in the imported files list."""
        return self.imported_files_list.count()
