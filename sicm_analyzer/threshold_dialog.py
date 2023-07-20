import sys
from sicm_analyzer.sicm_data import SICMdata, get_sicm_data
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QApplication, QLabel, QLineEdit, QGridLayout, QWidget, QPushButton, \
    QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt


class ThresholdDialog(QDialog):
    """ Dialog allows user to
    - view distribution of z values for the selected view
    - select a threshold value by clicking plot OR entering value """
    def __init__(self, z: np.ndarray):
        super().__init__()

        self.z = z.flatten()
        self.threshold = min(self.z)
        self.ax_span = None
        self.coord = []

        self.setWindowTitle("Apply Threshold")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure, self.ax = self.distribution_plot()
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(-40, 40), textcoords="offset points",
                                      bbox=dict(boxstyle='square', fc='lightgrey', ec='k', lw=0.5),
                                      arrowprops=dict(arrowstyle='->'))
        self.annot.set_visible(False)

        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.box_thres = self.threshold_widget()
        layout.addWidget(self.box_thres)
        self.cursor = Cursor(self.ax, vertOn=True, horizOn=False, color='steelblue')

        cid = self.figure.canvas.mpl_connect('button_press_event', self.onclick)

        self.button_update.clicked.connect(self.update_threshold_line)

        self.button_apply.clicked.connect(self.close_window)

    def threshold_widget(self):
        """ QWidget that holds all text/buttons for displaying Z value distribution data and selecting threshold"""

        z_min = min(self.z)
        z_max = max(self.z)

        self.label_zmin = QLabel('Min Z value: ' + str(z_min))
        self.label_zmax = QLabel('Max Z value: ' + str(z_max))
        self.label_thres = QLabel("Set Threshold: ")
        self.line_thres = QLineEdit("type value OR click in plot above")
        self.button_update = QPushButton("update")
        self.spacer = QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.button_apply = QPushButton("Apply Threshold")

        grid = QGridLayout()
        holder = QWidget()
        holder.setLayout(grid)

        grid.addWidget(self.label_zmin, 0, 0, 1, 2)
        grid.addWidget(self.label_zmax, 1, 0, 1, 2)
        grid.addWidget(self.label_thres, 2, 0)
        grid.addWidget(self.line_thres, 2, 1, 1, 2)
        grid.addWidget(self.button_update, 2, 3)
        grid.addItem(self.spacer, 3, 0)
        grid.addWidget(self.button_apply, 4, 0)

        return holder

    def onclick(self, event):
        """ stores (x,y) value of click, updates threshold instance variable, line edit, & redraws figure """
        if len(self.ax.lines) > 0:
            self.ax.lines.pop()
        self.cursor = Cursor(self.ax, vertOn=True, horizOn=False)
        if self.ax_span:
            self.ax_span.remove()
        self.coord.append((event.xdata, event.ydata))
        x = event.xdata
        y = event.ydata

        # printing the values of the selected point
        self.threshold = x
        self.update_threshold_text()
        self.annot.xy = (x, y)
        text = "z = {:.3f}".format(x)
        self.ax.axvline(x, color='steelblue')
        self.annot.set_text(text)
        self.annot.set_visible(True)

        self.ax_span = self.ax.axvspan(min(self.z), x, color='steelblue', alpha=0.25, lw=0)
        self.ax.set_xlim(min(self.z))

        self.figure.canvas.draw()  # redraw the figure

    def update_threshold_text(self):
        self.line_thres.setText("{:.4f}".format(self.threshold))

    def update_threshold_line(self):
        """ updates threshold instance variable by taking user input from line edit"""

        self.threshold = float(self.line_thres.text())

        if len(self.ax.lines) > -1:
            self.ax.lines.pop()
        self.cursor = Cursor(self.ax, vertOn=True, horizOn=False)

        try:
            if self.ax_span:
                self.ax_span.remove()
        except ValueError:
            print("value error")

        self.annot.xy = (self.threshold, 2)
        text = "z = {:.3f}".format(self.threshold)
        self.ax.axvline(self.threshold, color='steelblue')
        self.annot.set_text(text)
        self.annot.set_visible(True)

        self.ax_span = self.ax.axvspan(min(self.z), self.threshold, color='steelblue', alpha=0.25, lw=0)
        self.ax.set_xlim(min(self.z))

        self.figure.canvas.draw()

    def get_threshold(self):
        return self.threshold

    def distribution_plot(self):
        fig, ax = plt.subplots()
        binwidth = 0.015
        ax.hist(self.z, bins=np.arange(min(self.z), max(self.z) + binwidth, binwidth), color='gray')
        ax.set_xlim(min(self.z), max(self.z))
        ax.set_xlabel('z values')
        ax.set_ylabel('frequency')
        ax.set_title('distribution of z values')

        return fig, ax

    def close_window(self):
        self.done(QDialog.DialogCode.Accepted)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    path = "/Users/claire/GitHubRepos/pySICM_Analysis/tests/sample_sicm_files/Zelle2 10x10 PFA.sicm"
    path2 = "/Users/claire/GitHubRepos/pySICM_Analysis/tests/sample_sicm_files/Zelle2Membran PFA.sicm"

    data = get_sicm_data(path2)

    print(data.y)

    test_dialog = ThresholdDialog(data.z)
    test_dialog.show()

    sys.exit(app.exec())
