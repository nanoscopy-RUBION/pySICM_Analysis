import json
import os
import sys
from enum import Enum
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QStyle, QVBoxLayout, QApplication, QLabel, QGridLayout, QWidget, QPushButton, QCheckBox, \
                            QComboBox, QFileDialog
from sicm_analyzer.parameters import GeneralParameters, AmplitudeParameters, SpacingParameters, HybridParameters, IMPLEMENTED_PARAMETERS


class FileSelectionOption(Enum):
    CURRENT_SELECTION = "Selected file only"
    ALL_CHECKED_ITEMS = "All checked files"
    ALL_FILES = "All imported files"


class ParametersDialog(QDialog):

    def __init__(self, controller=None, parent=None):
        super().__init__()

        pixmap = QStyle.StandardPixmap.SP_DriveFDIcon
        save_icon = self.style().standardIcon(pixmap)
        pixmap = QStyle.StandardPixmap.SP_DirOpenIcon
        open_icon = self.style().standardIcon(pixmap)

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
        for entry in FileSelectionOption:
            self.combobox_file_selection.insertItem(
                self.combobox_file_selection.count(),
                entry.value,
                entry
            )

        self.button_holder = QWidget()
        button_holder_layout = QGridLayout()
        self.button_holder.setLayout(button_holder_layout)
        self.button_select_all = QPushButton("Select all parameters")
        self.button_unselect_all = QPushButton("Unselect all parameters")
        self.button_save_config_as = QPushButton(save_icon, "Save parameter configuration")
        self.button_open_config = QPushButton(open_icon, "Open parameter configuration")
        button_holder_layout.addWidget(self.button_select_all, 0, 0)
        button_holder_layout.addWidget(self.button_unselect_all, 1, 0)
        button_holder_layout.addWidget(self.button_save_config_as, 0, 1)
        button_holder_layout.addWidget(self.button_open_config, 1, 1)

        self.button_show = QPushButton("Show results table")
        row.addWidget(self.label_file_selection, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        row.addWidget(self.combobox_file_selection, 0, 1)
        row.addWidget(self.button_show, 0, 2)

        self.general = ParameterHolder("General Parameters", GeneralParameters.list())
        self.amps = ParameterHolder("Amplitude Parameters", AmplitudeParameters.list())
        self.spaces = ParameterHolder("Spacing Parameters", SpacingParameters.list())
        self.hybrids = ParameterHolder("Hybrid Parameters", HybridParameters.list())

        modular.addWidget(self.button_holder, 0, 0, 2, 2)
        modular.addWidget(self.select_file_holder, 0, 2, 1, 2)
        modular.addWidget(self.general, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.amps, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.spaces, 2, 2, alignment=Qt.AlignmentFlag.AlignTop)
        modular.addWidget(self.hybrids, 2, 3, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(modular)

        self.button_select_all.clicked.connect(self.select_all_parameters)
        self.button_unselect_all.clicked.connect(self.unselect_all_parameters)
        self.button_show.clicked.connect(self.controller.show_results_table_updated)
        self.button_save_config_as.clicked.connect(self.save_config)
        self.button_open_config.clicked.connect(self.open_config)

    def get_file_selection_option(self) -> FileSelectionOption:
        return self.combobox_file_selection.currentData()

    def get_param_truth_values(self):
        self.params = self.general.get_param_dictionary()
        self.params.update(self.amps.get_param_dictionary())
        self.params.update(self.spaces.get_param_dictionary())
        self.params.update(self.hybrids.get_param_dictionary())

    def write_json_file(self, filename: str):
        with open(filename, 'w') as outfile:
            json.dump(self.params, outfile, indent=4)

    def save_config(self):
        directories = QFileDialog()
        directories.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        directories.setFileMode(QFileDialog.FileMode.AnyFile)
        directories.setDefaultSuffix("json")
        options = directories.Option(QFileDialog.Option.DontUseNativeDialog)
        filepath = directories.getSaveFileName(
            caption="Save parameter configuration file",
            directory=os.getcwd(),
            filter="JSON (*.json)",
            options=options
        )

        if filepath[0]:
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
        if path[0]:
            self.read_json_and_initialize(path[0])

    def read_json_and_initialize(self, filepath):
        with open(filepath) as config_file:
            contents = config_file.read()
            config_dict = json.loads(contents)

            self.general.apply_config(config_dict)
            self.amps.apply_config(config_dict)
            self.spaces.apply_config(config_dict)
            self.hybrids.apply_config(config_dict)

    def get_all_selected_params(self) -> list[str]:
        """Returns a list containing all names of parameters which
        have been checked."""
        rtn = []
        rtn.extend(self.general.get_selected_params())
        rtn.extend(self.amps.get_selected_params())
        rtn.extend(self.spaces.get_selected_params())
        rtn.extend(self.hybrids.get_selected_params())
        return rtn

    def select_all_parameters(self):
        self._set_checked_for_all_parameters(True)

    def unselect_all_parameters(self):
        self._set_checked_for_all_parameters(False)

    def _set_checked_for_all_parameters(self, is_checked: bool):
        self.general.set_checked_all(is_checked)
        self.amps.set_checked_all(is_checked)
        self.spaces.set_checked_all(is_checked)
        self.hybrids.set_checked_all(is_checked)

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()


class ParameterHolder(QWidget):
    """A widget containing checkboxes for parameters."""
    def __init__(self, category, param_names: list[str]):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title = QLabel(category)
        self.title.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title)
        self.parameters: list[QCheckBox] = []
        for name in param_names:
            new_checkbox = QCheckBox(name)
            if not IMPLEMENTED_PARAMETERS.get(name, None):
                new_checkbox.setEnabled(False)
                new_checkbox.setToolTip("Not implemented")
            self.parameters.append(new_checkbox)

        for checkbox in self.parameters:
            layout.addWidget(checkbox)

    def get_param_dictionary(self) -> dict[str, bool]:
        rtn = {}
        for checkbox in self.parameters:
            rtn[checkbox.text()] = checkbox.isChecked()
        return rtn

    def apply_config(self, config_dict: dict):
        """Apply checked status contained in config_dict to all checkboxes."""
        for cbox in self.parameters:
            key = cbox.text()
            is_checked = config_dict.get(key, False)
            cbox.setChecked(is_checked)

    def get_selected_params(self) -> list[str]:
        """Return a list of all checked checkbox values."""
        return [cbox.text() for cbox in self.parameters if cbox.isChecked()]

    def set_checked_all(self, is_checked: bool):
        """Change checked status of all checkboxes."""
        for cbox in self.parameters:
            cbox.setChecked(is_checked)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = ParametersDialog()
    test.show()
    sys.exit(app.exec())
