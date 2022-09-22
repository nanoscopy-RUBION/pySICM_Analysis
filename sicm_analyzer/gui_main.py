"""
TODO add module documentation
"""
import os
from os.path import join
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QActionGroup, QKeyEvent

from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QLabel, QWidget, QVBoxLayout, QSplitter, QStyle, \
    QMainWindow, QToolBar, QAbstractItemView, QDockWidget

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib

try:
    matplotlib.use('QtAgg')
except:
    matplotlib.use("agg")


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

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resource_dir = join(os.getcwd(), "resources")
        self.close_window = pyqtSignal()
        self.central_widget = QtWidgets.QWidget(self)
        self.imported_files_list = QListWidget(self)
        self.data_manipulation_list = QListWidget(self)
        self.init_ui()
        self.set_menus_enabled(False)

    def init_ui(self):
        pixmap = QStyle.StandardPixmap.SP_FileIcon
        icon_files = self.style().standardIcon(pixmap)
        pixmap = QStyle.StandardPixmap.SP_DriveFDIcon
        icon_export = self.style().standardIcon(pixmap)
        pixmap = QStyle.StandardPixmap.SP_DirOpenIcon
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
        self.data_manipulation_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.data_manipulation_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        bottom = QWidget()
        bottom.setLayout(vertical_layout_bottom)

        self.horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        self.vertical_splitter.addWidget(top)
        self.vertical_splitter.addWidget(bottom)
        self.vertical_splitter.setStretchFactor(0, 6)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        self.horizontal_splitter.addWidget(self.vertical_splitter)
        horizontal_layout.addWidget(self.horizontal_splitter)

        # DockWidgets
        self.dock_3d_plot = QDockWidget("3D graph", self)
        self.dock_3d_plot.setFloating(False)
        self.dock_2d_plot = QDockWidget("2D graph", self)
        self.dock_2d_plot.setFloating(False)
        self.central_widget.setLayout(horizontal_layout)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_3d_plot)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_2d_plot)


        # File menu
        self.action_clear = QAction(QIcon(join(self.resource_dir, "pySICM64.png")), '&Clear', self)
        self.action_import_files = QAction(icon_files, "&Import Files...", self)
        self.action_import_directory = QAction(icon_directory, '&Import Directory...', self)
        self.action_export_sicm_data = QAction(icon_export, 'Export sicm data', self)
        self.action_export_file = QAction(icon_export, 'Export view object', self)
        self.action_export_file.setEnabled(False)
        self.action_export_3d = QAction("3D graph", self)
        self.action_export_2d = QAction("2D graph", self)
        self.action_exit = QAction('&Exit', self)

        file_menu.addAction(self.action_clear)
        file_menu.addSeparator()
        file_menu.addAction(self.action_import_files)
        file_menu.addAction(self.action_import_directory)
        clipboard_menu = file_menu.addMenu(icon_export, 'Export graph')
        clipboard_menu.addAction(self.action_export_3d)
        clipboard_menu.addAction(self.action_export_2d)
        file_menu.addAction(self.action_export_sicm_data)
        file_menu.addAction(self.action_export_file)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        # Edit menu
        self.action_undo = QAction("Undo", self)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_redo = QAction("Redo", self)
        self.action_redo.setShortcut("Ctrl+R")
        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)

        self.action_toggle_toolbar = QAction("Show/Hide toolbar", self)
        self.action_toggle_toolbar.triggered.connect(self.toggle_show_toolbar)
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.action_toggle_toolbar)

        # View menu
        self.action_toggle_axes = QAction('&Show axes', self)
        self.action_toggle_axes.setCheckable(True)
        self.action_toggle_axes.setChecked(True)
        self.action_view_restore = QAction('&Restore view', self)
        self.action_view_ratio = QAction('Aspect ratio', self)
        action_view_surface = QAction('&Interpolate surface', self)
        action_view_surface.setEnabled(False)  # TODO
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_xlimits.setEnabled(False)  # TODO
        action_view_ylimits = QAction('&Adjust y limits', self)
        action_view_ylimits.setEnabled(False)  # TODO
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
        self.view_menu.addAction(action_view_surface)
        self.view_menu.addAction(action_view_xlimits)
        self.view_menu.addAction(action_view_ylimits)
        self.view_menu.addAction(self.action_view_colormap)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.action_view_restore)

        # Manipulate data menu
        self.action_data_crop_input = QAction('Enter range...', self)
        self.action_data_crop_select = QAction('Select area...', self)
        self.action_data_minimum = QAction('Subtract minimum', self)
        self.action_data_transpose_z = QAction('Transpose Z', self)
        self.action_data_filter = QAction("Filter data", self)
        self.action_data_level_plane = QAction('Plane', self)
        action_data_paraboloid = QAction('Paraboloid', self)
        action_data_paraboloid.setEnabled(False)  # TODO
        action_data_line = QAction('Linewise', self)
        action_data_line.setEnabled(False)  # TODO
        action_data_linemean = QAction('Linewise (mean)', self)
        action_data_linemean.setEnabled(False)  # TODO
        action_data_liney = QAction('Linewise Y', self)
        action_data_liney.setEnabled(False)  # TODO
        self.action_data_poly = QAction('polyXX (5th)', self)

        action_data_splines = QAction('by cubic splines', self)
        action_data_splines.setEnabled(False)  # TODO
        action_data_neighbor = QAction('by nearest neighbor', self)
        action_data_neighbor.setEnabled(False)  # TODO
        self.action_data_reset = QAction('Reset data manipulations', self)

        self.data_menu = menubar.addMenu("&Manipulate data")
        crop_menu = self.data_menu.addMenu("Crop")
        crop_menu.addAction(self.action_data_crop_input)
        crop_menu.addAction(self.action_data_crop_select)
        simple_menu = self.data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(self.action_data_minimum)
        simple_menu.addAction(self.action_data_transpose_z)
        self.data_menu.addAction(self.action_data_filter)
        flatten_menu = self.data_menu.addMenu('Leveling')
        flatten_menu.addAction(self.action_data_level_plane)
        flatten_menu.addAction(action_data_paraboloid)
        flatten_menu.addAction(action_data_line)
        flatten_menu.addAction(action_data_linemean)
        flatten_menu.addAction(action_data_liney)
        flatten_menu.addAction(self.action_data_poly)
        interpolation_menu = self.data_menu.addMenu('Interpolation')
        interpolation_menu.addAction(action_data_splines)
        interpolation_menu.addAction(action_data_neighbor)
        self.data_menu.addSeparator()
        self.data_menu.addAction(self.action_data_reset)

        # Measurements menu
        self.action_roughness = QAction("Roughness")
        self.action_roughness.setEnabled(False)
        action_measure_dist = QAction('&Measure distance', self)
        action_measure_dist.setEnabled(False)  # TODO
        action_measure_profile = QAction('&Measure profile', self)
        action_measure_profile.setEnabled(False)  # TODO
        self.action_set_rois = QAction("ROIs", self)
        self.action_set_roi = QAction("Set ROI", self)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(self.action_roughness)
        self.measure_menu.addAction(action_measure_dist)
        self.measure_menu.addAction(action_measure_profile)
        self.measure_menu.addAction(self.action_set_rois)
        self.measure_menu.addAction(self.action_set_roi)

        # About menu
        self.about_menu = menubar.addMenu("&About")
        self.action_about = QAction('click test', self)

        self.about_menu.addAction(self.action_about)

        # Help menu
        # this menu should contain instruction how to use the software
        # and information about algorithms used in data analysis

        # Key events
        self.imported_files_list.installEventFilter(self)
        self.delete_key = None


        self.toolbar = QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.action_import_files)
        self.toolbar.addAction(self.action_clear)

        self.action_test_dock = QAction("Show dock")
        self.action_test_dock.triggered.connect(self.show_graphs)
        self.toolbar.addAction(self.action_test_dock)

        self.toolbar.addSeparator()
        self.addToolBar(self.toolbar)

        self.setGeometry(700, 350, 800, 800)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def eventFilter(self, source, event):
        """Add key events here:
        At the moment the following key events are recognized:

        Key_Delete
        """
        if event.type() is QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Delete:
                try:
                    self.delete_key()
                except:
                    pass
        return super().eventFilter(source, event)

    def show_graphs(self):
        if not self.dock_3d_plot.isVisible():
            self.dock_3d_plot.show()
        if not self.dock_2d_plot.isVisible():
            self.dock_2d_plot.show()

    def set_menus_enabled(self, enable):
        self.view_menu.setEnabled(enable)
        self.data_menu.setEnabled(enable)
        self.measure_menu.setEnabled(enable)
        self.action_roughness.setEnabled(enable)
        self.about_menu.setEnabled(enable)

    def toggle_show_toolbar(self):
        if self.toolbar.isVisible():
            self.toolbar.setVisible(False)
        else:
            self.toolbar.setVisible(True)

    def add_canvas_for_3d_plot(self, canvas):
        self.dock_3d_plot.setWidget(canvas)

    def add_canvas_for_2d_plot(self, canvas):
        self.dock_2d_plot.setWidget(canvas)

    def display_status_bar_message(self, message):
        self.statusBar().showMessage(message)

    def add_items_to_list(self, items):
        self.imported_files_list.addItems(items)

    def clear_list_widgets(self):
        self.imported_files_list.clear()
        self.data_manipulation_list.clear()

    def get_item_list_count(self):
        """Returns the number of items
        in the imported files list."""
        return self.imported_files_list.count()

    def set_undo_menu_items(self, enabled: bool = False, text=""):
        default = "Undo "
        try:
            self.action_undo.setEnabled(enabled)
            self.action_undo.setText(default + text)
        except TypeError:
            self.action_undo.setEnabled(enabled)
            self.action_undo.setText(default)

    def set_redo_menu_items(self, enabled: bool = False, text=""):
        default = "Redo "
        try:
            self.action_redo.setEnabled(enabled)
            self.action_redo.setText(default + text)
        except TypeError:
            self.action_redo.setEnabled(enabled)
            self.action_redo.setText(default)

    def set_data_manipulation_list_items(self, items):
        self.data_manipulation_list.clear()
        self.data_manipulation_list.addItems(items)
