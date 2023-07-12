import csv
import os

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PyQt6.QtGui import QIcon, QColor, QPixmap, QDoubleValidator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QLabel, QCheckBox, QDialog, QSlider, \
    QSpacerItem, QSizePolicy, QFileDialog, QMessageBox

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QColorDialog, QSpinBox
from matplotlib import cm
import numpy as np
from PyQt6.QtWidgets import QDialog

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

        self.button_custom_cmap = QPushButton("Create/Load Custom Color Map")

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
            self.open_custom_cmap_window
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

    def find_cmap(self, current_text):
        """ check if current_text is a value in COLOR_MAPS defined dictionary
        if it is, then get_cmap() and set self.current_cmap
        otherwise, self.current_cmap will already be set via custom cmap dialog"""
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
        self.cmap_window = CustomColorMapDialog()
        if self.cmap_window.exec() == QDialog.DialogCode.Accepted:
            self.current_custom_cmap = self.cmap_window.get_cmap()
            self.cmap_combobox.addItem(self.cmap_window.get_cmap().name)


class CustomColorMapDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Color Map Editor")
        # self.setFixedSize(650, 500)
        self.setContentsMargins(20, 20, 20, 20)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.positions = None

        # overall vertical layout
        self.v1_layout = QVBoxLayout()
        self.v1_layout.setSpacing(10)

        # ______OLD LAYOUT___________________________________________________________________________________________
        """
        # horizontal layout 2 - num_colors box
        self.num_colors_box = QComboBox()
        # self.num_colors_box.addItems(NUM_COLORS)

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
        # h5_layout = QHBoxLayout()
        # self.color_bar_preview_widget = QWidget()
        # self.color_bar_preview_widget.setLayout(h5_layout)

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
        """
        # ____________NEW LAYOUT__________________________________________________________________________________
        # below this line is the newly added functionality for the color chooser

        # default values
        self.num_colors = 6
        self.name = "n/a"
        self.cmap_data = []
        self.cmap = cm.get_cmap("viridis")

        self.v2_layout = QVBoxLayout()
        self.v2_layout.setSpacing(10)

        self.box_num_colors = QWidget()
        grid_num_colors = QGridLayout()
        self.box_num_colors.setLayout(grid_num_colors)
        self.label_num_colors = QLabel("Number of Colors (2-6):")
        self.spinbox_num_colors = QSpinBox()
        self.spinbox_num_colors.lineEdit().setReadOnly(True)
        self.spinbox_num_colors.setMinimum(2)
        self.spinbox_num_colors.setMaximum(6)
        self.spinbox_num_colors.setDisplayIntegerBase(6)
        self.button_apply_num = QPushButton("Apply Number of Colors")
        grid_num_colors.addWidget(self.label_num_colors, 0, 0)
        grid_num_colors.addWidget(self.spinbox_num_colors, 0, 1)
        grid_num_colors.addWidget(self.button_apply_num, 0, 2)

        self.box_six_colors = QWidget()
        grid_six_colors = QGridLayout()
        self.box_six_colors.setLayout(grid_six_colors)
        self.color1 = ColorModule(1)
        self.first_colormod = self.color1
        self.color2 = ColorModule(2)
        self.color3 = ColorModule(3)
        self.color4 = ColorModule(4)
        self.color5 = ColorModule(5)
        self.color6 = ColorModule(6)
        self.last_colormod = self.color6
        self.color_modules = [self.color1, self.color2, self.color3, self.color4, self.color5, self.color6]
        self.modules_dict = {obj.num_id: obj for obj in self.color_modules}
        self.set_equal_positioning()
        grid_six_colors.addWidget(self.color1, 0, 0)
        grid_six_colors.addWidget(self.color2, 0, 1)
        grid_six_colors.addWidget(self.color3, 0, 2)
        grid_six_colors.addWidget(self.color4, 0, 3)
        grid_six_colors.addWidget(self.color5, 0, 4)
        grid_six_colors.addWidget(self.color6, 0, 5)

        self.button_preview_cbar = QPushButton("Preview Custom Colormap")

        self.colors = ['black', 'grey', 'white']
        self.cmap = self.create_custom_cmap(self.colors)

        self.color_bar_fig = generate_colorbar_figure(self.cmap)
        self.figure = FigureCanvas(self.color_bar_fig)

        self.box_save_options = QWidget()
        grid_save_options = QGridLayout()
        self.box_save_options.setLayout(grid_save_options)
        self.button_load_cmap = QPushButton("Load Saved Cmap")
        self.button_save_cmap = QPushButton("Save As")
        self.button_use_cmap = QPushButton("Use cmap")
        self.button_use_cmap.setEnabled(False)
        grid_save_options.addWidget(self.button_load_cmap, 0, 0)
        grid_save_options.addWidget(self.button_save_cmap, 0, 1, 1, 4)
        grid_save_options.addWidget(self.button_use_cmap, 0, 5)

        self.v2_layout.addWidget(self.box_num_colors)
        self.v2_layout.addWidget(self.box_six_colors)
        self.v2_layout.addItem(QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.v2_layout.addWidget(self.button_preview_cbar)
        self.v2_layout.addWidget(self.figure)
        self.v2_layout.addItem(QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.v2_layout.addWidget(self.box_save_options)

        self.button_apply_num.clicked.connect(self.apply_num_colors_visible)
        self.button_preview_cbar.clicked.connect(self.set_colorbar_preview)
        self.button_load_cmap.clicked.connect(self.get_cmap_data_from_file)
        self.button_save_cmap.clicked.connect(self.open_save_cmap_window)
        self.button_use_cmap.clicked.connect(self.save_and_close)
        # __________________________________________________________________________________________________________
        # WHEN READY, SET LAYOUT OF SELF TO SWITCH BETWEEN OLD AND NEW UI ------------------------------------------

        self.setLayout(self.v2_layout)

    def load_cmap_data_to_editor(self, data):
        self.spinbox_num_colors.setValue(len(data))
        self.apply_num_colors_visible()

        counter = 0

        for x in data:
            self.color_modules[counter].loading = True
            if "True" in x[0]:
                self.color_modules[counter].reset_to_custom()
                self.color_modules[counter].custom_color = parse_tuple(x[1])
                self.color_modules[counter].display_swatch()
                self.color_modules[counter].position = x[2]
                self.color_modules[counter].line_position.setText(str(x[2]))
                self.color_modules[counter].display_rgba()
            else:
                self.color_modules[counter].reset_to_predefined()
                self.color_modules[counter].combobox_predefined.setCurrentText(x[1])
                self.color_modules[counter].position = x[2]
                self.color_modules[counter].line_position.setText(str(x[2]))
            self.color_modules[counter].loading = False
            counter = counter + 1

        self.set_colorbar_preview()

    def get_cmap_data_from_file(self):
        loader = QFileDialog()
        loader.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        options = loader.Option(QFileDialog.Option.DontUseNativeDialog)
        path = loader.getOpenFileName(
            caption="Open Colormap File",
            directory=os.getcwd(),
            filter="CSV (*.csv)",
            options=options
        )
        if (path[0] is not None) and (path[0] != ''):
            self.cmap_data = extract_cmap_data_from_csv(path[0])
            self.cmap.name = extract_filename(str(path[0]))
            self.load_cmap_data_to_editor(self.cmap_data)


    def open_save_cmap_window(self):
        directories = QFileDialog()
        directories.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        directories.setFileMode(QFileDialog.FileMode.AnyFile)
        directories.setDefaultSuffix("csv")
        options = directories.Option(QFileDialog.Option.DontUseNativeDialog)
        filepath = directories.getSaveFileName(
            caption="Save Colormap As",
            directory=os.getcwd(),
            filter="CSV (*.csv)",
            options=options
        )
        string_filepath = filepath[0]
        if not string_filepath.endswith(".csv"):
            string_filepath += ".csv"
        data = self.get_data_for_csv()
        write_cmap_to_csv(data, string_filepath)
        self.cmap.name = extract_filename(str(string_filepath))

    def get_data_for_csv(self):
        clrs = self.get_dynamic_color_text()
        psns = self.get_dynamic_positions()
        bools = []
        for mod in self.color_modules:
            if mod.num_id > self.num_colors:
                continue
            else:
                bools.append(mod.check_custom_color.isChecked())

        rtn = tuple(zip(bools, clrs, psns))
        return rtn

    def set_colorbar_preview(self):
        self.button_use_cmap.setEnabled(True)
        self.v2_layout.replaceWidget(self.figure, self.update_colormap())

    def update_colormap(self):
        try:
            positions = self.get_dynamic_positions()
            self.cmap = self.create_custom_cmap(self.get_dynamic_color_text(), positions)
            self.color_bar_fig = generate_colorbar_figure(self.cmap)
            self.figure = FigureCanvas(self.color_bar_fig)
            return self.figure
        except ValueError:
            error_msg = QMessageBox.critical(self, "Invalid Positional Input",
                                             "Invalid Positional Input \nPosition mapping points must be "
                                             "in increasing order from 0.0 to 1.0.",
                                             buttons=QMessageBox.StandardButton.Ok,
                                             defaultButton=QMessageBox.StandardButton.Ok)

    # TODO delete once finished with testing
    def test_getters(self):
        print("colors:")
        print(self.get_dynamic_color_text())
        print("positions:")
        print(self.get_dynamic_positions())

    def set_equal_positioning(self):
        positions = np.linspace(0.000, 1.000, self.num_colors)

        for i in range(self.num_colors):
            self.color_modules[i].line_position.setText(str(positions[i]))

        self.first_colormod.line_position.setReadOnly(True)
        self.last_colormod.line_position.setReadOnly(True)

    def get_dynamic_positions(self):
        pos = []

        for i in range(self.num_colors):
            pos.append(float(self.color_modules[i].line_position.text()))

        if not all(pos[i] < pos[i + 1] for i in range(len(pos) - 1)):
            raise ValueError

        return pos

    def get_dynamic_color_text(self):
        col = []

        for mod in self.color_modules:
            if mod.num_id > self.num_colors:
                break
            if not mod.check_custom_color.isChecked():
                col.append(mod.combobox_predefined.currentText())
            else:
                col.append(mod.custom_color)

        return col

    def create_custom_cmap(self, user_colors: list, positions=None):
        """
        Takes in a list of user specified colors (len > 1) and returns color map
        """
        if len(user_colors) < 2:
            raise ValueError('The length of user_colors was less than 2')

        name = 'xxTemp'

        if (self.cmap.name != "n/a") or (self.cmap.name != "xxTemp"):
            name = self.cmap.name

        if positions is not None:
            zipped_colors_positions = tuple(zip(positions, user_colors))
            cmap = LinearSegmentedColormap.from_list(name, zipped_colors_positions, N=256)
        else:
            cmap = LinearSegmentedColormap.from_list(name, user_colors, N=256)

        return cmap

    def get_cmap(self):
        return self.cmap

    def save_and_close(self):
        self.done(QDialog.DialogCode.Accepted)

    # self.exec() creates a modal window!! better than self.open(), which creates a window in parallel to colormapdialog
    def open_cmap_window(self):
        if self.isVisible():
            self.hide()
        self.exec()

    def apply_num_colors_visible(self):
        self.num_colors = self.spinbox_num_colors.value()
        self.last_colormod.line_position.setReadOnly(False)
        self.last_colormod = self.modules_dict.get(self.num_colors)

        for x in self.color_modules:
            if x.num_id > self.num_colors:
                if x.hidden:
                    continue
                else:
                    x.toggle_hidden()
            else:
                if x.hidden:
                    x.toggle_hidden()

        self.set_equal_positioning()

        """
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
            if not all(positions[i] < positions[i + 1] for i in range(len(positions) - 1)):
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
        """


class ColorModule(QWidget):
    """Creates a small widget for each color containing id, option to choose predefined/custom, and set position"""

    def __init__(self, num_id: int):
        super().__init__()
        self.picker = None
        self.num_id = num_id
        self.hidden = False
        self.isFirstColor = False
        self.isLastColor = False
        self.loading = False
        self.position = -1.000
        self.custom_color = '(0.2, 0.3, 0.4, 1)'
        self.setWindowTitle("Color " + str(num_id))

        grid = QGridLayout()

        self.label_id = QLabel("COLOR " + str(num_id) + "   ")
        self.combobox_predefined = QComboBox()
        icon_dict = create_color_icon_dictionary()
        add_icons_to_combobox_items(self.combobox_predefined, icon_dict)
        self.check_custom_color = QCheckBox("Use custom?")
        self.button_choose_color = QPushButton('Choose')
        self.button_choose_color.setDisabled(True)
        self.label_swatch = QLabel('.')
        self.label_hexcolor = QLabel('RGBA: ')
        self.line_rgba = QLineEdit('none')
        self.line_rgba.setReadOnly(True)
        self.label_spacer = QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.label_position = QLabel("Position (0-1):")
        self.line_position = QLineEdit()

        grid.addWidget(self.label_id, 0, 0, 1, 3)
        grid.addWidget(self.combobox_predefined, 1, 0, 1, 3)
        # grid.addItem(self.label_spacer, 2, 0)
        grid.addItem(QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 2, 0)
        grid.addWidget(self.check_custom_color, 3, 0, 1, 2)
        grid.addWidget(self.button_choose_color, 3, 2)
        grid.addWidget(self.label_swatch, 5, 0)
        grid.addWidget(self.label_hexcolor, 5, 1)
        grid.addWidget(self.line_rgba, 5, 2)
        # grid.addItem(self.label_spacer, 6, 0)
        grid.addItem(QSpacerItem(50, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 2, 0)
        grid.addWidget(self.label_position, 7, 0, 1, 2)
        grid.addWidget(self.line_position, 7, 2)

        self.setLayout(grid)

        self.check_custom_color.stateChanged.connect(self.update_choose_button)

        self.button_choose_color.clicked.connect(self.open_colorpicker_dialog)

    def open_colorpicker_dialog(self):
        self.picker = QColorDialog()
        self.picker.setOptions(QColorDialog.ColorDialogOption.DontUseNativeDialog)
        self.picker.exec()

        whole_rgb = self.picker.currentColor().getRgb()
        self.custom_color = tuple(value / 256 for value in whole_rgb)

        self.display_swatch()
        self.display_rgba()

    def reset_to_predefined(self):
        self.combobox_predefined.setEnabled(True)
        self.check_custom_color.setChecked(False)
        self.button_choose_color.setEnabled(False)
        self.label_swatch.setStyleSheet("background-color: transparent")
        self.line_rgba.setText(" ")

    def reset_to_custom(self):
        self.combobox_predefined.setEnabled(False)
        self.check_custom_color.setChecked(True)
        self.button_choose_color.setEnabled(True)

    def update_choose_button(self):
        if self.loading:
            return
        if not self.check_custom_color.isChecked():
            self.label_swatch.setStyleSheet("background-color: transparent")
        self.button_choose_color.setEnabled(not self.button_choose_color.isEnabled())
        self.combobox_predefined.setEnabled(not self.combobox_predefined.isEnabled())

    def toggle_hidden(self):
        self.hidden = not self.hidden
        self.label_id.setHidden(not self.label_id.isHidden())
        self.combobox_predefined.setHidden(not self.combobox_predefined.isHidden())
        self.check_custom_color.setHidden(not self.check_custom_color.isHidden())
        self.button_choose_color.setHidden(not self.button_choose_color.isHidden())
        self.label_swatch.setHidden(not self.label_swatch.isHidden())
        self.label_hexcolor.setHidden(not self.label_hexcolor.isHidden())
        self.line_rgba.setHidden(not self.line_rgba.isHidden())
        self.label_position.setHidden(not self.label_position.isHidden())
        self.line_position.setHidden(not self.line_position.isHidden())

    def display_rgba(self):
        self.line_rgba.setText(str(self.custom_color))

    def display_swatch(self):
        color = f"rgba({self.custom_color[0] * 256}, " \
                f"{self.custom_color[1] * 256}, " \
                f"{self.custom_color[2] * 256}, " \
                f"{self.custom_color[3] * 256})"
        self.label_swatch.setStyleSheet(f"background-color: {color}")


def extract_filename(path):
    filename_with_extension = os.path.basename(path)
    filename, _ = os.path.splitext(filename_with_extension)
    return filename


def write_cmap_to_csv(data, filename):
    """
    file format: csv with 3 columns, N rows (N = number of colors)
    - isCustom: bool
    - color: either a CSS4 name or a RBGA tuple (R, G, B, A)
    - position: float between 0 and 1
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['isCustom', 'Color', 'Position'])  # Write header row
        writer.writerows(data)  # Write data rows


def extract_cmap_data_from_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            isCustom, color, position = row
            data.append((isCustom, color, float(position)))
    return data


def parse_tuple(string):
    try:
        values = string.strip('()').split(',')
        if len(values) != 4:
            raise ValueError("Input does not represent a tuple of length 4.")

        parsed_tuple = tuple(float(val.strip()) for val in values)
        return parsed_tuple
    except ValueError as e:
        raise ValueError("Invalid tuple string format.") from e


# takes EMPTY QComboBox and a color dictionary (key=color_name(string), value=icon(QIcon)) & adds
# a new item (colorname) and sets the icon for that item for every entry in qcombobox.
def add_icons_to_combobox_items(qcombobox: QComboBox, color_dictionary):
    counter = 0

    for color_name in color_dictionary:
        qcombobox.addItem(color_name)
        qcombobox.setItemIcon(counter, color_dictionary[color_name])
        counter = counter + 1


#
# # test function to preview custom color map with mpl color bar
# def preview_colorbar(cmap):
#     fig, ax = plt.subplots(figsize=(6, 1))
#     fig.subplots_adjust(bottom=0.5)
#
#     fig.colorbar(plt.cm.ScalarMappable(cmap=cmap),
#                  cax=ax, orientation='horizontal', label='Preview ColorMap')
#     plt.show()
#

def generate_colorbar_figure(cmap):
    """Creates a new matplotlib figure that contains the colorbar preview"""
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.25)

    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap),
                 cax=ax, orientation='horizontal')
    return fig


def create_color_icon_dictionary():
    """
    dictionary for matching color names to color icons in predefined lists
    key: string containing color_name from mcolors.CSS4 color list
    value: QIcon object that displays a small swatch of corresponding color
    """
    color_icons = {}

    for color_name, color_value in mcolors.CSS4_COLORS.items():
        color = QColor(color_value)

        pixmap = QPixmap(20, 20)
        pixmap.fill(color)

        icon = QIcon(pixmap)

        color_icons[color_name] = icon

    return color_icons


def write_to_csv_test(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['isCustom', 'Color', 'Position'])  # Write header row
        writer.writerows(data)  # Write data rows


def extract_filename_test(path):
    filename_with_extension = os.path.basename(path)
    filename, _ = os.path.splitext(filename_with_extension)
    return filename


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # # testApp = CustomColorMapDialog()
    # # testApp.show()
    #
    # color_picker = QColorDialog()
    # color_picker.setOptions(QColorDialog.ColorDialogOption.DontUseNativeDialog)
    # color_picker.exec()
    #
    # color_picker.colorSelected.connect(print_something)
    # print(color_picker.currentColor().getRgb())
    #
    # sys.exit(app.exec())

    test_filepath = "/Users/claire/GitHubRepos/pySICM_Analysis/sicm_analyzer/tester1.csv"

    st = extract_filename_test(test_filepath)

    print(st)
