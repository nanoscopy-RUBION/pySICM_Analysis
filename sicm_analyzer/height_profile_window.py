import csv
import numpy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolBar,  QSplitter
from PyQt6.QtGui import QAction, QCursor, QIcon, QKeyEvent
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sicm_analyzer.graph_canvas import GraphCanvas
from sicm_analyzer.mouse_events import ROW, COLUMN, CROSS
from sicm_analyzer.sicm_data import ScanBackstepMode
from sicm_analyzer.graph_canvas import RASTER_IMAGE
from skimage import measure
import numpy as np
from os.path import join
import os

from sicm_analyzer.view import View


class HeightProfileWindow(QWidget):
    """A small window for displaying height profiles.

    The canvas is an instance of GraphCanvas and thus
    supports all functionality of that class, i.e. mouse
    interactions with the graph.
    """

    def __init__(self, data: ScanBackstepMode, parent: QWidget = None, view=None):
        # to have a separate window set parent to None
        super(HeightProfileWindow, self).__init__(parent=None)

        self.data = data
        self.parent = parent
        self.view: View = view
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.x_is_row = True

        self.parent = parent

        # icons for toolbar
        self.resource_dir = join(os.getcwd(), "resources")
        self.icons_dir = join(self.resource_dir, "icons")
        icon_export = QIcon(join(self.icons_dir, "line_profile_export.svg"))
        icon_row = QIcon(join(self.icons_dir, "line_profile_row.svg"))
        icon_column = QIcon(join(self.icons_dir, "line_profile_column.svg"))
        icon_cross = QIcon(join(self.icons_dir, "line_profile_cross.svg"))
        icon_custom = QIcon(join(self.icons_dir, "line_profile_custom.svg"))

        # toolbar
        self.toolbar = QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("QToolBar {border-bottom: 1px solid #D3D3D3;}")

        # graphs
        self.canvas_data = GraphCanvas()
        self.canvas_data.draw_graph(data, RASTER_IMAGE, self.view)
        self.canvas_lines = GraphCanvas()
        graphs = QSplitter(Qt.Orientation.Horizontal)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setMenuBar(self.toolbar)
        graphs.addWidget(self.canvas_data)
        graphs.addWidget(self.canvas_lines)
        layout.addWidget(graphs)

        # Toolbar actions
        self.action_export = QAction(icon_export, "Export as csv", self)
        self.action_export.triggered.connect(self.export_as_csv)

        self.action_line_row = QAction(icon_row, "row mode", self)
        self.action_line_row.triggered.connect(self.select_line_profile_row)

        self.action_line_column = QAction(icon_column, "column mode", self)
        self.action_line_column.triggered.connect(self.select_line_profile_column)

        self.action_line_custom = QAction(icon_custom, "custom mode", self)
        self.action_line_custom.triggered.connect(self.select_line_profile_line)

        self.action_line_cross = QAction(icon_cross, "cross mode", self)
        self.action_line_cross.triggered.connect(self.show_xy_profile)

        self.toolbar.addAction(self.action_export)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_line_row)
        self.toolbar.addAction(self.action_line_column)
        self.toolbar.addAction(self.action_line_custom)
        self.toolbar.addAction(self.action_line_cross)
        self.toolbar.addSeparator()

    # override
    def keyPressEvent(self, event):
        """
        """
        if event.key() == Qt.Key.Key_Escape:
            try:
                self.canvas_data.unbind_mouse_events()
                self.set_default_cursor()
                self.canvas_data.redraw_graph()
            except:
                pass

    def set_cross_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))

    def set_default_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def export_as_csv(self):
        """Exports x and y data as csv file.

        For convenience .csv extension is added
        to the file name.
        """
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self,
                                                caption="Export height profile data as csv file",
                                                filter="All files (*.*);;CSV (*.csv)",
                                                # directory=DEFAULT_FILE_PATH,
                                                initialFilter="CSV (*.csv)",
                                                options=options
                                                )
        if file_path[0]:
            if file_path[0].lower().endswith(".csv"):
                file_path = file_path[0]
            else:
                file_path = file_path[0] + ".csv"

            with open(file_path, "w", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                for i in range(len(self.x1)):
                    writer.writerow([self.x1[i], self.y1[i]])

    def update_plot(self, x: numpy.ndarray, y: numpy.ndarray):
        if self.view.show_as_px:
            self.x1 = x.tolist()
        else:
            if self.x_is_row:
                self.x1 = [value * self.data.micron_to_pixel_factor_x() for value in x]
            else:
                self.x1 = [value * self.data.micron_to_pixel_factor_y() for value in x]
        self.y1 = y.tolist()
        self.canvas_lines.draw_line_plot(x, y, self.data, self.view)

    def update_xy_line_profile_plot(self, x_x, x_y, y_x, y_y):
        if self.view.show_as_px:
            self.x1 = x_x.tolist()
            self.x2 = y_x.tolist()
        else:
            self.x1 = [value * self.data.micron_to_pixel_factor_x() for value in x_x]
            self.x2 = [value * self.data.micron_to_pixel_factor_y() for value in y_x]

        self.y1 = x_y.tolist()
        self.y2 = y_y.tolist()
        self.canvas_lines.draw_xy_line_profiles(x_x, x_y, y_x, y_y, self.data, self.view)

    def _focus_line_profile_widget(self):
        self.set_default_cursor()

    def _show_line_profile(self, selection_mode: str, index: int = -1):
        if index >= 0:
            data = self.data
            shape = data.z.shape
            if selection_mode == ROW and index <= shape[0]:
                x = data.x
                z = data.z
                self.update_plot(x[index, :], z[index, :])
            if selection_mode == COLUMN and index <= shape[1]:
                y = data.y
                z = data.z
                self.update_plot(y[:, index], z[:, index])

    def _show_line_profile_of_drawn_line(self, x_data: (int, int) = (-1, -1), y_data: (int, int) = (-1, -1)):
        try:
            src = (y_data[0], x_data[0])
            dst = (y_data[1], x_data[1])
            plot = measure.profile_line(image=self.data.z, src=src, dst=dst, linewidth=1, reduce_func=None)
            a = range(plot.shape[0])
            if self.view.show_as_px:
                x = np.array(a)
            else:
                x = np.array(a) * self.data.micron_to_pixel_factor_x()

            self.update_plot(x=x, y=plot)
        except Exception as e:
            print(e)

    def _show_xy_line_profiles(self, y_index: int = -1, x_index: int = -1):
        shape = self.data.z.shape
        if 0 <= x_index <= shape[0] and 0 <= y_index <= shape[1]:
            x = self.data.x
            y = self.data.y
            z = self.data.z
            self.update_xy_line_profile_plot(x[x_index, :], z[x_index, :], y[:, y_index], z[:, y_index])

    def select_line_profile_row(self):
        """Selection mode is row.
        """
        self.set_cross_cursor()
        self.x_is_row = True
        self.canvas_data.bind_mouse_events_for_showing_line_profile(
            data=self.data,
            view=self.view,
            func=self._show_line_profile,
            clean_up_func=self._focus_line_profile_widget,
            mode=ROW
        )

    def select_line_profile_column(self):
        """Selection mode is column.
        """
        self.set_cross_cursor()
        self.x_is_row = False
        self.canvas_data.bind_mouse_events_for_showing_line_profile(
            data=self.data,
            view=self.view,
            func=self._show_line_profile,
            clean_up_func=self._focus_line_profile_widget,
            mode=COLUMN
        )

    def select_line_profile_line(self):
        """Selection mode is custom line."""
        self.set_cross_cursor()
        self.x_is_row = True
        self.canvas_data.bind_mouse_events_for_draw_line(
            data=self.data,
            view=self.view,
            func=self._show_line_profile_of_drawn_line,
            clean_up_func=self._focus_line_profile_widget,
        )

    def show_xy_profile(self):
        """Show a window displaying a line plot which is
        updated on mouse movement over the 2D canvas.
        """
        self.set_cross_cursor()
        self.x_is_row = True
        self.canvas_data.bind_mouse_events_for_showing_line_profile(
            data=self.data,
            view=self.view,
            func=self._show_xy_line_profiles,
            clean_up_func=self._focus_line_profile_widget,
            mode=CROSS
        )
