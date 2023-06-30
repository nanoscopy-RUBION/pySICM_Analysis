import sys

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt6.QtGui import QIcon, QColor, QPixmap, QDoubleValidator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QLabel, QCheckBox, QDialog

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from typing import Callable
from matplotlib import cm

COLOR_MAPS = {
    "AFM hot": cm.afmhot,
    "Bone": cm.bone,
    "cividis": cm.cividis,
    "gist_yarg": cm.get_cmap("gist_yarg"),
    "grays": cm.gray,
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
        self.cmap_window = None
        self.current_cmap = None
        self.current_custom_cmap = None

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
            lambda: self.controller.apply_colormap_to_selection(self.find_cmap(self.cmap_combobox.currentText()))
        )
        self.button_apply_to_checked.clicked.connect(
            lambda: self.controller.apply_colormap_to_checked(self.find_cmap(self.cmap_combobox.currentText()))
        )
        self.button_apply_to_all.clicked.connect(
            lambda: self.controller.apply_colormap_to_all(self.find_cmap(self.cmap_combobox.currentText()))
        )

    # check if current_text is a value in the COLOR_MAPS defined dictionary
    # if it is, then get_cmap() and set self.current_cmap
    # otherwise, self.current_cmap will already be set via custom cmap dialog
    def find_cmap(self, current_text):
        if current_text in COLOR_MAPS.keys():
            self.current_cmap = COLOR_MAPS.get(current_text)
            return self.current_cmap
        else:
            return self.current_custom_cmap

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()

    def open_custom_cmap_window(self):
        # print("open_custom_cmap_window()")
        self.cmap_window = CustomColorMapDialog()
        self.cmap_window.open_cmap_window()
        self.current_custom_cmap = self.cmap_window.get_cmap()
        self.cmap_combobox.addItem(self.cmap_window.get_cmap().name)

        # print("I've reached the end of open_custom_cmap_window().")
        # print("The current cmap is" + self.current_cmap.name)


class CustomColorMapDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Color Map Editor")
        self.setFixedSize(650, 500)
        self.setContentsMargins(20, 20, 20, 20)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.positions = None

        # overall vertical layout
        self.v1_layout = QVBoxLayout()
        self.v1_layout.setSpacing(10)
        self.setLayout(self.v1_layout)

        # horizontal layout 2 - num_colors box
        self.num_colors_box = QComboBox()
        self.num_colors_box.addItems(NUM_COLORS)

        # alternative horizontal layout 3 - grid layout
        h3_layout_grid = QGridLayout()

        # horizontal layout 3 - combo boxes
        self.combo_box_holder_widget = QWidget()
        self.combo_box_holder_widget.setLayout(h3_layout_grid)

        color_icon_dict = create_color_icon_dictionary()
        self.color_1_box = QComboBox()
        add_icons_to_combobox_items(self.color_1_box, color_icon_dict)
        self.color_2_box = QComboBox()
        add_icons_to_combobox_items(self.color_2_box, color_icon_dict)
        self.color_3_box = QComboBox()
        add_icons_to_combobox_items(self.color_3_box, color_icon_dict)

        self.check_use_custom_positions = QCheckBox(
            "Use custom positioning of colors in color map. End points must be 0.0 and 1.0"
        )

        self.label_colors = QLabel("Colors")
        self.label_positions = QLabel("Position (0.0-1.0)")

        self.position_1_box = QLineEdit()
        self.position_1_box.setReadOnly(True)
        self.position_2_box = QLineEdit()
        self.position_2_box.setReadOnly(True)
        self.position_3_box = QLineEdit()
        self.position_3_box.setReadOnly(True)

        self.msg_invalid_position2 = QLabel("   invalid input")
        self.msg_invalid_position2.setStyleSheet("color: red;")
        self.msg_invalid_position2.hide()

        middle_validator = QDoubleValidator(0.000, 0.999, 3)
        self.position_2_box.setValidator(middle_validator)

        h3_layout_grid.addWidget(self.label_colors, 0, 0)
        h3_layout_grid.addWidget(self.color_1_box, 0, 1)
        h3_layout_grid.addWidget(self.color_2_box, 0, 2)
        h3_layout_grid.addWidget(self.color_3_box, 0, 3)
        h3_layout_grid.addWidget(self.check_use_custom_positions, 1, 0, 1, 4)
        h3_layout_grid.addWidget(self.label_positions, 2, 0)
        h3_layout_grid.addWidget(self.position_1_box, 2, 1)
        h3_layout_grid.addWidget(self.position_2_box, 2, 2)
        h3_layout_grid.addWidget(self.position_3_box, 2, 3)
        h3_layout_grid.addWidget(self.msg_invalid_position2, 3, 2)

        # horizontal layout 4 - preview push button
        self.preview_button = QPushButton("Preview Color Map")

        # horizontal layout 5 - color bar preview
        h5_layout = QHBoxLayout()
        self.color_bar_preview_widget = QWidget()
        self.color_bar_preview_widget.setLayout(h5_layout)

        self.colors = ['black', 'grey', 'white']
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

        self.save_cmap_button.clicked.connect(
            self.save_and_close
        )

        self.check_use_custom_positions.stateChanged.connect(
            self.update_line_edit_state
        )

    def update_line_edit_state(self):
        self.position_1_box.setText('0.000')
        self.position_2_box.setReadOnly(not self.position_2_box.isReadOnly())
        self.position_3_box.setText('1.000')

    def get_selected_colors(self):
        selected_colors = [self.color_1_box.currentText(),
                           self.color_2_box.currentText(),
                           self.color_3_box.currentText()]

        return selected_colors

    def get_selected_positions(self):
        selected_positions = [float(self.position_1_box.text()),
                              float(self.position_2_box.text()),
                              float(self.position_3_box.text())]

        # checks if the middle value is between 0 and 1
        if not self.validate_position_input(selected_positions):
            self.msg_invalid_position2.show()
            return
        else:
            self.msg_invalid_position2.hide()
            return selected_positions

    def validate_position_input(self, positions):
        if not all(positions[i] < positions[i+1] for i in range(len(positions)-1)):
            return False
        else:
            return True

    # creates the current colormap (based on using custom positions or not), assigns it to cmap attribute,
    # and updates the colorbar preview
    def update_colorbar_figure(self):

        self.colors = self.get_selected_colors()

        if self.check_use_custom_positions.isChecked():
            self.positions = self.get_selected_positions()
            self.cmap = create_custom_cmap(self.colors, self.positions)
        else:
            self.cmap = create_custom_cmap(self.colors)

        self.color_bar_fig = generate_colorbar_figure(self.cmap)
        self.figure = FigureCanvas(self.color_bar_fig)

        return self.figure

    def update_colorbar_preview(self):
        self.v1_layout.replaceWidget(self.figure, self.update_colorbar_figure())

    def get_cmap(self):
        return self.cmap

    def save_and_close(self):
        # print("custom color map dialog: self.cmap.name = " + self.cmap.name)
        self.close()

    # self.exec() creates a modal window!! self.open() creates a window in parallel to colormapdialog
    def open_cmap_window(self):
        if self.isVisible():
            self.hide()
        self.exec()


# Takes in a list of strings (colors), and returns a concatenated string separated by dashes
def color_namer(colors):
    rtn = ""
    for color in colors:
        rtn += color + "-"
    rtn = rtn[:-1]

    return rtn


# takes EMPTY QComboBox and a color dictionary (key=color_name(string), value=icon(QIcon)) & adds
# a new item (colorname) and sets the icon for that item for every entry in qcombobox.
def add_icons_to_combobox_items(qcombobox: QComboBox, color_dictionary):

    counter = 0

    for color_name in color_dictionary:
        qcombobox.addItem(color_name)
        qcombobox.setItemIcon(counter, color_dictionary[color_name])
        counter = counter + 1


# Takes in a list of user specified colors (len > 1) and returns color map
def create_custom_cmap(user_colors: list, positions=None):
    if len(user_colors) < 2:
        raise ValueError('The length of user_colors was less than 2')

    map_name = color_namer(user_colors)

    if positions is not None:
        zipped_colors_positions = tuple(zip(positions, user_colors))
        cmap = LinearSegmentedColormap.from_list(map_name, zipped_colors_positions, N=256)
    else:
        cmap = LinearSegmentedColormap.from_list(map_name, user_colors, N=256)

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
    fig.subplots_adjust(bottom=0.25)

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

    # test_colors = ['blue', 'white', 'red']
    #
    # test_cmap = create_custom_cmap(test_colors)
    # plt.cm.register_cmap(name="CL_test", cmap=test_cmap)
    #
    # test to see if my colormap is being registered correctly with the plt cm registry
    # preview_colorbar(plt.cm.get_cmap('CL_test'))

    sys.exit(app.exec())
