
import os
from os.path import join
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QActionGroup, QKeyEvent, QDragEnterEvent, QDropEvent, QCursor

from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QLabel, QWidget, QVBoxLayout, QSplitter, QStyle, \
    QMainWindow, QToolBar, QAbstractItemView, QDockWidget, QTextEdit, QMenu

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
        self.icons_dir = join(self.resource_dir, "icons")
        self.close_window = pyqtSignal()
        self.central_widget = QtWidgets.QWidget(self)
        self.imported_files_list = QListWidget(self)
        # self.imported_files_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        # self.imported_files_list.setSortingEnabled(True)
        self.imported_files_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)

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
        self.action_remove_all = QAction(QIcon(join(self.icons_dir, "clear.png")), '&Remove all', self)
        self.action_remove_selection = QAction("Remove selection", self)
        self.action_remove_selection.setShortcut("Ctrl+D")
        self.action_copy_selection = QAction("Copy selected file", self)
        self.action_copy_checked = QAction("Copy checked files", self)
        self.action_rename_selection = QAction("Rename selected file", self)
        self.action_preferences = QAction("Preferences", self)
        self.action_import_files = QAction(icon_files, "&Import Files...", self)
        self.action_import_directory = QAction(icon_directory, '&Import Directory...', self)
        self.action_export_sicm_data = QAction(icon_export, 'Export sicm data', self)
        self.action_export_sicm_data_multi = QAction(icon_export, 'Export sicm data (multi)', self)
        self.action_export_file = QAction(icon_export, 'Export view object', self)
        self.action_export_file.setEnabled(False)
        self.action_export_approach_csv = QAction(icon_export, 'Export approach curve data (csv)', self)
        self.action_export_3d = QAction("3D graph", self)
        self.action_export_2d = QAction("2D graph", self)
        self.action_exit = QAction('&Exit', self)

        file_menu.addAction(self.action_remove_all)
        file_menu.addAction(self.action_remove_selection)
        file_menu.addAction(self.action_copy_selection)
        file_menu.addAction(self.action_copy_checked)
        file_menu.addAction(self.action_rename_selection)
        file_menu.addSeparator()
        file_menu.addAction(self.action_preferences)
        file_menu.addSeparator()
        open_sample_menu = file_menu.addMenu("Open sample")
        file_menu.addAction(self.action_import_files)
        file_menu.addAction(self.action_import_directory)
        clipboard_menu = file_menu.addMenu(icon_export, 'Export graph')
        clipboard_menu.addAction(self.action_export_3d)
        clipboard_menu.addAction(self.action_export_2d)
        file_menu.addAction(self.action_export_sicm_data)
        file_menu.addAction(self.action_export_sicm_data_multi)
        file_menu.addAction(self.action_export_file)
        file_menu.addAction(self.action_export_approach_csv)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        # Samples
        self.action_sample1 = QAction("Sample 1", self)
        open_sample_menu.addAction(self.action_sample1)
        self.action_sample2 = QAction("Sample 2", self)
        open_sample_menu.addAction(self.action_sample2)
        self.action_sample3 = QAction("Sample 3", self)
        open_sample_menu.addAction(self.action_sample3)
        self.action_sample4 = QAction("Sample 4", self)
        open_sample_menu.addAction(self.action_sample4)
        self.action_sample2.setEnabled(False)
        self.action_sample3.setEnabled(False)
        self.action_sample4.setEnabled(False)

        # Edit menu
        self.action_undo = QAction("Undo", self)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_redo = QAction("Redo", self)
        self.action_redo.setShortcut("Ctrl+R")
        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)

        action_sort_ascending = QAction(QIcon(join(self.icons_dir, "sort_ascending.svg")), "Sort (ascending)", self)
        action_sort_ascending.triggered.connect(lambda: self.__sort_list_items(Qt.SortOrder.AscendingOrder))
        action_sort_descending = QAction(QIcon(join(self.icons_dir, "sort_descending.svg")), "Sort (descending)", self)
        action_sort_descending.triggered.connect(lambda: self.__sort_list_items(Qt.SortOrder.DescendingOrder))

        action_check_all = QAction("Check all items", self)
        action_check_all.triggered.connect(self.check_all_items)
        action_uncheck_all = QAction("Uncheck all items", self)
        action_uncheck_all.triggered.connect(self.uncheck_all_items)

        self.action_toggle_toolbar = QAction("Show/Hide toolbar", self)
        self.action_toggle_toolbar.triggered.connect(self.toggle_show_toolbar)
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(action_check_all)
        edit_menu.addAction(action_uncheck_all)
        edit_menu.addSeparator()
        edit_menu.addAction(action_sort_ascending)
        edit_menu.addAction(action_sort_descending)
        edit_menu.addSeparator()
        edit_menu.addAction(self.action_toggle_toolbar)

        # View menu
        self.action_toggle_axes = QAction('&Show axes', self)
        self.action_toggle_axes.setCheckable(True)
        self.action_toggle_axes.setChecked(True)
        self.action_toggle_edge_lines = QAction('Hide lines', self)
        self.action_toggle_edge_lines.setCheckable(True)
        self.action_toggle_edge_lines.setChecked(True)
        self.action_view_restore = QAction('&Restore view', self)
        self.action_view_restore_all = QAction('&Restore view for all', self)
        self.action_view_ratio = QAction('Aspect ratio', self)
        self.action_set_z_limits = QAction("Set z limits", self)
        self.action_reset_z_limits = QAction("Reset z limits", self)
        action_view_surface = QAction('&Interpolate surface', self)
        action_view_surface.setEnabled(False)  # TODO
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_xlimits.setEnabled(False)  # TODO
        action_view_ylimits = QAction('&Adjust y limits', self)
        action_view_ylimits.setEnabled(False)  # TODO
        self.action_view_colormap = QAction('Colormap', self)
        self.action_store_angles = QAction('Store viewing angles', self)
        self.action_restore_angles = QAction('Restore default viewing angles', self)
        self.action_show_graphs = QAction("Show plot windows", self)
        self.action_show_graphs.triggered.connect(self.show_graphs)

        self.action_set_axis_labels_px = QAction("pixels", self)
        self.action_set_axis_labels_px.setCheckable(True)
        self.action_set_axis_labels_micron = QAction("µm", self)
        self.action_set_axis_labels_micron.setCheckable(True)

        self.action_set_z_axis_label_micron = QAction("µm", self)
        self.action_set_z_axis_label_micron.setCheckable(True)
        self.action_set_z_axis_label_nano = QAction("nm", self)
        self.action_set_z_axis_label_nano.setCheckable(True)

        self.action_apply_view_to_all = QAction("Apply view settings to all", self)
        self.action_apply_view_to_checked = QAction("Apply view settings to checked", self)

        self.view_menu = menubar.addMenu("&View")
        self.view_menu.addAction(self.action_toggle_axes)
        self.view_menu.addAction(self.action_toggle_edge_lines)
        axis_label_menu = self.view_menu.addMenu('Set axis labels to...')
        axis_label_menu.addAction(self.action_set_axis_labels_px)
        axis_label_menu.addAction(self.action_set_axis_labels_micron)

        z_axis_label_menu = self.view_menu.addMenu('Show z axis in...')
        z_axis_label_menu.setEnabled(False)
        z_axis_label_menu.addAction(self.action_set_z_axis_label_micron)
        z_axis_label_menu.addAction(self.action_set_z_axis_label_nano)

        action_group_axis_labels = QActionGroup(self)
        action_group_axis_labels.addAction(self.action_set_axis_labels_px)
        action_group_axis_labels.addAction(self.action_set_axis_labels_micron)
        action_group_axis_labels.setExclusive(True)
        self.action_set_axis_labels_px.setChecked(True)

        action_group_z_axis_label = QActionGroup(self)
        action_group_z_axis_label.addAction(self.action_set_z_axis_label_micron)
        action_group_z_axis_label.addAction(self.action_set_z_axis_label_nano)
        action_group_z_axis_label.setExclusive(True)
        self.action_set_z_axis_label_micron.setChecked(True)

        viewing_angles_menu = self.view_menu.addMenu("Viewing angles...")
        self.current_angles_label = QAction("Stored angles: Azim=-60.0, Elev=30.0")
        self.current_angles_label.setEnabled(False)
        viewing_angles_menu.addAction(self.current_angles_label)
        viewing_angles_menu.addAction(self.action_store_angles)
        viewing_angles_menu.addAction(self.action_restore_angles)

        self.view_menu.addAction(self.action_view_ratio)
        self.view_menu.addAction(self.action_set_z_limits)
        self.view_menu.addAction(self.action_reset_z_limits)
        self.view_menu.addAction(action_view_surface)
        self.view_menu.addAction(action_view_xlimits)
        self.view_menu.addAction(action_view_ylimits)
        self.view_menu.addAction(self.action_view_colormap)
        self.view_menu.addAction(self.action_show_graphs)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.action_apply_view_to_all)
        self.view_menu.addAction(self.action_apply_view_to_checked)
        self.view_menu.addAction(self.action_view_restore)
        self.view_menu.addAction(self.action_view_restore_all)

        # Manipulate data menu
        self.action_batch_mode = QAction("Batch mode (experimental version)", self)
        self.action_data_crop_tool = QAction('Crop...', self)
        self.action_data_crop_select = QAction('Select area...', self)
        self.action_data_minimum = QAction('Subtract minimum', self)
        self.action_data_threshold = QAction('Subtract threshold...', self)
        self.action_data_transpose_z = QAction('Transpose Z', self)
        self.action_data_invert_z = QAction("Invert z", self)
        self.action_data_filter = QAction("Filter data...", self)
        self.action_pick_outlier = QAction("Pick outlier", self)
        self.action_data_flip_x = QAction("X", self)
        self.action_data_flip_y = QAction("Y", self)
        self.action_data_level_plane = QAction('Plane', self)
        action_data_paraboloid = QAction('Paraboloid', self)
        action_data_paraboloid.setEnabled(False)  # TODO
        action_data_line = QAction('Linewise', self)
        action_data_line.setEnabled(False)  # TODO
        action_data_linemean = QAction('Linewise (mean)', self)
        action_data_linemean.setEnabled(False)  # TODO
        self.action_data_liney = QAction('Linewise Y', self)
        self.action_data_liney.setEnabled(False)  # TODO
        self.action_data_poly = QAction('polyXX (5th) symfit', self)
        self.action_data_poly_lmfit = QAction('polyXX (5th) lmfit', self)

        action_data_splines = QAction('by cubic splines', self)
        action_data_splines.setEnabled(False)  # TODO
        action_data_neighbor = QAction('by nearest neighbor', self)
        action_data_neighbor.setEnabled(False)  # TODO
        self.action_data_to_height_diff = QAction('Transform to height differences', self)
        self.action_data_reset = QAction('Reset data manipulations', self)

        self.data_menu = menubar.addMenu("&Manipulate data")
        self.data_menu.addAction(self.action_batch_mode)
        self.data_menu.addSeparator()
        self.data_menu.addAction(self.action_data_crop_tool)
        simple_menu = self.data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(self.action_data_minimum)
        simple_menu.addAction(self.action_data_transpose_z)
        simple_menu.addAction(self.action_data_invert_z)
        flip_menu = simple_menu.addMenu("Flip data")
        flip_menu.addAction(self.action_data_flip_x)
        flip_menu.addAction(self.action_data_flip_y)
        self.data_menu.addAction(self.action_data_threshold)
        self.data_menu.addAction(self.action_data_filter)
        self.data_menu.addAction(self.action_pick_outlier)
        flatten_menu = self.data_menu.addMenu('Leveling')
        flatten_menu.addAction(self.action_data_level_plane)
        flatten_menu.addAction(action_data_paraboloid)
        flatten_menu.addAction(action_data_line)
        flatten_menu.addAction(action_data_linemean)
        flatten_menu.addAction(self.action_data_liney)
        flatten_menu.addAction(self.action_data_poly)
        flatten_menu.addAction(self.action_data_poly_lmfit)
        interpolation_menu = self.data_menu.addMenu('Interpolation')
        interpolation_menu.addAction(action_data_splines)
        interpolation_menu.addAction(action_data_neighbor)
        self.data_menu.addAction(self.action_data_to_height_diff)
        self.data_menu.addSeparator()
        self.data_menu.addAction(self.action_data_reset)

        # Measurements menu
        self.action_results = QAction("Results (selected file)")
        self.action_results.setEnabled(False)
        self.action_measure_roughness_batch = QAction("Results (checked files)", self)
        self.action_results_custom = QAction("Results (custom configuration)")
        # TODO address when feature becomes enabled vs disabled
        self.action_line_profile_row = QAction("row")
        self.action_line_profile_row.setEnabled(False)
        self.action_line_profile_column = QAction("column")
        self.action_line_profile_column.setEnabled(False)
        self.action_line_profile_line = QAction("line")
        self.action_line_profile_line.setEnabled(False)
        self.action_line_profile_xy = QAction("xy")
        self.action_line_profile_column.setEnabled(False)
        self.action_get_pixel_values = QAction("Get pixel values", self)
        self.action_measure_dist = QAction('&Measure distance', self)
        self.action_measure_dist.setEnabled(False)  # TODO

        action_measure_profile = QAction('&Measure profile', self)
        action_measure_profile.setEnabled(False)  # TODO
        self.action_set_rois = QAction("ROIs", self)
        self.action_set_roi = QAction("Set ROI", self)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(self.action_results)
        self.measure_menu.addAction(self.action_measure_roughness_batch)
        self.measure_menu.addAction(self.action_results_custom)
        self.measure_menu.addSeparator()
        self.action_height_profile_tool = QAction("Height profile tool...", self)
        self.measure_menu.addAction(self.action_height_profile_tool)
        self.measure_menu.addAction(self.action_get_pixel_values)
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
        self.escape_key = None

        # Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.action_import_files)
        self.toolbar.addAction(self.action_import_directory)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_remove_all)
        self.toolbar.addAction(action_sort_ascending)
        self.toolbar.addAction(action_sort_descending)
        self.toolbar.addSeparator()
        self.action_show_dock_widgets = QAction(QIcon(join(self.icons_dir, "plot_widgets.png")), "Show plots")
        self.action_show_dock_widgets.triggered.connect(self.show_graphs)
        self.toolbar.addAction(self.action_show_dock_widgets)

        self.toolbar.addSeparator()
        self.addToolBar(self.toolbar)

        # context menu
        self.context_menu = QMenu(self)
        self.context_menu.addAction(self.action_copy_selection)
        self.context_menu.addAction(self.action_rename_selection)
        self.context_menu.addAction(self.action_remove_selection)
        self.context_menu.addAction(self.action_data_reset)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.action_undo)
        self.context_menu.addAction(self.action_redo)

        self.imported_files_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.imported_files_list.customContextMenuRequested.connect(self.show_context_menu)

        self.setGeometry(700, 350, 800, 800)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def show_context_menu(self, point):
        self.context_menu.exec(self.imported_files_list.mapToGlobal(point))

    def set_wait_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))

    def set_cross_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))

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
        Key_Escape
        """
        if event.type() is QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Delete:
                try:
                    self.delete_key()
                except:
                    pass
            if event.key() == Qt.Key.Key_Escape:
                try:
                    self.escape_key()
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
        self.action_data_poly_lmfit.setEnabled(enable)

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

    def update_viewing_angles_label(self, azim: float, elev: float):
        a = str(round(azim, 1))
        e = str(round(elev, 1))
        self.current_angles_label.setText(f"Stored angles: Azim={a}, Elev={e}")

    def add_items_to_list(self, items: list[str]):
        """Adds a list item for each filename in the list."""
        for item in items:
            self.add_item_to_list(item)

    def add_item_to_list(self, item):
        checkable_item = self._get_checkable_item(item)
        self.imported_files_list.addItem(checkable_item)

    def _get_checkable_item(self, item):
        """Create and return a list item which has a checkbox."""
        checkable_item = QtWidgets.QListWidgetItem(item)
        checkable_item.setFlags(
            Qt.ItemFlag.ItemIsUserCheckable
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsDragEnabled
        )
        checkable_item.setCheckState(Qt.CheckState.Checked)
        return checkable_item

    def __sort_list_items(self, order: Qt.SortOrder):
        """Reorders list items according to the order parameter."""
        self.imported_files_list.sortItems(order)

    def insert_item_after_current_selection(self, item):
        """Insert an item right below the currently selected item."""
        checkable_item = self._get_checkable_item(item)
        pos = self.imported_files_list.currentRow() + 1
        self.imported_files_list.insertItem(pos, checkable_item)

    def change_item_name(self, new_name):
        """Set a new name for the selected item."""
        item = self.imported_files_list.selectedItems()[0]
        item.setText(new_name)

    def get_all_checked_items(self) -> list[str]:
        items = []
        for i in range(self.imported_files_list.count()):
            if self.imported_files_list.item(i).checkState() == Qt.CheckState.Checked:
                items.append(self.imported_files_list.item(i).text())
        return items

    def check_all_items(self):
        """Sets the check state of all items in the imported files list to checked."""
        self._change_checkstate_of_all_items(Qt.CheckState.Checked)

    def uncheck_all_items(self):
        """Sets the check state of all items in the imported files list to checked."""
        self._change_checkstate_of_all_items(Qt.CheckState.Unchecked)

    def _change_checkstate_of_all_items(self, state: Qt.CheckState):
        """Sets the check state of all items in the imported files list."""
        for i in range(self.imported_files_list.count()):
            self.imported_files_list.item(i).setCheckState(state)

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

    def update_info_text(self,
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
                         y_size_raw,
                         previous_manipulations: list[str]
                         ):
        manipulations = "<ul style=\"list-style-type:circle;\">"
        if previous_manipulations:
            for manipulation in previous_manipulations:
                manipulations = manipulations + "<li>" + manipulation + "</li>"
            manipulations = manipulations + "</ul>"
        else:
            manipulations = "none"

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
               f"<tr><td colspan='2'><hr/></td></tr>" \
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
               f"<tr><td colspan='2'><hr/></td></tr>" \
               f"<tr>" \
               f"<td><b>Previous manipulations:</b></td> <td>{manipulations}</td>" \
               f"</tr>" \
               f"</table>" \
               "</html>"
        self.info_text.clear()
        self.info_text.setHtml(text)

    def clear_info_text(self):
        self.info_text.clear()
