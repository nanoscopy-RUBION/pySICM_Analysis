from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, \
    QDialog, QDialogButtonBox, QPushButton
from PyQt6.QtGui import QIntValidator, QCursor
from sicm_analyzer.graph_canvas import GraphCanvas, RASTER_IMAGE


class CropToolWindow(QDialog):
    """
    This widget will appear as a free-floating window if
    it has no parent.
    """
    red_font = "QLineEdit {color: red;}"
    black_font = "QLineEdit {color: black;}"

    def __init__(self, controller, z_shape, data, view=None, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Crop Tool")
        #self.setFixedSize(700, 250)
        self.controller = controller
        self.max_x = z_shape[1] - 1
        self.max_y = z_shape[0] - 1
        self.data = data
        self.view = view

        main_layout = QHBoxLayout()
        self.figure_canvas_2d = GraphCanvas()
        self.figure_canvas_2d.draw_graph(self.data, RASTER_IMAGE, self.view)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setLayout(main_layout)
        label = QLabel(
            "Please enter coordinates for two points.\n"
            "Note: Indexing begins at 0. Maximum \n"
            f"values are {self.max_x} for X and {self.max_y} for Y.")
        central_layout.addWidget(label)

        row1 = QWidget()
        row1_layout = QHBoxLayout()
        row1.setLayout(row1_layout)
        label_p1 = QLabel("P1:")
        label_x1 = QLabel("x")
        self.edit_x1 = QLineEdit("0")
        self.edit_x1.setValidator(QIntValidator(0, self.max_x))
        self.edit_x1.setMaximumWidth(50)
        label_y1 = QLabel("y")
        self.edit_y1 = QLineEdit("0")
        self.edit_y1.setValidator(QIntValidator(0, self.max_y))
        self.edit_y1.setMaximumWidth(50)
        row1_layout.addWidget(label_p1)
        row1_layout.addSpacing(30)
        row1_layout.addWidget(label_x1)
        row1_layout.addWidget(self.edit_x1)
        row1_layout.addWidget(label_y1)
        row1_layout.addWidget(self.edit_y1)
        row1_layout.addStretch()
        central_layout.addWidget(row1)

        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        label_p2 = QLabel("P2:")
        label_x2 = QLabel("x")
        self.edit_x2 = QLineEdit("0")
        self.edit_x2.setValidator(QIntValidator(0, self.max_x))
        self.edit_x2.setMaximumWidth(50)
        label_y2 = QLabel("y")
        self.edit_y2 = QLineEdit("0")
        self.edit_y2.setValidator(QIntValidator(0, self.max_y))
        self.edit_y2.setMaximumWidth(50)
        row2_layout.addWidget(label_p2)
        row2_layout.addSpacing(30)
        row2_layout.addWidget(label_x2)
        row2_layout.addWidget(self.edit_x2)
        row2_layout.addWidget(label_y2)
        row2_layout.addWidget(self.edit_y2)
        row2_layout.addStretch()
        central_layout.addWidget(row2)

        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        self.crop_tool = QPushButton("Crop")
        self.crop_tool.setFixedSize(40, 40)
        self.crop_tool.clicked.connect(self.activate_tool)
        central_layout.addWidget(self.crop_tool)

        central_layout.addStretch()
        central_layout.addWidget(buttons)

        main_layout.addWidget(central_widget)
        main_layout.addWidget(self.figure_canvas_2d)

        self._bind_on_change_events()
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def set_cross_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))

    def set_default_cursor(self):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()

    def get_input_as_points(self):
        """Returns input as two QPoint objects.

        In case of invalid input both QPoint objects will have
        the coordinates (0, 0)."""
        # try:
        #     x1 = int(self.edit_x1.text().strip() or "0")
        #     y1 = int(self.edit_y1.text().strip() or "0")
        #     x2 = int(self.edit_x2.text().strip() or "0")
        #     y2 = int(self.edit_y2.text().strip() or "0")
        #     point1 = QPoint(x1, y1)
        #     point2 = QPoint(x2, y2)
        #
        #     if point1.x() <= point2.x():
        #         point2 = point2 + QPoint(1, 0)
        #     else:
        #         point1 = point1 + QPoint(1, 0)
        #     if point1.y() <= point2.y():
        #         point2 = point2 + QPoint(0, 1)
        #     else:
        #         point1 = point1 + QPoint(0, 1)
        # except ValueError:
        #     point1 = QPoint()
        #     point2 = QPoint()
        try:
            x1 = int(self.edit_x1.text().strip() or "0")
            y1 = int(self.edit_y1.text().strip() or "0")
            x2 = int(self.edit_x2.text().strip() or "0")
            y2 = int(self.edit_y2.text().strip() or "0")

            if x1 <= x2:
                x2 = x2 + 1
            else:
                x1 = x1 + 1
            if y1 <= y2:
                y2 = y2 + 1
            else:
                y1 = y1 + 1

            point1 = (x1, y1)
            point2 = (x2, y2)
        except ValueError:
            point1 = (0, 0)
            point2 = (0, 0)
        return point1, point2

    def activate_tool(self):
        self.set_cross_cursor()
        self.figure_canvas_2d.draw_rectangle_on_raster_image(
            data=self.data,
            view=self.view,
            func=self.update_input,
            clean_up_func=self.set_default_cursor
        )

    def _bind_on_change_events(self):
        self.edit_x1.textChanged.connect(self._update_preview)
        self.edit_y1.textChanged.connect(self._update_preview)
        self.edit_x2.textChanged.connect(self._update_preview)
        self.edit_y2.textChanged.connect(self._update_preview)

    def _unbind_on_change_events(self):
        self.edit_x1.textChanged.disconnect(self._update_preview)
        self.edit_y1.textChanged.disconnect(self._update_preview)
        self.edit_x2.textChanged.disconnect(self._update_preview)
        self.edit_y2.textChanged.disconnect(self._update_preview)

    def update_input(self, point1: QPoint, point2: QPoint):
        self._unbind_on_change_events()
        self.edit_x1.setText(str(point1.x()))
        self.edit_y1.setText(str(point1.y()))
        self.edit_x2.setText(str(point2.x()))
        self.edit_y2.setText(str(point2.y()))
        self._bind_on_change_events()

    def _update_preview(self):
        point1, point2 = self.get_input_as_points()
        width = abs(point1.x() - point2.x())
        height = abs(point1.y() - point2.y())

        if point1.x() < point2.x():
            orig_x = point1.x()
        else:
            orig_x = point2.x()
        if point1.y() < point2.y():
            orig_y = point1.y()
        else:
            orig_y = point2.y()

        rect = self.figure_canvas_2d.get_rectangle((orig_x, orig_y), width=width, height=height)
        self.figure_canvas_2d.add_rectangle_to_raster_image(rectangles=[rect, ])
