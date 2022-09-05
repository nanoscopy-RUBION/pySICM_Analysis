from PyQt6.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QComboBox


class FilterDialog(QDialog):
    """A small dialog window with a combobox for filter selection
    and a text field for radius input."""

    def __init__(self, parent=None, filter_list=None):
        super().__init__(parent)

        if filter_list is None:
            filter_list = []

        self.setWindowTitle("Select filter")
        self.filter_list = QComboBox()
        self.filter_list.addItems(filter_list)
        self.input = QLineEdit(self)
        self.input.setToolTip("Enter an integer for radius of the filter")
        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.ButtonRole.Ok)
        buttons.addButton(QDialogButtonBox.ButtonRole.Cancel)

        layout = QFormLayout(self)
        layout.addRow("Filter:", self.filter_list)
        layout.addRow("Radius (px):", self.input)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def get_inputs(self):
        """Returns filter selection and input as strings."""
        return self.filter_list.currentText(), self.input.text()
