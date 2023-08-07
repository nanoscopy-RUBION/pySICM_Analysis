import json
import os
import sys
import itertools

from PyQt6.uic.properties import QtCore

import sicm_analyzer.measurements
from sicm_analyzer.sicm_data import SICMdata, get_sicm_data
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QApplication, QLabel, QLineEdit, QGridLayout, QWidget, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox, QComboBox, QFileDialog
import sicm_analyzer.measurements
import numpy as np
import matplotlib.pyplot as plt

FILE_SELECTION = {"Selected file only": False,
                  "All checked files": True,
                  }

AMPLITUDE_PARAMS = ["2.1 Arithmetic average height (R_a)",
                    "2.2 Root mean square roughness",
                    "2.3 Ten-point height (ISO) (R_z)",
                    "2.3 Ten-point height (DIN) (R_z)",
                    "2.4 Maximum height of peaks (R_p)",
                    "2.5 Maximum depth of valleys (R_v)",
                    "2.6 Mean height of peaks (R_pm)",
                    "2.7 Mean depth of valleys (R_vm)",
                    "2.8 Maximum height of profile (R_t or R_max)",
                    "2.9 Maximum peak to valley height (R_ti)",
                    "2.10 Mean of max peak to valley height (R_tm)",
                    "2.11 Largest peak to valley height (R_y)",
                    "2.12 Third point height (R_3y)",
                    "2.13 Mean of the third point height (R_3z)",
                    "2.14 Profile solidarity factor (k)",
                    "2.15 Skewness (R_sk)",
                    "2.16 Kurtosis (R_ku)",
                    "2.17 Amplitude density function (ADF)",
                    "2.18 Auto correlation function (ACF)",
                    "2.19 Correlation Length (beta)",
                    "2.20 Power spectral density (PSD)"
                    ]

TEST_PARAMS = {"2.1 Arithmetic average height (R_a)": sicm_analyzer.measurements.get_arithmetic_average_height,
               "2.2 Root mean square roughness": sicm_analyzer.measurements.get_root_mean_sq_roughness,
               "2.3 Ten-point height (ISO) (R_z)": sicm_analyzer.measurements.get_ten_point_height_ISO,
               "2.3 Ten-point height (DIN) (R_z)": sicm_analyzer.measurements.get_ten_point_height_DIN,
               "2.4 Maximum height of peaks (R_p)": sicm_analyzer.measurements.get_max_peak_height_from_mean,
               "2.5 Maximum depth of valleys (R_v)": sicm_analyzer.measurements.get_max_valley_depth_from_mean,
               "2.6 Mean height of peaks (R_pm)": sicm_analyzer.measurements.get_mean_height_of_peaks,
               "2.7 Mean depth of valleys (R_vm)": sicm_analyzer.measurements.get_mean_depth_of_valleys,
               "2.8 Maximum height of profile (R_t or R_max)": sicm_analyzer.measurements.get_max_height_of_profile,
               "2.9 Maximum peak to valley height (R_ti)": sicm_analyzer.measurements.get_maximum_height_single_profile,
               "2.10 Mean of max peak to valley height (R_tm)":
                   sicm_analyzer.measurements.get_mean_maximum_peak_valley_heights,
               "2.11 Largest peak to valley height (R_y)": sicm_analyzer.measurements.get_largest_peak_to_valley_height,
               "2.12 Third point height (R_3y)": sicm_analyzer.measurements.get_third_point_height,
               "2.13 Mean of the third point height (R_3z)": sicm_analyzer.measurements.get_mean_of_third_point_height,
               "2.14 Profile solidarity factor (k)": sicm_analyzer.measurements.get_profile_solidarity_factor,
               "2.15 Skewness (R_sk)": sicm_analyzer.measurements.get_skewness,
               "2.16 Kurtosis (R_ku)": sicm_analyzer.measurements.get_kurtosis_coefficient,
               "2.17 Amplitude density function (ADF)": sicm_analyzer.measurements.get_amplitude_density_function,
               "2.18 Auto correlation function (ACF)": sicm_analyzer.measurements.get_auto_correlation_function,
               "2.19 Correlation Length (beta)": sicm_analyzer.measurements.get_correlation_length,
               "2.20 Power spectral density (PSD)": sicm_analyzer.measurements.get_power_spectral_density
               }

SPACING_PARAMS = ["High spot count (HSC)",
                  "Peak count (P_c)",
                  "Mean spacing of adjacent local peaks (S)",
                  "Mean spacing at mean line (S_m)",
                  "Number of intersections of the profile at mean line (n(0))",
                  "Number of peaks in the profile (m)",
                  "Number of inflection points (g)",
                  "Mean radius of asperities (r_p)"
                  ]

HYBRID_PARAMS = ["Profile slope at mean line (gamma)",
                 "Mean slope of the profile (delta_a)",
                 "RMS slope of the profile (delta_q)",
                 "Average wavelength (lambda_a)",
                 "Relative length of the profile (l_o)",
                 "Bearing area length (t_p) and bearing area curve",
                 "Stepness factor of the profile (S_f)",
                 "Waviness factor of the profile (W_f)",
                 "Roughness height uniformity (H_u)",
                 "Roughness height skewness (H_s)",
                 "Roughness pitch uniformity (P_u)",
                 "Roughness pitch skewness (P_s)"
                 ]


class ParametersDialog(QDialog):

    def __init__(self, controller=None, parent=None):
        super().__init__()

        self.parent = parent
        self.controller = controller
        self.setWindowTitle("Calculate Results Parameters")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.params = {}

        modular = QGridLayout()

        self.select_file_holder = QWidget()
        row = QGridLayout()
        self.select_file_holder.setLayout(row)
        self.label_file_selection = QLabel("Generate results table for: ")
        self.combobox_file_selection = QComboBox()
        self.combobox_file_selection.addItems(FILE_SELECTION.keys())
        self.button_show = QPushButton("Show results table")
        row.addWidget(self.label_file_selection, 0, 0)
        row.addWidget(self.combobox_file_selection, 0, 1)
        row.addWidget(self.button_show, 0, 2)

        self.amps = ParameterHolder("Amplitude Parameters", list(TEST_PARAMS.keys()))
        self.spaces = ParameterHolder("Spacing Parameters", SPACING_PARAMS)
        self.hybrids = ParameterHolder("Hybrid Parameters", HYBRID_PARAMS)

        self.button_save_config_as = QPushButton("Save parameter configuration")
        self.button_open_config = QPushButton("Open parameter configuration")

        modular.addWidget(self.select_file_holder, 0, 0, 1, 3)
        modular.addWidget(self.amps, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.spaces, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.hybrids, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.button_save_config_as, 2, 1)
        modular.addWidget(self.button_open_config, 2, 2)
        self.setLayout(modular)

        self.button_show.clicked.connect(self.controller.show_results_table_updated)
        self.button_save_config_as.clicked.connect(self.save_config)
        self.button_open_config.clicked.connect(self.open_config)

    def get_file_selection_option(self):
        selected = self.combobox_file_selection.currentText()
        return FILE_SELECTION[selected]

    def get_param_truth_values(self):
        self.params = self.amps.get_param_dictionary()
        self.params.update(self.spaces.get_param_dictionary())
        self.params.update(self.hybrids.get_param_dictionary())

    def write_json_file(self, filename: str):
        with open(filename, 'w') as outfile:
            json.dump(self.params, outfile)

    def save_config(self):
        directories = QFileDialog()
        directories.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        directories.setFileMode(QFileDialog.FileMode.AnyFile)
        directories.setDefaultSuffix("json")
        options = directories.Option(QFileDialog.Option.DontUseNativeDialog)
        filepath = directories.getSaveFileName(
            caption="Save Colormap As",
            directory=os.getcwd(),
            filter="JSON (*.json)",
            options=options
        )
        string_filepath = filepath[0]
        if not string_filepath.endswith(".json"):
            string_filepath += ".json"
        self.get_param_truth_values()
        self.write_json_file(string_filepath)

    def open_config(self):
        loader = QFileDialog()
        loader.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        options = loader.Option(QFileDialog.Option.DontUseNativeDialog)
        path = loader.getOpenFileName(
            caption="Open parameter configuration file",
            directory=os.getcwd(),
            filter="JSON (*.json)",
            options=options
        )
        if (path[0] is not None) and (path[0] != ''):
            print("successfully navigated the opening dialog")
            print(path[0])
            self.read_json_and_intialize(path[0])

    def read_json_and_intialize(self, filepath):
        with open(filepath) as config_file:
            contents = config_file.read()
            config_dict = json.loads(contents)
            print(config_dict)

            for cbox in self.amps.parameters:
                key = cbox.text()
                try:
                    isChecked = config_dict[key]
                    cbox.setChecked(isChecked)
                except TypeError:
                    print("something went wrong - the value from dictionary is not a boolean")

            for cbox in self.spaces.parameters:
                key = cbox.text()
                try:
                    isChecked = config_dict[key]
                    cbox.setChecked(isChecked)
                except TypeError:
                    print("something went wrong - the value from dictionary is not a boolean")

            for cbox in self.hybrids.parameters:
                key = cbox.text()
                try:
                    isChecked = config_dict[key]
                    cbox.setChecked(isChecked)
                except TypeError:
                    print("something went wrong - the value from dictionary is not a boolean")

    def get_selected_params(self):
        rtn = []

        for cbox in self.amps.parameters:
            if cbox.isChecked():
                rtn.append(cbox.text())

        for cbox in self.spaces.parameters:
            if cbox.isChecked():
                rtn.append(cbox.text())

        for cbox in self.hybrids.parameters:
            if cbox.isChecked():
                rtn.append(cbox.text())

        return rtn

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()


class ParameterHolder(QWidget):

    def __init__(self, category, param_names):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title = QLabel(category)
        self.title.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title)
        self.parameters = []

        for i in range(len(param_names)):
            x = QCheckBox(param_names[i])
            self.parameters.append(x)

        for i in self.parameters:
            layout.addWidget(i)

    def get_param_dictionary(self):
        rtn = {}
        for checkbox in self.parameters:
            rtn[checkbox.text()] = checkbox.isChecked()
        return rtn


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = ParametersDialog()
    test.show()
    sys.exit(app.exec())
