import csv

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class LineProfileWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.x = []
        self.y = []
        self.parent = parent
        self.toolbar = None
        self.canvas = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.export_button = QPushButton("Export data as csv")

        self.layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_as_csv)

    def export_as_csv(self):
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
                data1 = self.x.tolist()
                data2 = self.y.tolist()
                for i in range(len(data1)):
                    writer.writerow([data1[i], data2[i]])

    def add_canvas(self, canvas):
        self.canvas = canvas
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def update_plot(self, x, y):
        self.x = x
        self.y = y
        self.canvas.plot_line_profile(x, y)
