from PyQt5.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QComboBox


class FilterDialog(QDialog):
    def __init__(self, parent=None, filter_list=None):
        super().__init__(parent)

        if filter_list is None:
            filter_list = []

        self.filter_list = QComboBox()
        self.filter_list.addItems(filter_list)
        self.input = QLineEdit(self)
        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.addButton(QDialogButtonBox.Cancel)

        layout = QFormLayout(self)
        layout.addRow("Filter:", self.filter_list)
        layout.addRow("Radius (px):", self.input)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def get_inputs(self):
        """Returns filter selection and input as strings."""
        return self.filter_list.currentText(), self.input.text()
