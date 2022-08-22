"""
TODO add module documentation
"""
import traceback

import numpy as np
import sys
from os import listdir
from os.path import isfile, join

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QListWidget, QLabel, QAction, QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QIcon
from matplotlib import cm
from matplotlib.colors import ListedColormap

from ManipulateData import filter_average_temporal, filter_median_temporal, interpolate_cubic, level_data, \
    subtract_minimum, filter_average_spatial, filter_median_spatial, crop, transpose_data
from SICMViewerHelper import SICMDataFactory, ApproachCurve, ScanBackstepMode
from View import View

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

TITLE = "pySICM Analyzer (2022_08_22_1)"


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data."""

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class SecondaryWindow(QWidget):
    """
    This is a QWidget. It is used as a platform to create secondary
    windows for selecting or inputting options
    CURRENTLY UNUSED
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""

    # Variables used to
    currentItem = None
    currentData = None
    currentView = None
    current_x = None
    current_y = None
    old_x = None
    old_y = None
    clickCount = 0
    # Variables used to preserve
    itemList = []
    viewList = []
    dataList = []

    def __init__(self):
        super().__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.list_widget = QListWidget(self)
        self.canvas = GraphCanvas()
        self.init_ui()
        self.set_menus_enabled(False)

        # for testing click events
        self.last_change = None
        self.X = None
        self.Y = None

    def init_ui(self):
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()

        self.list_widget.currentItemChanged.connect(self.item_changed_event)
        action_exit = QtWidgets.QAction(QIcon('exit.png'), '&Exit', self)
        action_exit.triggered.connect(QtWidgets.qApp.quit)
        action_clear = QtWidgets.QAction('&Clear', self)
        action_clear.triggered.connect(self.menu_action_clear)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        layout.addWidget(self.list_widget, 2)
        layout.addWidget(self.canvas, 3)
        self.central_widget.setLayout(layout)

        action_import_single = QAction('&Import Files', self)
        action_import_single.triggered.connect(self.menu_action_import)
        action_import_multiple = QAction('&Import Directory', self)
        action_import_multiple.triggered.connect(self.menu_action_import_directory)

        action_export_file = QAction('&Export to file', self)
        action_export_file.triggered.connect(self.menu_action_export_file)
        action_export_bitmap = QAction('&As bitmap (png)', self)
        action_export_bitmap.triggered.connect(self.menu_action_export_bitmap)
        action_export_vector = QAction('&as vector (pdf)', self)
        action_export_vector.triggered.connect(self.menu_action_export_vector)

        file_menu.addAction(action_clear)
        file_menu.addSeparator()
        file_menu.addAction(action_import_single)
        file_menu.addAction(action_import_multiple)
        clipboard_menu = file_menu.addMenu('Export as image')
        clipboard_menu.addAction(action_export_bitmap)
        clipboard_menu.addAction(action_export_vector)
        file_menu.addAction(action_export_file)
        file_menu.addSeparator()
        file_menu.addAction(action_exit)

        self.action_toggle_axes = QAction('&Show axes', self)
        self.action_toggle_axes.setCheckable(True)
        self.action_toggle_axes.setChecked(True)
        self.action_toggle_axes.triggered.connect(self.menu_action_toggle_axes)

        action_view_restore = QAction('&Restore view', self)
        action_view_restore.triggered.connect(self.menu_action_view_restore)
        action_view_ratio = QAction('&Aspect ratio', self)
        action_view_ratio.triggered.connect(self.menu_action_view_ratio)
        action_view_surface = QAction('&Interpolate surface', self)
        action_view_surface.triggered.connect(self.menu_action_interpolate_view)
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_xlimits.triggered.connect(self.menu_action_view_xlimits)
        action_view_ylimits = QAction('&Adjust y limits', self)
        action_view_ylimits.triggered.connect(self.menu_action_view_ylimits)
        action_view_colormap = QAction('&Colormap', self)
        action_view_colormap.triggered.connect(self.menu_action_view_colormap)

        action_store_angles = QAction('Store viewing angles', self)
        action_store_angles.triggered.connect(self.store_viewing_angles)

        self.view_menu = menubar.addMenu("&View")
        self.view_menu.addAction(self.action_toggle_axes)
        self.view_menu.addAction(action_store_angles)
        self.view_menu.addAction(action_view_ratio)
        # view_menu.addAction(action_view_surface)
        self.view_menu.addAction(action_view_xlimits)
        self.view_menu.addAction(action_view_ylimits)
        self.view_menu.addAction(action_view_colormap)
        self.view_menu.addSeparator()
        self.view_menu.addAction(action_view_restore)

        action_data_crop = QAction('&Crop', self)
        action_data_crop.triggered.connect(self.menu_action_data_crop)
        action_data_default = QAction('&Apply default scale', self)
        # action_data_default.triggered.connect(self.menu_action_data_default)
        action_data_minimum = QAction('&Subtract minimum', self)
        action_data_minimum.triggered.connect(self.menu_action_data_minimum)
        action_data_transpose = QAction('&Transpose Z', self)
        action_data_transpose.triggered.connect(self.menu_action_data_transpose_z)
        action_data_median = QAction('&Temporal Median', self)
        action_data_median.triggered.connect(self.menu_action_data_median)
        action_data_average = QAction('&Temporal Average', self)
        action_data_average.triggered.connect(self.menu_action_data_average)
        action_data_smedian = QAction('&Spatial Median', self)
        action_data_smedian.triggered.connect(self.menu_action_data_smedian)
        action_data_saverage = QAction('&Spatial Average', self)
        action_data_saverage.triggered.connect(self.menu_action_data_saverage)
        action_data_plane = QAction('&Plane', self)
        #action_data_plane.triggered.connect(self.test_level_plane)
        action_data_plane.triggered.connect(self.menu_action_data_plane)
        action_data_paraboloid = QAction('&Paraboloid', self)
        action_data_paraboloid.triggered.connect(self.menu_action_data_paraboloid)
        action_data_line = QAction('&Linewise', self)
        # action_data_line.triggered.connect(self.menu_action_data_line)
        action_data_linemean = QAction('&Linewise (mean)', self)
        # action_data_linemean.triggered.connect(self.menu_action_data_linemean)
        action_data_liney = QAction('&Linewise Y', self)
        # action_data_liney.triggered.connect(self.menu_action_data_liney)
        action_data_poly = QAction('&polyXX', self)
        action_data_poly.triggered.connect(self.menu_action_data_poly)
        action_data_splines = QAction('&by cubic splines', self)
        action_data_splines.triggered.connect(self.menu_action_data_splines)
        action_data_neighbor = QAction('&by nearest neighbor', self)
        action_data_neighbor.triggered.connect(self.menu_action_data_neighbor)
        action_data_reset = QAction('&Reset data manipulations', self)
        action_data_reset.triggered.connect(self.menu_action_data_reset)

        self.data_menu = menubar.addMenu("&Manipulate data")
        simple_menu = self.data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(action_data_crop)
        simple_menu.addAction(action_data_default)
        simple_menu.addAction(action_data_minimum)
        simple_menu.addAction(action_data_transpose)
        filter_menu = self.data_menu.addMenu('Filter')
        filter_menu.addAction(action_data_median)
        filter_menu.addAction(action_data_average)
        filter_menu.addAction(action_data_smedian)
        filter_menu.addAction(action_data_saverage)
        flatten_menu = self.data_menu.addMenu('Leveling')
        flatten_menu.addAction(action_data_plane)
        flatten_menu.addAction(action_data_paraboloid)
        flatten_menu.addAction(action_data_line)
        flatten_menu.addAction(action_data_linemean)
        flatten_menu.addAction(action_data_liney)
        flatten_menu.addAction(action_data_poly)
        interpolation_menu = self.data_menu.addMenu('Interpolation')
        interpolation_menu.addAction(action_data_splines)
        interpolation_menu.addAction(action_data_neighbor)
        self.data_menu.addAction(action_data_reset)

        action_measure_dist = QAction('&Measure distance', self)
        action_measure_dist.triggered.connect(self.menu_action_measure_dist)
        action_measure_profile = QAction('&Measure profile', self)
        action_measure_profile.triggered.connect(self.menu_action_measure_profile)

        self.measure_menu = menubar.addMenu("&Measurements")
        self.measure_menu.addAction(action_measure_dist)
        self.measure_menu.addAction(action_measure_profile)

        self.properties_menu = menubar.addMenu("&Properties")

        self.about_menu = menubar.addMenu("&About")
        action_about = QAction('click test', self)
        action_about.triggered.connect(self.about)
        self.about_menu.addAction(action_about)

        self.setGeometry(700, 350, 800, 800)
        self.setWindowTitle(TITLE)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def set_menus_enabled(self, enable):
        self.view_menu.setEnabled(enable)
        self.data_menu.setEnabled(enable)
        self.measure_menu.setEnabled(enable)
        self.properties_menu.setEnabled(enable)
        self.about_menu.setEnabled(enable)

    def menu_action_import(self):
        """Opens a file dialog to choose sicm files."""
        files = self.import_files_dialog()
        self.add_files_to_list(files)

    def menu_action_import_directory(self):
        """Opens a file dialog to choose a directory."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        dirname = QFileDialog().getExistingDirectory(parent=self,
                                                     caption='Select Folder',
                                                     options=options
                                                     )
        if dirname:
            sicm_files = [join(dirname, f) for f in listdir(dirname) if (isfile(join(dirname, f)) and f.endswith('.sicm'))]
            self.add_files_to_list(sicm_files)
        else:
            self.statusBar().showMessage("No directory imported.")

    def import_files_dialog(self, directory=".."):
        """Opens a directory to import all .sicm files (Does not search subdirectories)."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filenames, _ = QFileDialog.getOpenFileNames(parent=self,
                                                    caption="Import pySICM Scan Files",
                                                    directory=directory,
                                                    filter="pySICM Files (*.sicm)",
                                                    options=options
                                                    )
        return filenames

    def add_files_to_list(self, files):
        """
        Adds file paths to the list widget.
        :param files: list of files
        """
        if files:
            if len(files) > 1:
                message_end = " files."
            else:
                message_end = " file."
            self.list_widget.addItems(files)
            self.set_menus_enabled(True)
            self.statusBar().showMessage("Imported " + str(len(files)) + message_end)
        else:
            self.statusBar().showMessage("No files imported.")

    def menu_action_export_file(self):
        """TODO implementation
        Exports the current view object as ... file.
        Need to think about the file format. .sicm might not be
        suitable after manipulating the data """
        # json to store metadata

        print("TODO: Export to file")

    def update_plots(self, view_data, sicm_data):
        """
        Redraws plots on the canvas of the MainWindow gui (the right side of the window). 
        If the data is from an approach curve, a single 2D plot will be displayed.
        If the data is from a backstep scan, a 3D plot . Plotting data and details are based upon the

        :param view_data: View object which contains the data and display settings for the graph
        :param sicm_data: TODO: rewrite so unnecessary
        """
        self.canvas.figure.clear()
        if isinstance(sicm_data, ScanBackstepMode):

            self.canvas.axes = self.canvas.figure.add_subplot(2, 1, 1, projection='3d')
            plot = self.canvas.axes.plot_surface(*view_data.get_modified_data(), cmap=view_data.color_map)

            self.canvas.figure.get_axes()[0].azim = self.currentView.azim
            self.canvas.figure.get_axes()[0].elev = self.currentView.elev
            self.canvas.figure.get_axes()[0].proj_type = 'ortho'
            self.canvas.axes.axis(view_data.axes_shown)
            self.canvas.figure.colorbar(plot)

            ax = self.canvas.axes = self.canvas.figure.add_subplot(2, 1, 2)
            # use pcolormesh for scalable pixelmaps
            #img = self.canvas.axes.pcolormesh(view_data.z_data, cmap=view_data.color_map)
            img = self.canvas.axes.imshow(view_data.z_data, cmap=view_data.color_map)
            self.canvas.axes.axis(view_data.axes_shown)
            self.canvas.figure.colorbar(img)

        if isinstance(sicm_data, ApproachCurve):
            self.canvas.axes = self.canvas.figure.add_subplot(111)
            self.canvas.axes.plot(*view_data.get_modified_data())
            self.canvas.axes.axis(view_data.axes_shown)

        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.statusBar().showMessage("Max: %s  Min: %s" % (
            str(np.max(self.currentView.get_z_data())),
            str(np.min(self.currentView.get_z_data()))
        ))

    def menu_action_clear(self):
        """Removes all items from list widget and disables menues."""
        self.list_widget.clear()
        self.currentView = None
        self.currentData = None
        self.set_menus_enabled(False)
        self.statusBar().showMessage("Files removed from the list.")

    def item_changed_event(self, item):
        """Updates the figure canvas when list selection has changed.
        """
        if item:
            self.action_toggle_axes.setEnabled(True)
            self.currentItem = item
            if self.currentItem not in self.itemList:
                self.itemList.append(item)
                sicm_data = SICMDataFactory().get_sicm_data(item.text())
                self.currentData = sicm_data
                data_view = View(sicm_data)
                self.currentView = data_view
                self.viewList.append(self.currentView)
                self.dataList.append(self.currentData)
            else:
                self.currentView = self.viewList[self.itemList.index(self.currentItem)]
                self.currentData = self.dataList[self.itemList.index(self.currentItem)]
            self.action_toggle_axes.setChecked(self.currentView.axes_shown)
            self.canvas.axes.set_title(item.text())
            self.update_plots(self.currentView, self.currentData)
        else:
            self.action_toggle_axes.setEnabled(False)

    def _figure_save_configuration(self):
        """Helper function for setting up which part
        of the plot should be saves."""
        fig = self.canvas.figure
        ax = fig.get_axes()[0]
        # Save just the portion _inside_ the second axis's boundaries
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig('ax2_figure.png', bbox_inches=extent)

        # Pad the saved area by 10% in the x-direction and 20% in the y-direction
        fig.savefig('ax2_figure_expanded.png', bbox_inches=extent.expanded(1.1, 1.2))


    def menu_action_export_bitmap(self):
        # TODO filedialog for saving

        self.canvas.figure.savefig(fname="testfigure.png", format="png")
        self._figure_save_configuration()
        print("TODO: Export as bitmap")

    def menu_action_export_vector(self):
        print("TODO: Export as pdf")

    def menu_action_view_colormap(self):
        """Opens a dialog to select a predefined
        colormap or to create a custome one.
        """
        # TODO open a dialog

        self.currentView.change_color_map(self._get_new_color_map())
        self.update_plots(self.currentView, self.currentData)

    def _get_new_color_map(self):
        """Color map creation should be placed in a
        seperate class.
        """
        viridis = cm.get_cmap('viridis', 256)
        newcolors = viridis(np.linspace(0, 1, 256))
        pink = np.array([10 / 256, 10 / 256, 10 / 256, 1])
        newcolors[:25, :] = pink
        newmap = ListedColormap(newcolors)


        N = 256
        vals = np.ones((N, 4))


        #custom_map = ListedColormap(cus_colors)
        return cm.get_cmap('viridis', 256)


    def menu_action_toggle_axes(self):
        """Shows or hides axes in figures.
        """
        self.currentView.toggle_axes()
        self.update_plots(self.currentView, self.currentData)

    def menu_action_view_xlimits(self):
        '''win = SecondaryWindow()
        win.nameLabel = QLabel(self)
        win.nameLabel.setText('Name:')
        win.line = QLineEdit(self)

        win.line.move(80, 20)
        win.line.resize(200, 32)
        win.nameLabel.move(20, 20)'''
        limits, success = QtWidgets.QInputDialog.getText(
            self, 'X Limit Input', 'Please enter the desired x limits separated by a space')
        limits = [float(f) for f in limits.split()]
        self.currentView.set_xlims(limits)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_view_ylimits(self):
        limits, success = QtWidgets.QInputDialog.getText(
            self, 'Y Limit Input', 'Please enter the desired y limits separated by a space')
        limits = [float(f) for f in limits.split()]
        self.currentView.set_ylims(limits)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_view_ratio(self):
        ratio, success = QtWidgets.QInputDialog.getText(
            self, 'Ratio Input', 'Please enter the numerical ratio, \'equal\', or \'auto\'')
        if self.currentView.set_aspect(ratio):
            self.update_plots(self.currentView, self.currentData)
        else:
            # TODO Implement error message to user
            return 0

    def menu_action_interpolate_view(self):
        print("TODO: interpolate view")

    def menu_action_view_restore(self):
        try:
            self.currentView.restore()
            self.update_plots(self.currentView, self.currentData)
            self.action_toggle_axes.setChecked(True)
        except Exception as e:
            print(f'No view to restore')
            print(str(e))
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    def menu_action_data_crop(self):
        xlimits, success = QtWidgets.QInputDialog.getText(
            self, 'X Crop Dimensions', 'Please enter the desired x dimensions separated by a space')
        xlimits = [int(f) for f in xlimits.split()]
        ylimits, success = QtWidgets.QInputDialog.getText(
            self, 'Y Crop Dimensions', 'Please enter the desired y dimensions separated by a space')
        ylimits = [int(f) for f in ylimits.split()]
        limits = np.array((xlimits, ylimits))
        self.currentView.set_data(crop(self.currentView.get_modified_data(), limits))
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_transpose_z(self):
        """Transposes z data of all measurements except ApproachCurves."""
        if not isinstance(self.currentData, ApproachCurve):
            self.currentView.set_z_data(transpose_data(self.currentView.z_data))
            self.update_plots(self.currentView, self.currentData)

    def menu_action_data_minimum(self):
        self.currentView.set_z_data(subtract_minimum(self.currentView.get_z_data()))
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_average(self):
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Average)', 'Please enter the number of pixels to use on either side')
        self.currentView.set_z_data(filter_average_temporal(self.currentView.get_z_data(), int(pixels)))
        self.currentView.make_plot(self.canvas.axes)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_median(self):
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Median)', 'Please enter the number of pixels to use on either side')
        self.currentView.set_z_data(filter_median_temporal(self.currentView.get_z_data(), int(pixels)))
        self.currentView.make_plot(self.canvas.axes)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_saverage(self):
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Average)', 'Please enter the number of pixels around the center to use')
        self.currentView.set_z_data(filter_average_spatial(self.currentView.get_z_data(), int(pixels)))
        self.currentView.make_plot(self.canvas.axes)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_smedian(self):
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Median)', 'Please enter the number of pixels around the center to use')
        self.currentView.set_z_data(filter_median_spatial(self.currentView.get_z_data(), int(pixels)))
        self.currentView.make_plot(self.canvas.axes)
        self.update_plots(self.currentView, self.currentData)

    def menu_action_data_plane(self):
        test = level_data(self.currentView, method='plane').transpose()
        # print(test)
        # print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)

    def menu_action_data_paraboloid(self):
        test = level_data(self.currentView, method='paraboloid').transpose()
        # print(test)
        # print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)

    def menu_action_data_poly(self):
        test = level_data(self.currentView, method='2Dpoly').transpose()
        # print(test)
        # print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)

    def menu_action_data_splines(self):
        # TODO Determine intended usage of this
        # self.currentView.set_z_data(interpolate_cubic(self.currentView).T)
        # self.update_plots(self.currentView,self.currentData)
        # self.currentView.make_plot(self.canvas.axes)
        # interpolate_cubic(self.currentView)
        # print(f)
        # plt.imshow(interpolate_cubic(self.currentView).T, extent=(0,1,0,1))
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Interpolation (Cubic Spline)', 'Please enter the number of pixels interpolate per')
        new_z, new_x, new_y = interpolate_cubic(self.currentView, int(pixels), method='cubic')  # .T
        # print(test)
        # print(test.shape)
        self.currentView.set_x_data(new_x)
        self.currentView.set_y_data(new_y)
        self.currentView.set_z_data(new_z)
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)
        return

    def menu_action_data_neighbor(self):
        # TODO Determine intended usage of this
        # self.currentView.set_z_data(interpolate_cubic(self.currentView).T)
        # self.update_plots(self.currentView,self.currentData)
        # self.currentView.make_plot(self.canvas.axes)
        # interpolate_cubic(self.currentView)
        # print(f)
        # plt.imshow(interpolate_cubic(self.currentView).T, extent=(0,1,0,1))
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Interpolation (Cubic Spline)', 'Please enter the number of pixels interpolate per')
        new_z, new_x, new_y = interpolate_cubic(self.currentView, int(pixels), method='nearest')  # .T
        # print(test)
        # print(test.shape)
        self.currentView.set_x_data(new_x)
        self.currentView.set_y_data(new_y)
        self.currentView.set_z_data(new_z)
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)
        return

    def menu_action_data_reset(self):
        self.currentView.reset_data()
        self.update_plots(self.currentView, self.currentData)
        self.currentView.make_plot(self.canvas.axes)

    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def get_old_x(self):
        return self.old_x

    def get_old_y(self):
        return self.old_y
    # def item_activated_event(self):#,item):
    # self.currentItem = item
    # print(self.list_widget.selectedItems)

    # def menu_action_clear(self):
    # """Removes all items from list widget."""
    # self.list_widget.clear()
    # self.statusBar().showMessage("Files removed from the list.")

    def store_viewing_angles(self):
        """Stores the two viewing angles in the View object.
        This is only possible for scans that are not of the type
        ApproachCurve.
        """
        try:
            azim = self.canvas.figure.get_axes()[0].azim
            elev = self.canvas.figure.get_axes()[0].elev
            self.currentView.set_viewing_angles(azim, elev)
        except AttributeError:
            self.statusBar().showMessage("ApproachCurves have no viewing angles.")
            self.currentView.set_viewing_angles()

    def menu_action_measure_dist(self):
        print("TODO Measure dist")

    def menu_action_measure_profile(self):
        print("TODO Measure profile")

    def about(self):
        if len(self.canvas.figure.get_axes()) > 1:
            self.cid = self.canvas.figure.canvas.mpl_connect('button_press_event', self.click_on_raster_image)

    def click_on_raster_image(self, event):
        """A test function for getting the correct pixel after clicking on it.

        """
        axes = event.canvas.figure.get_axes()[0]
        if event.inaxes == axes:
            print("oben")
        else:
            print("unten")
            print("x: %s, y: %s" % (event.xdata, event.ydata))
            x = int(event.xdata + 0.5)
            y = int(event.ydata + 0.5)
            if not self.last_change:
                self.X = x
                self.Y = y
                self.last_change = self.currentView.z_data[y, x]
                self.currentView.z_data[y, x] = 0.0
                self.update_plots(self.currentView, self.currentData)
            else:
                print("Last: %s" % self.last_change)
                self.currentView.z_data[self.Y, self.X] = self.last_change
                self.last_change = self.currentView.z_data[y, x]
                self.currentView.z_data[y, x] = 0.0
                self.X = x
                self.Y = y
                self.update_plots(self.currentView, self.currentData)
                print(self.X, self.Y)
            print(self.currentView.z_data[x, y])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = MainWindow()
    sys.exit(app.exec())
