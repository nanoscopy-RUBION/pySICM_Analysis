"""
TODO add documentation
"""


import matplotlib
from sicmViewer import SICMDataFactory, ApproachCurve, ScanBackstepMode

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

        self.list_widget.currentItemChanged.connect(self.item_changed_event)

        action_exit = QtWidgets.QAction(QIcon('exit.png'), '&Exit', self)
        action_exit.triggered.connect(QtWidgets.qApp.quit)
        action_import = QtWidgets.QAction(QIcon('open.png'), '&Import', self)
        action_import.triggered.connect(self.menu_action_import)
        action_clear = QtWidgets.QAction('&Clear', self)
        action_clear.triggered.connect(self.menu_action_clear)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(action_clear)
        file_menu.addAction(action_import)
        file_menu.addAction(action_exit)

        layout.addWidget(self.list_widget, 2)
        layout.addWidget(self.canvas, 3)
        self.central_widget.setLayout(layout)

        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle(TITLE)
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

    def add_files_to_list(self, files):
        """TODO add doc string"""
        self.list_widget.addItems(files)
        if len(files) > 1:
            message_end = " files."
        else:
            message_end = " file."
        self.statusBar().showMessage("Imported " + str(len(files)) + message_end)

    def menu_action_import(self):
        """TODO add doc string"""
        files = self.import_files_dialog()
        if files:
            self.add_files_to_list(files)
        else:
            self.statusBar().showMessage("No files imported.")

    def menu_action_clear(self):
        """Removes all items from list widget."""
        self.list_widget.clear()
        self.statusBar().showMessage("Files removed from the list.")

    def item_changed_event(self, item):
        """Updates the figure canvas when list selection has changed.
        """
        self.canvas.figure.clear()
        if item:
            self.canvas.axes.set_title(item.text())
            sicm_data = SICMDataFactory().get_sicm_data(item.text())
            if isinstance(sicm_data, ScanBackstepMode):
                self.canvas.axes = self.canvas.figure.add_subplot(2,1,1, projection='3d')
                self.canvas.axes.plot_surface(*sicm_data.plot(), cmap=matplotlib.cm.YlGnBu_r)
                self.canvas.axes = self.canvas.figure.add_subplot(2,1,2)
                self.canvas.axes.imshow(sicm_data.z, cmap=matplotlib.cm.YlGnBu_r)
            if isinstance(sicm_data, ApproachCurve):
                self.canvas.axes = self.canvas.figure.add_subplot(111)
                self.canvas.axes.plot(*sicm_data.plot())
        self.canvas.figure.tight_layout()
        self.canvas.draw()