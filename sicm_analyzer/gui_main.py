"""
TODO add module documentation
"""
import os
from os.path import join
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QActionGroup, QKeyEvent, QDragEnterEvent, QDropEvent, QCursor

from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QLabel, QWidget, QVBoxLayout, QSplitter, QStyle, \
    QMainWindow, QToolBar, QAbstractItemView, QDockWidget, QGridLayout, QPlainTextEdit, QTextEdit

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
        self.setAcceptDrops(True)

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

        # info widget
        info_layout = QVBoxLayout()
        info_label = QLabel("Metadata:")
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMinimumHeight(100)
        #self.info_text.setFixedHeight(160)
        info_layout.addWidget(info_label)
        info_layout.addWidget(self.info_text)
        info_widget = QWidget()
        info_widget.setLayout(info_layout)

        self.vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        self.vertical_splitter.addWidget(info_widget)
        self.vertical_splitter.addWidget(top)
        self.vertical_splitter.addWidget(bottom)
        self.vertical_splitter.setStretchFactor(0, 1)
        self.vertical_splitter.setStretchFactor(1, 5)
        self.vertical_splitter.setStretchFactor(2, 2)

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
        self.action_clear = QAction(QIcon(join(self.resource_dir, "clear.png")), '&Clear list', self)
        self.action_remove_selection = QAction("Remove selection", self)
        self.action_remove_selection.setShortcut("Ctrl+D")
        self.action_import_files = QAction(icon_files, "&Import Files...", self)
        self.action_import_directory = QAction(icon_directory, '&Import Directory...', self)
        self.action_export_sicm_data = QAction(icon_export, 'Export sicm data', self)
        self.action_export_file = QAction(icon_export, 'Export view object', self)
        self.action_export_file.setEnabled(False)
        self.action_export_3d = QAction("3D graph", self)
        self.action_export_2d = QAction("2D graph", self)
        self.action_exit = QAction('&Exit', self)

        file_menu.addAction(self.action_clear)
        file_menu.addAction(self.action_remove_selection)
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
        self.action_show_graphs = QAction("Show plot windows", self)
        self.action_show_graphs.triggered.connect(self.show_graphs)

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
        self.view_menu.addAction(self.action_show_graphs)
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
        self.action_results = QAction("Results")
        self.action_results.setEnabled(False)
        self.action_line_profile_row = QAction("row")
        self.action_line_profile_row.setEnabled(False)
        self.action_line_profile_column = QAction("column")
        self.action_line_profile_column.setEnabled(False)
        self.action_line_profile_line = QAction("line")
        self.action_line_profile_line.setEnabled(False)
        self.action_line_profile_xy = QAction("xy")
        self.action_line_profile_column.setEnabled(False)
        self.action_measure_dist = QAction('&Measure distance', self)
        self.action_measure_dist.setEnabled(False)  # TODO
        action_measure_profile = QAction('&Measure profile', self)
        action_measure_profile.setEnabled(False)  # TODO
        self.action_set_rois = QAction("ROIs", self)
        self.action_set_roi = QAction("Set ROI", self)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(self.action_results)
        line_profile_menu = self.measure_menu.addMenu("Show line profile")
        line_profile_menu.addAction(self.action_line_profile_row)
        line_profile_menu.addAction(self.action_line_profile_column)
        line_profile_menu.addAction(self.action_line_profile_xy)
        line_profile_menu.addAction(self.action_line_profile_line)
        self.measure_menu.addAction(self.action_measure_dist)
        self.measure_menu.addAction(action_measure_profile)
        self.measure_menu.addAction(self.action_set_rois)
        self.measure_menu.addAction(self.action_set_roi)
        self.action_set_roi.setEnabled(False)
        self.action_set_rois.setEnabled(False)

        # About menu
        self.about_menu = menubar.addMenu("&About")
        self.about_menu.setEnabled(False)
        self.action_about = QAction('click test', self)

        #self.about_menu.addAction(self.action_about)

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

        self.action_show_dock_widgets = QAction(QIcon(join(self.resource_dir, "plot_widgets.png")), "Show plots")
        self.action_show_dock_widgets.triggered.connect(self.show_graphs)
        self.toolbar.addAction(self.action_show_dock_widgets)

        self.toolbar.addSeparator()
        self.addToolBar(self.toolbar)

        self.setGeometry(700, 350, 800, 800)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def set_wait_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))

    def set_default_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent) -> None:
        try:
            files = [url.toLocalFile() for url in e.mimeData().urls()]
            self.drop_event_function(files)
        except:
            print("DropEvent: no function called")

    def drop_event_function(self, files):
        """This is a placeholder function. You can reference it to any function which takes
        a list of urls as an argument. This function is called after a drop event in the main window."""
        pass

    def set_drop_event_function(self, func):
        """Sets a drop event function. func must take a list of strings
         as an argument."""
        self.drop_event_function = func

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
        """Shows the dock widgets containing the
        plot canvases."""
        if not self.dock_3d_plot.isVisible():
            self.dock_3d_plot.show()
        if not self.dock_2d_plot.isVisible():
            self.dock_2d_plot.show()

    def set_menus_enabled(self, enable):
        """"
        Sets the menu items enabled status.

        Add menus and menu items here which should be enabled
        or disabled when list selection changes.
        """
        self.view_menu.setEnabled(enable)
        self.data_menu.setEnabled(enable)
        self.measure_menu.setEnabled(enable)
        self.action_results.setEnabled(enable)
        self.about_menu.setEnabled(False)
        self.action_line_profile_row.setEnabled(enable)
        self.action_line_profile_column.setEnabled(enable)
        self.action_line_profile_line.setEnabled(enable)
        self.action_export_sicm_data.setEnabled(enable)
        self.action_measure_dist.setEnabled(enable)

    def toggle_show_toolbar(self):
        """Show or hide toolbar."""
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

    def update_info_labels(self,
                           scan_date,
                           scan_time,
                           scan_mode,
                           x_px,
                           y_px,
                           x_size,
                           y_size,
                           x_px_raw,
                           y_px_raw,
                           x_size_raw,
                           y_size_raw
                           ):
        text = f"<html>" \
               f"<table style='width:100%'>" \
               f"<tr>" \
               f"<td><b>Scan date:</b></td> <td>{scan_date}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>Scan time:</b></td> <td>{scan_time}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>Scan mode:</b></td> <td>{scan_mode}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>x pixels:</b></td> <td>{x_px}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>y pixels:</b></td> <td>{y_px}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>x size [µm]:</b></td> <td>{x_size}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>y size [µm]:</b></td> <td>{y_size}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>x pixels (raw):</b></td> <td>{x_px_raw}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>y pixels (raw):</b></td> <td>{y_px_raw}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>x size [µm] (raw):</b></td> <td>{x_size_raw}</td>" \
               f"</tr>" \
               f"<tr>" \
               f"<td><b>y size [µm] (raw):</b></td> <td>{y_size_raw}</td>" \
               f"</tr>" \
               f"</table>" \
               "</html>"
        self.info_text.clear()
        self.info_text.setHtml(text)
