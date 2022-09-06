from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, \
    QDialog, QDialogButtonBox


class SetROIsDialog(QDialog):
    """

    """

    def __init__(self, controller, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Set ROIs")
        self.setFixedSize(500, 500)
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
        buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

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


