from PyQt6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from matplotlib import cm

COLOR_MAPS = {
    "AFM hot": cm.afmhot,
    "Bone": cm.bone,
    "Cividis": cm.cividis,
    "Greys": cm.gray,
    "Hot (für Dilan)": cm.hot,
    "Jet": cm.jet,
    "Jet (reverse)": cm.jet_r,
    "Summer": cm.summer,
    "Summer (reverse)": cm.summer_r,
    "Viridis": cm.viridis
}


class ColorMapDialog(QWidget):
    """
    This widget will appear as a free-floating window if
    it has no parent.
    """

    def __init__(self, controller, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Color Map Chooser")
        self.setFixedSize(300, 150)
        self.controller = controller

        layout = QVBoxLayout()
        self.setLayout(layout)

        hlayout = QHBoxLayout()
        button_box = QWidget()
        button_box.setLayout(hlayout)

        self.cmap_combobox = QComboBox()
        self.cmap_combobox.addItems(COLOR_MAPS.keys())

        self.button_apply = QPushButton("Apply")

        layout.addWidget(self.cmap_combobox)
        layout.addWidget(button_box)
        hlayout.addWidget(self.button_apply)

        self.button_apply.clicked.connect(self.apply_color_map_selection)

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()

    def apply_color_map_selection(self):
        self._apply_color_map_to_view(self.controller.view, COLOR_MAPS.get(self.cmap_combobox.currentText()))
        self.controller.update_figures_and_status()

    def _apply_color_map_to_view(self, view, cmap):
        view.color_map = cmap
