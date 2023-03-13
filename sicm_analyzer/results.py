from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QPlainTextEdit, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QApplication, QSizePolicy, QMenu

from sicm_analyzer.sicm_data import SICMdata
from sicm_analyzer.measurements import get_roughness
import numpy as np


class SingleResultsWindow(QWidget):
    """
    This window will show the results of one sicm data object.

    At the moment, it will only display roughness and some information
    about the polynomial fit used to calculate the roughness.
    """

    def __init__(self, data: SICMdata, parent=None, size=(500, 600)):
        super().__init__()
        width = size[0]
        height = size[1]
        self.parent = parent
        self.setWindowTitle("Results of current selection")
        self.setFixedSize(width, height)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.text.insertPlainText(self.get_results(data))

        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(self.close)
        layout.addWidget(self.button_close)

    def get_results(self, data: SICMdata):
        roughness = get_roughness(data)
        text = ""
        text = text + f"Roughness: {roughness} µm\n"
        text = text + f"Minimum value: {np.min(data.z)} µm\n"
        text = text + f"Maximum value: {np.max(data.z)} µm\n"
        text = text + "\n\n"
        text = text + "Fit Results:\n"
        text = text + str(data.fit_results)

        return text

    def update_results(self, data: SICMdata):
        self.text.clear()
        self.text.insertPlainText(self.get_results(data))


class TableResultsWindow(QWidget):
    """
    This window will show the results of a set of multiple scan objects.
    The scan objects' data are passed as a dict structured as follows:

        data = {
            "col_name": [row1, row2, row3, ...],
            ...
        }

    For example:

        data = {
            "file": ["/path/to/file1.sicm", "/path/to/file2.sicm"],
            "max_height": [3.123124234, 6.435345345],
            "n_pixels": [1000, 90]
        }
    """

    def __init__(self, data: dict[str, list[int | str | float]], parent=None):
        super().__init__()

        self.parent = parent
        self.setWindowTitle("Results of all checked files")

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        rows = len(data.keys())
        cols = len(data["scan"])
        self.table = QTableWidget(cols, rows)
        self.table.setAlternatingRowColors(True)
        self.fill_table(data)
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(self.close)

        self.table.sizeHint()
        layout.addWidget(self.button_close)
        layout.expandingDirections()

        # context menu
        self.context_menu = QMenu(self)
        action_cp_table_clipboard = self.context_menu.addAction("Copy table to clipboard")
        action_cp_selection_clipboard = self.context_menu.addAction("Copy selection to clipboard")

        action_cp_table_clipboard.triggered.connect(self.copy_table_to_clipboard)
        action_cp_selection_clipboard.triggered.connect(self.copy_selection_to_clipboard)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        self.context_menu.exec(event.globalPos())

    def fill_table(self, data: dict[str, list[int | str | float]]):
        """Fills the table with data."""
        headers = []
        for n, key in enumerate(data.keys()):
            headers.append(key)
            for m, item in enumerate(data[key]):
                table_item = QTableWidgetItem(str(item))
                self.table.setItem(m, n, table_item)
        self.table.setHorizontalHeaderLabels(headers)

    def copy_table_to_clipboard(self):
        if self.table.rowCount() > 0:
            rows = self.table.rowCount()
            columns = self.table.columnCount()
            lines = []
            for r in range(rows):
                line = []
                for c in range(columns):
                    line.append(str(self.table.item(r, c).text()))
                lines.append(";".join(line))

            QApplication.clipboard().setText("\n".join(lines))
        else:
            self.parent.display_status_bar_message("No data in table.")

    def copy_selection_to_clipboard(self):
        r = self.table.selectedIndexes()
        c = []
        if len(r) > 0:

            s = []
            row = r[0].row()
            for i in r:
                if i.row() == row:
                    s.append(str(i.data()))
                    continue
                c.append(";".join(s))
                s = []
                row = i.row()
                s.append(str(i.data()))
            c.append(";".join(s))

        QApplication.clipboard().setText("\n".join(c))

