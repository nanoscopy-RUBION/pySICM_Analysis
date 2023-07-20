import sys

from PyQt6.uic.properties import QtCore

from sicm_analyzer.sicm_data import SICMdata, get_sicm_data
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QApplication, QLabel, QLineEdit, QGridLayout, QWidget, QPushButton, \
    QSpacerItem, QSizePolicy, QCheckBox, QComboBox
import numpy as np
import matplotlib.pyplot as plt

FILE_SELECTION = {"Selected file only": False,
                  "All checked files": True
                  }

AMPLITUDE_PARAMS = {0: "Arithmetic average height (R_a)",
                    1: "Root mean square roughness",
                    2: "Ten-point height (ISO) (R_z)",
                    3: "Ten-point height (DIN) (R_z)",
                    4: "Maximum height of peaks (R_p)",
                    5: "Maximum depth of valleys (R_v)"
                    }

SPACING_PARAMS = {0: "High spot count (HSC)",
                  1: "Peak count (P_c)",
                  2: "Mean spacing of adjacent local peaks (S)",
                  3: "Mean spacing at mean line (S_m)",
                  4: "Number of intersections of the profile at mean line (n(0))",
                  5: "Number of peaks in the profile (m)",
                  6: "Number of inflection points (g)",
                  7: "Mean radius of asperities (r_p)"
                  }

HYBRID_PARAMS = {0: "Profile slope at mean line (gamma)",
                 1: "Mean slope of the profile (delta_a)",
                 2: "RMS slope of the profile (delta_q)",
                 3: "Average wavelength (lambda_a)",
                 4: "Relative length of the profile (l_o)",
                 5: "Bearing area length (t_p) and bearing area curve",
                 6: "Stepness factor of the profile (S_f)",
                 7: "Waviness factor of the profile (W_f)",
                 8: "Roughness height uniformity (H_u)",
                 9: "Roughness height skewness (H_s)",
                 10: "Roughness pitch uniformity (P_u)",
                 11: "Roughness pitch skewness (P_s)"
                 }


class ParametersDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculate Results Parameters")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

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

        self.amps = ParameterHolder("Amplitude Parameters", AMPLITUDE_PARAMS)
        self.spaces = ParameterHolder("Spacing Parameters", SPACING_PARAMS)
        self.hybrids = ParameterHolder("Hybrid Parameters", HYBRID_PARAMS)

        modular.addWidget(self.select_file_holder, 0, 0, 1, 3)
        modular.addWidget(self.amps, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.spaces, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.hybrids, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(modular)


class ParameterHolder(QWidget):

    def __init__(self, category, param_names: dict):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title = QLabel(category)
        self.title.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title)
        self.parameters = []

        for i in range(len(param_names)):
            x = QCheckBox(param_names.get(i))
            self.parameters.append(x)

        for i in self.parameters:
            layout.addWidget(i)

    def get_checked_params(self):

        rtn = []

        for checkbox in self.parameters:
            if checkbox is QCheckBox():
                rtn.append(checkbox.isChecked())

        return rtn


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = ParametersDialog()
    test.show()
    sys.exit(app.exec())
