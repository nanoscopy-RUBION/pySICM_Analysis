import sys

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt6.QtGui import QIcon, QColor, QPixmap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from typing import Callable
from matplotlib import cm

from sicm_analyzer.view import View

COLOR_MAPS = {
    "AFM hot": cm.afmhot,
    "Bone": cm.bone,
    "Cividis": cm.cividis,
    "gist_yarg": cm.get_cmap("gist_yarg"),
    "Greys": cm.gray,
    "Hot (für Dilan)": cm.hot,
    "Jet": cm.jet,
    "Jet (reverse)": cm.jet_r,
    "Summer": cm.summer,
    "Summer (reverse)": cm.summer_r,
    "Viridis": cm.viridis,
    "Seriös cool": cm.YlGnBu_r,
    "Spectral": cm.Spectral,
    "RdYlBu": cm.RdYlBu,
    "Magma": cm.magma,
    "BrBG": cm.BrBG,
    "Monotone": cm.binary,
    "Earth": cm.gist_earth,
    "Ocean": cm.ocean
}

NUM_COLORS = {"2": 2,
              "3": 3,
              "4": 4,
              "5": 5,
              "6": 6
              }


class ColorMapDialog(QWidget):
    """
    This widget will appear as a free-floating window if it has no parent.
    """

    def __init__(self, controller, parent=None):
        """
        This widget will appear as a free-floating window if it has no parent.

        """

        super().__init__()
        self.parent = parent
        self.setWindowTitle("Color Map Chooser")
        self.setFixedSize(500, 300)
        self.setContentsMargins(15, 15, 15, 15)
        self.controller = controller
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        v_layout = QVBoxLayout()
        button_box = QWidget()
        button_box.setLayout(v_layout)

        self.button_custom_cmap = QPushButton("Create custom color map")

        self.cmap_combobox = QComboBox()
        self.cmap_combobox.addItems(COLOR_MAPS.keys())

        self.button_apply = QPushButton("Apply to selected")
        self.button_apply_to_checked = QPushButton("Apply to checked")
        self.button_apply_to_all = QPushButton("Apply to all")

        layout.addWidget(self.button_custom_cmap)
        layout.addWidget(self.cmap_combobox)
        layout.addWidget(button_box)
        v_layout.addWidget(self.button_apply)
        v_layout.addWidget(self.button_apply_to_checked)
        v_layout.addWidget(self.button_apply_to_all)

        self.button_custom_cmap.clicked.connect(
            lambda: self.open_custom_cmap_window()
        )
        self.button_apply.clicked.connect(
            lambda: self.controller.apply_colormap_to_selection(COLOR_MAPS.get(self.cmap_combobox.currentText()))
        )
        self.button_apply_to_checked.clicked.connect(
            lambda: self.controller.apply_colormap_to_checked(COLOR_MAPS.get(self.cmap_combobox.currentText()))
        )
        self.button_apply_to_all.clicked.connect(
            lambda: self.controller.apply_colormap_to_all(COLOR_MAPS.get(self.cmap_combobox.currentText()))
        )

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()

    def open_custom_cmap_window(self):
        cmap_window = CustomColorMapDialog()
        cmap_window.open_window()

        # return cmap_window.get_current_cmap()


class CustomColorMapDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Color Map Editor")
        self.setFixedSize(500, 300)
        self.setContentsMargins(20, 20, 20, 20)

        # overall vertical layout
        self.v1_layout = QVBoxLayout()
        self.v1_layout.setSpacing(10)
        self.setLayout(self.v1_layout)

        # horizontal layout 2 - num_colors box
        self.num_colors_box = QComboBox()
        self.num_colors_box.addItems(NUM_COLORS)

        # horizontal layout 3 - combo boxes
        h3_layout = QHBoxLayout()
        self.combo_box_holder_widget = QWidget()
        self.combo_box_holder_widget.setLayout(h3_layout)

        color_icon_dict = create_color_icon_dictionary()
        self.color_1_box = QComboBox()
        add_icons_to_combobox_items(self.color_1_box, color_icon_dict)
        self.color_2_box = QComboBox()
        add_icons_to_combobox_items(self.color_2_box, color_icon_dict)
        self.color_3_box = QComboBox()
        add_icons_to_combobox_items(self.color_3_box, color_icon_dict)

        h3_layout.addWidget(self.color_1_box)
        h3_layout.addWidget(self.color_2_box)
        h3_layout.addWidget(self.color_3_box)

        # horizontal layout 4 - preview push button
        self.preview_button = QPushButton("Preview Color Map")

        # horizontal layout 5 - color bar preview
        h5_layout = QHBoxLayout()
        self.color_bar_preview_widget = QWidget()
        self.color_bar_preview_widget.setLayout(h5_layout)

        self.colors = ['darkslategray', 'white', 'orange']
        self.cmap = create_custom_cmap(self.colors)

        self.color_bar_fig = generate_colorbar_figure(self.cmap)
        self.figure = FigureCanvas(self.color_bar_fig)

        # horizontal layout 6 - save cmap
        self.save_cmap_button = QPushButton("Use selected colormap")

        # adding all widgets to the final layout
        self.v1_layout.addWidget(self.num_colors_box)
        self.v1_layout.addWidget(self.combo_box_holder_widget)
        self.v1_layout.addWidget(self.preview_button)
        self.v1_layout.addWidget(self.figure)
        self.v1_layout.addWidget(self.save_cmap_button)

        # if clicked, call update_colorbar_preview will update the colorbar displayed to preview the colormap
        self.preview_button.clicked.connect(
            self.update_colorbar_preview
        )

    def get_selected_colors(self):
        selected_colors = [self.color_1_box.currentText(),
                           self.color_2_box.currentText(),
                           self.color_3_box.currentText()]

        return selected_colors

    def update_colorbar_figure(self):
        self.colors = self.get_selected_colors()
        self.cmap = create_custom_cmap(self.colors)
        self.color_bar_fig = generate_colorbar_figure(self.cmap)

        self.figure = FigureCanvas(self.color_bar_fig)

        return self.figure

    def update_colorbar_preview(self):
        self.v1_layout.replaceWidget(self.figure, self.update_colorbar_figure())

    def get_current_cmap(self):
        return self.cmap

    def save_and_close(self):
        return self.get_current_cmap()

    def open_window(self):
        if self.isVisible():
            self.hide()
        self.show()


# takes EMPTY QComboBox and a color dictionary (key=color_name(string), value=icon(QIcon)) & adds
# a new item (colorname) and sets the icon for that item for every entry in qcombobox.
def add_icons_to_combobox_items(qcombobox: QComboBox, color_dictionary):
    counter = 0

    for color_name in color_dictionary:
        qcombobox.addItem(color_name)
        qcombobox.setItemIcon(counter, color_dictionary[color_name])
        counter = counter + 1


# Takes in a list of user specified colors (len > 1) and returns color map
def create_custom_cmap(user_colors: list):
    if len(user_colors) < 2:
        raise ValueError('The length of user_colors was less than 2')

    # Generate a custom colormap
    cmap = LinearSegmentedColormap.from_list('custom_colormap', user_colors, N=256)
    return cmap


# test function to preview custom color map with mpl color bar
def preview_colorbar(cmap):
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap),
                 cax=ax, orientation='horizontal', label='Preview ColorMap')
    plt.show()


def generate_colorbar_figure(cmap):
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap),
                 cax=ax, orientation='horizontal')
    return fig


# creates a dictionary where the key is a string containing color_name from mcolors.CSS4 color list and the value
# is a QIcon object that will display the corresponding color
def create_color_icon_dictionary():
    color_icons = {}

    for color_name, color_value in mcolors.CSS4_COLORS.items():
        color = QColor(color_value)

        pixmap = QPixmap(20, 20)
        pixmap.fill(color)

        icon = QIcon(pixmap)

        color_icons[color_name] = icon

    return color_icons


if __name__ == '__main__':
    app = QApplication(sys.argv)
    testApp = CustomColorMapDialog()
    testApp.show()

    sys.exit(app.exec())
