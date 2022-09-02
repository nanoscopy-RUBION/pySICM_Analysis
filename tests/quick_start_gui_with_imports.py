import sys
from os import listdir
from os.path import join

from PyQt5.QtWidgets import QApplication

from pySICM_Analysis.gui_main import MainWindow
from pySICM_Analysis.main import Controller

if __name__ == "__main__":
    # setup application and gui
    app = QApplication(sys.argv)
    app.setApplicationName("pySICM TestSuite")
    window = MainWindow()
    controller = Controller(window)
    controller.add_canvases_to_main_window()
    controller.connect_actions()

    # import some sicm files
    dir = "/mnt/data/programmierung/sicm_test_data/"
    files = []
    for file in listdir(dir):
        if file.endswith(".sicm"):
            files.append(join(dir, file))
    controller.add_files_to_list(files)

    sys.exit(app.exec())
