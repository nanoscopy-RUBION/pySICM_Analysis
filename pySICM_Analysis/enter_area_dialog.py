from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, QPushButton, \
    QDialog, QDialogButtonBox


class EnterAreaDialog(QDialog):
    """
    This widget will appear as a free-floating window if
    it has no parent.
    """

    def __init__(self, controller, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Enter Range for Crop")
        self.setFixedSize(300, 200)
        self.controller = controller

        central_layout = QVBoxLayout()
        self.setLayout(central_layout)

        row1 = QWidget()
        row1_layout = QHBoxLayout()
        row1.setLayout(row1_layout)
        label_x1 = QLabel("x1:")
        self.edit_x1 = QLineEdit()
        label_y1 = QLabel("y1:")
        self.edit_y1 = QLineEdit()
        row1_layout.addWidget(label_x1)
        row1_layout.addWidget(self.edit_x1)
        row1_layout.addWidget(label_y1)
        row1_layout.addWidget(self.edit_y1)

        central_layout.addWidget(row1)

        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        label_x2 = QLabel("x2:")
        self.edit_x2 = QLineEdit()
        label_y2 = QLabel("y2:")
        self.edit_y2 = QLineEdit()
        row2_layout.addWidget(label_x2)
        row2_layout.addWidget(self.edit_x2)
        row2_layout.addWidget(label_y2)
        row2_layout.addWidget(self.edit_y2)

        central_layout.addWidget(row2)

        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.addButton(QDialogButtonBox.Cancel)

        central_layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

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
        try:
            x1 = int(self.edit_x1.text().strip())
            y1 = int(self.edit_y1.text().strip())
            x2 = int(self.edit_x2.text().strip())
            y2 = int(self.edit_y2.text().strip())
            point1 = QPoint(x1, y1)
            point2 = QPoint(x2, y2)
        except ValueError:
            point1 = QPoint()
            point2 = QPoint()
        return point1, point2

