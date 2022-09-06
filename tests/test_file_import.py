from os import listdir
from os.path import join
import sys
from unittest import TestCase
import os
from PyQt6.QtWidgets import QApplication

from sicm_analyzer.gui_main import MainWindow
from sicm_analyzer.main import Controller

app = QApplication(sys.argv)


def get_filenames():
    APP_PATH = os.getcwd()
    SAMPLE_FILES_DIR = join(APP_PATH, "tests", "sample_sicm_files")
    files = []
    for file in listdir(SAMPLE_FILES_DIR):
        if file.endswith(".sicm"):
            files.append(join(SAMPLE_FILES_DIR, file))
    return files


class PlotTests(TestCase):

    def setUp(self):
        app.setApplicationName("pySICM TestSuite")
        window = MainWindow()
        self.controller = Controller(window)
        self.controller.add_canvases_to_main_window()
        self.controller.connect_actions()

    def test_file_import(self):
        self.controller.add_files_to_list(get_filenames())
        self.assertEqual(self.controller.main_window.imported_files_list.count(), 11)


class GuiInteractionTests(TestCase):

    def setUp(self):
        app.setApplicationName("pySICM TestSuite")
        window = MainWindow()
        self.controller = Controller(window)
        self.controller.add_canvases_to_main_window()
        self.controller.connect_actions()
        self.controller.add_files_to_list(get_filenames())

    def test_switch_from_px_to_micron_and_back(self):

        print("bla")