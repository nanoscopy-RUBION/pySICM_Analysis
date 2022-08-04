from PyQt5.QtWidgets import QApplication
from viewer_gui import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = MainWindow()
    sys.exit(app.exec())