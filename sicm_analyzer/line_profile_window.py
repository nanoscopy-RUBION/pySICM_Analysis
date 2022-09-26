from PyQt6.QtWidgets import QWidget


class LineProfileWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Enter Range for Crop")

