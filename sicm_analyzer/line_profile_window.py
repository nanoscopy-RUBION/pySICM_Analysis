from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class LineProfileWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.toolbar = None
        self.canvas = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def add_canvas(self, canvas):
        self.canvas = canvas
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def update_plot(self, x, y):
        self.canvas.plot_line_profile(x, y)
