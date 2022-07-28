import PyQt5 as pqt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

'''app = QApplication([])
button = QPushButton('Click')
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()

button.clicked.connect(on_button_clicked)
button.show()
app.exec()'''

import sys

"""
TODO add documentation
"""


import matplotlib

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QListWidget
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')
TITLE = "pySICM Viewer (2022_05_20_1)"


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data."""
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QWidget(self)
        self.list_widget = QListWidget(self)
        self.canvas = GraphCanvas()
        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()

        #self.list_widget.currentItemChanged.connect(self.item_changed_event)

        action_exit = QtWidgets.QAction(QIcon('exit.png'), '&Exit', self)
        action_exit.triggered.connect(QtWidgets.qApp.quit)
        action_import = QtWidgets.QAction(QIcon('open.png'), '&Import', self)
        action_import.triggered.connect(self.menu_action_import)
        action_clear = QtWidgets.QAction('&Clear', self)
        #action_clear.triggered.connect(self.menu_action_clear)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(action_clear)
        file_menu.addAction(action_import)
        file_menu.addAction(action_exit)

        layout.addWidget(self.list_widget, 2)
        layout.addWidget(self.canvas, 3)
        self.central_widget.setLayout(layout)


        action_exit = QAction(QIcon('exit.png'), '&Exit', self)
        #action_exit.triggered.connect(qApp.quit)
        action_import = QAction(QIcon('open.png'), '&Import', self)
        #action_import.triggered.connect(self.menu_action_import)
        action_clear = QAction('&Clear', self)
        #action_clear.triggered.connect(self.menu_action_clear)

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(action_clear)
        file_menu.addAction(action_import)
        file_menu.addAction(action_exit)

        action_import_single = QAction('&Import Single File', self)
        #action_import_single.triggered.connect(self.menu_action_import_single)
        action_import_multiple = QAction('&Import Multiple Files', self)
        #action_import_multiple.triggered.connect(self.menu_action_import_multiple)

        import_menu = menubar.addMenu("&Import")
        import_menu.addAction(action_import_single)
        import_menu.addAction(action_import_multiple)

        action_export_file = QAction('&To file', self)
        #action_export_file.triggered.connect(self.menu_action_export_file)
        action_export_bitmap = QAction('&As bitmap (png)', self)
        #action_export_bitmap.triggered.connect(self.menu_action_export_bitmap)
        action_export_vector = QAction('&as vector (pdf)', self)
        #action_export_vector.triggered.connect(self.menu_action_export_vector)

        export_menu = menubar.addMenu("&Export")
        clipboard_menu = export_menu.addMenu('To clipboard')
        clipboard_menu.addAction(action_export_bitmap)
        clipboard_menu.addAction(action_export_vector)
        export_menu.addAction(action_export_file)

        action_plot_rotate = QAction('&Rotate', self) #TODO implement as checkbox
        #action_plot_rotate.triggered.connect(self.menu_action_plot_rotate)
        action_plot_pan = QAction('&Pan', self)
        #action_plot_pan.triggered.connect(self.menu_action_plot_pan)
        action_plot_zoom = QAction('&Zoom', self)
        #action_plot_zoom.triggered.connect(self.menu_action_plot_zoom)

        plot_menu = menubar.addMenu("&Plot interaction")
        plot_menu.addAction(action_plot_rotate)
        plot_menu.addAction(action_plot_pan)
        plot_menu.addAction(action_plot_zoom)

        action_view_content = QAction('&Hide axis content', self)
        #action_view_content.triggered.connect(self.menu_action_view_content)
        action_view_axes = QAction('&Hide axes when updated', self)
        #action_view_axes.triggered.connect(self.menu_action_view_axes)
        action_view_restore = QAction('&Restore view', self)
        #action_view_restore.triggered.connect(self.menu_action_view_restore)
        action_view_mode = QAction('&Mode', self)
        #action_view_mode.triggered.connect(self.menu_action_view_mode)
        action_view_ratio = QAction('&Aspect ratio', self)
        #action_view_ratio.triggered.connect(self.menu_action_view_ratio)
        action_view_surface = QAction('&Interpolate surface', self)
        #action_view_surface.triggered.connect(self.menu_action_view_surface)
        action_view_limits = QAction('&Adjust limits', self)
        #action_view_limits.triggered.connect(self.menu_action_view_limits)
        action_view_colormap = QAction('&Colormap', self)
        #action_view_colormap.triggered.connect(self.menu_action_view_colormap)

        view_menu = menubar.addMenu("&View")
        view_menu.addAction(action_view_content)
        view_menu.addAction(action_view_axes)
        view_menu.addAction(action_view_restore)
        view_menu.addAction(action_view_mode)
        view_menu.addAction(action_view_ratio)
        view_menu.addAction(action_view_surface)
        view_menu.addAction(action_view_limits)
        view_menu.addAction(action_view_colormap)

        action_data_simple = QAction('&Simple manipulations', self)
        #action_data_simple.triggered.connect(self.menu_action_data_simple)
        action_data_filter = QAction('&Filter', self)
        #action_data_filter.triggered.connect(self.menu_action_data_filter)
        action_data_flatten = QAction('&Flatten', self)
        #action_data_flatten.triggered.connect(self.menu_action_data_flatten)
        action_data_interpolation = QAction('&Interpolation', self)
        #action_data_interpolation.triggered.connect(self.menu_action_data_interpolation)

        data_menu = menubar.addMenu("&Manipulate data")
        data_menu.addAction(action_data_simple)
        data_menu.addAction(action_data_filter)
        data_menu.addAction(action_data_flatten)
        data_menu.addAction(action_data_interpolation)

        action_measure_dist = QAction('&Measure distance', self)
        #action_measure_dist.triggered.connect(self.menu_action_measure_dist)
        action_measure_profile = QAction('&Measure profile', self)
        #action_measure_profile.triggered.connect(self.menu_action_measure_profile)

        measure_menu = menubar.addMenu("&Measurements")
        measure_menu.addAction(action_measure_dist)
        measure_menu.addAction(action_measure_profile)

        properties_menu = menubar.addMenu("&Properties")

        about_menu = menubar.addMenu("&About")

        self.setGeometry(700, 350, 800, 800)
        self.setWindowTitle('Submenu')
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def import_files_dialog(self):
        """Opens a file dialog to choose .sicm files."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filenames, _ = QFileDialog.getOpenFileNames(self,
                                                    "Import pySICM Scan Files",  # title
                                                    "..",  # path
                                                    "pySICM Files (*.sicm)",  # file formats
                                                    options=options
                                                    )
        return filenames

    #def add_files_to_list(self, files):
        #"""TODO add doc string"""
        #self.list_widget.addItems(files)
        #if len(files) > 1:
            #message_end = " files."
        #else:
            #message_end = " file."
        #self.statusBar().showMessage("Imported " + str(len(files)) + message_end)

    def menu_action_import(self):
        """TODO add doc string"""
        files = self.import_files_dialog()
        if files:
            self.add_files_to_list(files)
        else:
            self.statusBar().showMessage("No files imported.")

    #def menu_action_clear(self):
        #"""Removes all items from list widget."""
        #self.list_widget.clear()
        #self.statusBar().showMessage("Files removed from the list.")

#class Example(QMainWindow):

    #def __init__(self):
        #super().__init__()

        #self.initUI()

    #def initUI(self):

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')

        #impMenu = QMenu('Import', self)
        #impAct = QAction('Import mail', self)
        #impMenu.addAction(impAct)

        #newAct = QAction('New', self)

        #fileMenu.addAction(newAct)
        #fileMenu.addMenu(impMenu)

app = QApplication(sys.argv)
windows = MainWindow()
sys.exit(app.exec())
