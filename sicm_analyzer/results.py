from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QPlainTextEdit

from sicm_analyzer.sicm_data import SICMdata
from sicm_analyzer.measurements import get_roughness

class ResultsWindow(QWidget):
    """
    This window will show the results of a sicm data object.

    At the moment, it will only display roughness and some information
    about the polynomial fit used to calculate the roughness.
    """

    def __init__(self, controller, data: SICMdata, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Results")
        self.setFixedSize(500, 600)
        self.controller = controller
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(self.close)
        layout.addWidget(self.button_close)
        self.text.insertPlainText(self.get_results(data))

    def get_results(self, data: SICMdata):
        roughness, fit_result = get_roughness(data)
        text = ""
        text = text + "Fit Results:\n"
        text = text + str(fit_result)
        text = text + "\n\n"
        text = text + f"Roughness: {roughness}"
        return text

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()