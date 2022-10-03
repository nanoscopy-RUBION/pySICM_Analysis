import csv
import numpy
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sicm_analyzer.graph_canvas import GraphCanvas


class LineProfileWindow(QWidget):
    """A small window for displaying line profile data.

    The canvas is an instance of GraphCanvas and thus
    supports all functionality of the class.

    A button for exporting the displayed data as
    a csv file is included.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.parent = parent
        self.toolbar = None
        self.canvas = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.export_button = QPushButton("Export data as csv")

        self.layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_as_csv)

    def export_as_csv(self):
        """Exports x and y data as csv file.

        For convenience .csv extension is added
        to the file name.
        """
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        file_path = QFileDialog.getSaveFileName(parent=self.parent,
                                                caption="Export line profile data as csv file",
                                                filter="All files (*.*);;CSV (*.csv)",
                                                #directory=DEFAULT_FILE_PATH,
                                                initialFilter="CSV (*.csv)",
                                                options=options
                                                )
        if file_path[0]:
            if file_path[0].lower().endswith(".csv"):
                file_path = file_path[0]
            else:
                file_path = file_path[0] + ".csv"

            with open(file_path, "w", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                for i in range(len(self.x1)):
                    writer.writerow([self.x1[i], self.y1[i]])

    def add_canvas(self, canvas: GraphCanvas):
        self.canvas = canvas
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def update_plot(self, x: numpy.ndarray, y: numpy.ndarray):
        self.x1 = x.tolist()
        self.y1 = y.tolist()
        self.canvas.draw_line_plot(x, y)

    def update_xy_line_profile_plot(self, x_x, x_y, y_x, y_y):
        self.x1 = x_x.tolist()
        self.y1 = x_y.tolist()
        self.x2 = y_x.tolist()
        self.y2 = y_y.tolist()
        self.canvas.draw_xy_line_profiles(x_x, x_y, y_x, y_y)
