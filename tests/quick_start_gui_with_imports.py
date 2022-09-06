import sys
import os
from os import listdir
from os.path import join

from PyQt6.QtWidgets import QApplication

from sicm_analyzer.gui_main import MainWindow
from sicm_analyzer.main import Controller

APP_PATH = os.getcwd()
SAMPLE_FILES_DIR = join(APP_PATH, "tests", "sample_sicm_files")

if __name__ == "__main__":
    # setup application and gui
    app = QApplication(sys.argv)
    app.setApplicationName("pySICM TestSuite")
    window = MainWindow()
    controller = Controller(window)
    controller.add_canvases_to_main_window()
    controller.connect_actions()

    # import some sicm files
    files = []
    for file in listdir(SAMPLE_FILES_DIR):
        if file.endswith(".sicm"):
            files.append(join(SAMPLE_FILES_DIR, file))
    controller.add_files_to_list(files)

    sys.exit(app.exec())
