from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
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
        self.setFixedSize(300, 150)
        self.controller = controller
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        v_layout = QVBoxLayout()
        button_box = QWidget()
        button_box.setLayout(v_layout)

        self.cmap_combobox = QComboBox()
        self.cmap_combobox.addItems(COLOR_MAPS.keys())

        self.button_apply = QPushButton("Apply to selected")
        self.button_apply_to_checked = QPushButton("Apply to checked")
        self.button_apply_to_all = QPushButton("Apply to all")

        layout.addWidget(self.cmap_combobox)
        layout.addWidget(button_box)
        v_layout.addWidget(self.button_apply)
        v_layout.addWidget(self.button_apply_to_checked)
        v_layout.addWidget(self.button_apply_to_all)

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
