from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QItemSelectionModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QWidget, QTableWidgetItem, QAbstractItemView, QTableView


class ROIsDialog(QWidget):
    """

    """

    def __init__(self, controller, parent=None):
        super().__init__()
        self.parent = parent
        self.controller = controller

        self.resize(520, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.widget_6 = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_6)

        self.grid_widget = QtWidgets.QWidget(self.widget_6)
        self.gridLayout = QtWidgets.QGridLayout(self.grid_widget)

        self.x_label = QtWidgets.QLabel("X:", self.grid_widget)
        self.x_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.x_slider = QtWidgets.QSlider(self.grid_widget)
        self.x_slider.setMinimumSize(QtCore.QSize(150, 30))
        self.x_slider.setMaximumSize(QtCore.QSize(150, 30))
        self.x_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_x_down = QtWidgets.QPushButton("<", self.grid_widget)
        self.button_x_down.setMinimumSize(QtCore.QSize(30, 30))
        self.button_x_down.setMaximumSize(QtCore.QSize(30, 30))
        self.button_x_up = QtWidgets.QPushButton(">", self.grid_widget)
        self.button_x_up.setMinimumSize(QtCore.QSize(30, 30))
        self.button_x_up.setMaximumSize(QtCore.QSize(30, 30))
        self.text_x = QtWidgets.QLineEdit("was", self.grid_widget)
        self.text_x.setMaximumSize(QtCore.QSize(60, 30))

        self.y_label = QtWidgets.QLabel("Y:", self.grid_widget)
        self.y_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.y_slider = QtWidgets.QSlider(self.grid_widget)
        self.y_slider.setMinimumSize(QtCore.QSize(150, 30))
        self.y_slider.setMaximumSize(QtCore.QSize(150, 30))
        self.y_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_y_down = QtWidgets.QPushButton("<", self.grid_widget)
        self.button_y_down.setMinimumSize(QtCore.QSize(30, 30))
        self.button_y_down.setMaximumSize(QtCore.QSize(30, 30))
        self.button_y_up = QtWidgets.QPushButton(">", self.grid_widget)
        self.button_y_up.setMinimumSize(QtCore.QSize(30, 30))
        self.button_y_up.setMaximumSize(QtCore.QSize(30, 30))
        self.text_y = QtWidgets.QLineEdit("Y", self.grid_widget)
        self.text_y.setMaximumSize(QtCore.QSize(60, 30))

        self.width_label = QtWidgets.QLabel("Width:", self.grid_widget)
        self.width_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.width_slider = QtWidgets.QSlider(self.grid_widget)
        self.width_slider.setMinimumSize(QtCore.QSize(150, 30))
        self.width_slider.setMaximumSize(QtCore.QSize(150, 30))
        self.width_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_width_down = QtWidgets.QPushButton("<", self.grid_widget)
        self.button_width_down.setMinimumSize(QtCore.QSize(30, 30))
        self.button_width_down.setMaximumSize(QtCore.QSize(30, 30))
        self.button_width_up = QtWidgets.QPushButton(">", self.grid_widget)
        self.button_width_up.setMinimumSize(QtCore.QSize(30, 30))
        self.button_width_up.setMaximumSize(QtCore.QSize(30, 30))
        self.text_width = QtWidgets.QLineEdit("width", self.grid_widget)
        self.text_width.setMaximumSize(QtCore.QSize(60, 30))

        self.height_label = QtWidgets.QLabel("Height:", self.grid_widget)
        self.height_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.height_slider = QtWidgets.QSlider(self.grid_widget)
        self.height_slider.setMinimumSize(QtCore.QSize(150, 30))
        self.height_slider.setMaximumSize(QtCore.QSize(150, 30))
        self.height_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_height_down = QtWidgets.QPushButton("<", self.grid_widget)
        self.button_height_down.setMinimumSize(QtCore.QSize(30, 30))
        self.button_height_down.setMaximumSize(QtCore.QSize(30, 30))
        self.button_height_up = QtWidgets.QPushButton(">", self.grid_widget)
        self.button_height_up.setMinimumSize(QtCore.QSize(30, 30))
        self.button_height_up.setMaximumSize(QtCore.QSize(30, 30))
        self.text_height = QtWidgets.QLineEdit("wo", self.grid_widget)
        self.text_height.setMaximumSize(QtCore.QSize(60, 30))

        # layout widgets in grid
        self.gridLayout.addWidget(self.text_y, 2, 10, 1, 1)
        self.gridLayout.addWidget(self.button_y_up, 2, 5, 1, 1)
        self.gridLayout.addWidget(self.x_label, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.gridLayout.addWidget(self.button_width_down, 5, 4, 1, 1)
        self.gridLayout.addWidget(self.text_width, 5, 10, 1, 1)
        self.gridLayout.addWidget(self.button_x_down, 1, 4, 1, 1)
        self.gridLayout.addWidget(self.x_slider, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.button_y_down, 2, 4, 1, 1)
        self.gridLayout.addWidget(self.button_x_up, 1, 5, 1, 1)
        self.gridLayout.addWidget(self.button_width_up, 5, 5, 1, 1)
        self.gridLayout.addWidget(self.button_height_up, 6, 5, 1, 1)
        self.gridLayout.addWidget(self.width_slider, 5, 2, 1, 1)
        self.gridLayout.addWidget(self.text_x, 1, 10, 1, 1)
        self.gridLayout.addWidget(self.y_slider, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.y_label, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.gridLayout.addWidget(self.text_height, 6, 10, 1, 1)
        self.gridLayout.addWidget(self.height_slider, 6, 2, 1, 1)
        self.gridLayout.addWidget(self.button_height_down, 6, 4, 1, 1)
        self.gridLayout.addWidget(self.width_label, 5, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.gridLayout.addWidget(self.height_label, 6, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)

        self.horizontalLayout.addWidget(self.grid_widget)
        self.widget_7 = QtWidgets.QWidget(self.widget_6)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_7)

        self.button_apply = QtWidgets.QPushButton("Add/Edit", self.widget_7)
        self.pushButton_10 = QtWidgets.QPushButton("Remove", self.widget_7)
        self.verticalLayout_2.addWidget(self.button_apply)


        self.verticalLayout_2.addWidget(self.pushButton_10)
        self.horizontalLayout.addWidget(self.widget_7)
        spacerItem = QtWidgets.QSpacerItem(96, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget_6)
        self.widget_4 = QtWidgets.QWidget(self)

        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)

        self.verticalLayout.addWidget(self.widget_4)
        self.widget_3 = QtWidgets.QWidget(self)

        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)

        self.verticalLayout.addWidget(self.widget_3)
        self.widget_2 = QtWidgets.QWidget(self)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)

        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self)

        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.widget)
        self.model_rois = QStandardItemModel()

        self.table_rois = QtWidgets.QTableWidget(3, 5)
        self.table_rois.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_rois.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.table_rois.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_rois.setHorizontalHeaderLabels(["ROI", "X", "Y", "Width", "Height"])

        self.verticalLayout.addWidget(self.table_rois)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)
        self.table_rois.setItem(0, 0, QTableWidgetItem("ROI 1"))
        self.table_rois.setItem(1, 0, QTableWidgetItem("ROI 2"))
        self.table_rois.setItem(2, 0, QTableWidgetItem("ROI 3"))
        self.table_rois.setItem(0, 1, QTableWidgetItem("10"))
        self.table_rois.setItem(1, 1, QTableWidgetItem("2"))
        self.table_rois.setItem(2, 1, QTableWidgetItem("53"))
        self.table_rois.setItem(0, 2, QTableWidgetItem("6"))
        self.table_rois.setItem(1, 2, QTableWidgetItem("8"))
        self.table_rois.setItem(2, 2, QTableWidgetItem("13"))
        self.table_rois.setItem(0, 3, QTableWidgetItem("10"))
        self.table_rois.setItem(1, 3, QTableWidgetItem("20"))
        self.table_rois.setItem(2, 3, QTableWidgetItem("30"))
        self.table_rois.setItem(0, 4, QTableWidgetItem("10"))
        self.table_rois.setItem(1, 4, QTableWidgetItem("20"))
        self.table_rois.setItem(2, 4, QTableWidgetItem("30"))


        #QtCore.QMetaObject.connectSlotsByName(Form)

    def open_window(self):
        if self.isVisible():
            self.hide()
        else:
            geometry = self.geometry()
            geometry.moveCenter(self.parent.geometry().center())
            self.setGeometry(geometry)
            self.show()



