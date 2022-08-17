import numpy as np
import PyQt5 as pqt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ManipulateData import filter_average_temporal, filter_median_temporal, interpolate_cubic, level_data, subtract_minimum, filter_average_spatial, filter_median_spatial, crop
from SICMViewerHelper import SICMDataFactory, ApproachCurve, ScanBackstepMode
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from View import View
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QLineEdit, QLabel

import sys
from os import listdir
from os.path import isfile, join

"""
TODO add documentation
"""


import matplotlib

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QListWidget
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')
TITLE = "pySICM Viewer (2022_05_20_1)"


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
    """Main window of the application. This"""


    #Variables used to 
    currentItem = None
    currentData = None
    currentView = None
    current_x = None
    current_y = None
    old_x = None
    old_y = None
    clickCount = 0
    #Variables used to preserve 
    itemList = []
    viewList = []
    dataList = []
    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QWidget(self)
        self.list_widget = QListWidget(self)
        self.canvas = GraphCanvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.hide()
        self.canvas.mousePressEvent = self.getPos
        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()

        self.list_widget.currentItemChanged.connect(self.item_changed_event)
        #self.list_widget.itemActivated.connect(self.item_activated_event)
        #self.list_widget.itemSelectionChanged.connect(self.item_activated_event)
        action_exit = QtWidgets.QAction(QIcon('exit.png'), '&Exit', self)
        action_exit.triggered.connect(QtWidgets.qApp.quit)
        action_import = QtWidgets.QAction(QIcon('open.png'), '&Import', self)
        action_import.triggered.connect(self.menu_action_import)
        action_clear = QtWidgets.QAction('&Clear', self)
        action_clear.triggered.connect(self.menu_action_clear)

        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(action_clear)
        file_menu.addAction(action_import)
        file_menu.addAction(action_exit)

        layout.addWidget(self.list_widget, 2)
        layout.addWidget(self.canvas, 3)
        self.central_widget.setLayout(layout)


        #action_exit = QAction(QIcon('exit.png'), '&Exit', self)
        #action_exit.triggered.connect(qApp.quit)
        #action_import = QAction(QIcon('open.png'), '&Import', self)
        #action_import.triggered.connect(self.menu_action_import)
        #action_clear = QAction('&Clear', self)
        #action_clear.triggered.connect(self.menu_action_clear)

        #file_menu = menubar.addMenu("&File")
        #file_menu.addAction(action_clear)
        #file_menu.addAction(action_import)
        #file_menu.addAction(action_exit)

        action_import_single = QAction('&Import Files', self)
        action_import_single.triggered.connect(self.menu_action_import)
        action_import_multiple = QAction('&Import Directory', self)
        action_import_multiple.triggered.connect(self.menu_action_import_directory)

        import_menu = menubar.addMenu("&Import")
        import_menu.addAction(action_import_single)
        import_menu.addAction(action_import_multiple)

        action_export_file = QAction('&To file', self)
        #action_export_file.triggered.connect(self.menu_action_export_file)
        action_export_bitmap = QAction('&As bitmap (png)', self)
        action_export_bitmap.triggered.connect(self.menu_action_export_bitmap)
        action_export_vector = QAction('&as vector (pdf)', self)
        action_export_vector.triggered.connect(self.menu_action_export_vector)

        export_menu = menubar.addMenu("&Export")
        clipboard_menu = export_menu.addMenu('As image')
        clipboard_menu.addAction(action_export_bitmap)
        clipboard_menu.addAction(action_export_vector)
        export_menu.addAction(action_export_file)

        action_plot_rotate = QAction('&Rotate', self) #TODO implement as checkbox
        #action_plot_rotate.triggered.connect(self.menu_action_plot_rotate)
        action_plot_rotate.setCheckable(True)
        action_plot_pan = QAction('&Pan', self)
        action_plot_pan.triggered.connect(self.menu_action_plot_pan)
        action_plot_zoom = QAction('&Zoom', self)
        action_plot_zoom.triggered.connect(self.menu_action_plot_zoom)
        action_plot_reset = QAction('&Reset', self)
        action_plot_reset.triggered.connect(self.menu_action_plot_reset)


        plot_menu = menubar.addMenu("&Plot interaction")
        plot_menu.addAction(action_plot_rotate)
        plot_menu.addAction(action_plot_pan)
        plot_menu.addAction(action_plot_zoom)
        plot_menu.addAction(action_plot_reset)

        action_view_content = QAction('&Hide axis content', self)
        action_view_content.setCheckable(True)
        action_view_content.triggered.connect(self.menu_action_view_content)
        #action_view_axes = QAction('&Hide axes when updated', self)
        #action_view_axes.setCheckable(True)
        #action_view_axes.triggered.connect(self.menu_action_view_axes)
        action_view_restore = QAction('&Restore view', self)
        action_view_restore.triggered.connect(self.menu_action_view_restore)
        #action_view_mode = QAction('&Mode', self)
        #action_view_mode.triggered.connect(self.menu_action_view_mode)
        action_view_ratio = QAction('&Aspect ratio', self)
        action_view_ratio.triggered.connect(self.menu_action_view_ratio)
        #action_view_surface = QAction('&Interpolate surface', self)
        #action_view_surface.triggered.connect(self.menu_action_view_surface)
        action_view_xlimits = QAction('&Adjust x limits', self)
        action_view_xlimits.triggered.connect(self.menu_action_view_xlimits)
        action_view_ylimits = QAction('&Adjust y limits', self)
        action_view_ylimits.triggered.connect(self.menu_action_view_ylimits)
        #action_view_colormap = QAction('&Colormap', self)
        #action_view_colormap.triggered.connect(self.menu_action_view_colormap)

        view_menu = menubar.addMenu("&View")
        view_menu.addAction(action_view_content)
        #view_menu.addAction(action_view_axes)
        view_menu.addAction(action_view_restore)
        #view_menu.addAction(action_view_mode)
        view_menu.addAction(action_view_ratio)
        #view_menu.addAction(action_view_surface)
        view_menu.addAction(action_view_xlimits)
        view_menu.addAction(action_view_ylimits)
        #view_menu.addAction(action_view_colormap)

        action_data_crop = QAction('&Crop', self)
        action_data_crop.triggered.connect(self.menu_action_data_crop)
        action_data_default = QAction('&Apply default scale', self)
        #action_data_default.triggered.connect(self.menu_action_data_default)
        action_data_minimum = QAction('&Subtract minimum', self)
        action_data_minimum.triggered.connect(self.menu_action_data_minimum)
        action_data_transpose = QAction('&Transpose Z', self)
        #action_data_transpose.triggered.connect(self.menu_action_data_transpose)
        action_data_median = QAction('&Temporal Median', self)
        action_data_median.triggered.connect(self.menu_action_data_median)
        action_data_average = QAction('&Temporal Average', self)
        action_data_average.triggered.connect(self.menu_action_data_average)
        action_data_smedian = QAction('&Spatial Median', self)
        action_data_smedian.triggered.connect(self.menu_action_data_smedian)
        action_data_saverage = QAction('&Spatial Average', self)
        action_data_saverage.triggered.connect(self.menu_action_data_saverage)
        action_data_plane = QAction('&Plane', self)
        action_data_plane.triggered.connect(self.menu_action_data_plane)
        action_data_paraboloid = QAction('&Paraboloid', self)
        action_data_paraboloid.triggered.connect(self.menu_action_data_paraboloid)
        action_data_line = QAction('&Linewise', self)
        #action_data_line.triggered.connect(self.menu_action_data_line)
        action_data_linemean = QAction('&Linewise (mean)', self)
        #action_data_linemean.triggered.connect(self.menu_action_data_linemean)
        action_data_liney = QAction('&Linewise Y', self)
        #action_data_liney.triggered.connect(self.menu_action_data_liney)
        action_data_poly = QAction('&polyXX', self)
        action_data_poly.triggered.connect(self.menu_action_data_poly)
        action_data_splines = QAction('&by cubic splines', self)
        action_data_splines.triggered.connect(self.menu_action_data_splines)
        action_data_neighbor = QAction('&by nearest neighbor', self)
        action_data_neighbor.triggered.connect(self.menu_action_data_neighbor)
        action_data_reset = QAction('&Reset data manipulations', self)
        action_data_reset.triggered.connect(self.menu_action_data_reset)

        data_menu = menubar.addMenu("&Manipulate data")
        simple_menu = data_menu.addMenu('Simple Manipulations')
        simple_menu.addAction(action_data_crop)
        simple_menu.addAction(action_data_default)
        simple_menu.addAction(action_data_minimum)
        simple_menu.addAction(action_data_transpose)
        filter_menu = data_menu.addMenu('Filter')
        filter_menu.addAction(action_data_median)
        filter_menu.addAction(action_data_average)
        filter_menu.addAction(action_data_smedian)
        filter_menu.addAction(action_data_saverage)
        flatten_menu = data_menu.addMenu('Leveling')
        flatten_menu.addAction(action_data_plane)
        flatten_menu.addAction(action_data_paraboloid)
        flatten_menu.addAction(action_data_line)
        flatten_menu.addAction(action_data_linemean)
        flatten_menu.addAction(action_data_liney)
        flatten_menu.addAction(action_data_poly)
        interpolation_menu = data_menu.addMenu('Interpolation')
        interpolation_menu.addAction(action_data_splines)
        interpolation_menu.addAction(action_data_neighbor)
        data_menu.addAction(action_data_reset)

        action_measure_dist = QAction('&Measure distance', self)
        #action_measure_dist.triggered.connect(self.menu_action_measure_dist)
        action_measure_profile = QAction('&Measure profile', self)
        #action_measure_profile.triggered.connect(self.menu_action_measure_profile)

        measure_menu = menubar.addMenu("&Measurements")
        measure_menu.addAction(action_measure_dist)
        measure_menu.addAction(action_measure_profile)

        properties_menu = menubar.addMenu("&Properties")

        about_menu = menubar.addMenu("&About")

        self.setGeometry(700, 350, 800, 800)
        self.setWindowTitle('Submenu')
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(300, 300)
        self.show()

    def menu_action_import(self):
        """TODO add doc string"""
        files = self.import_files_dialog()
        if files:
            self.add_files_to_list(files)
        else:
            self.statusBar().showMessage("No files imported.")

    def update_plots(self,view_data,sicm_data):
        """
        Update Plots
        Redraws plots on the canvas of the MainWindow gui (the right side of the window). 
        If the data is from an approach curve, a single 2D plot will be displayed.
        If the data is from a backstep scan, a 3D plot . Plotting data and details are based upon the 
        :param _view_data: View object which contains the data and display settings for the graph
        :param sicm_data: TODO: rewrite so unnecessary
        """
        plt.close('all')
        self.canvas.figure.clear()
        if isinstance(sicm_data, ScanBackstepMode):
            self.canvas.axes = self.canvas.figure.add_subplot(2,1,2)
            view_data.make_plot(self.canvas.axes)
            self.canvas.axes = self.canvas.figure.add_subplot(2,1,1, projection='3d')
            self.canvas.axes.plot_surface(*view_data.get_data(),cmap=matplotlib.cm.YlGnBu_r)
            #self.canvas.axes.plot_surface(*sicm_data.plot(), cmap=matplotlib.cm.YlGnBu_r)
            #self.canvas.axes.imshow(sicm_data.z, cmap=matplotlib.cm.YlGnBu_r)
            #Call view object and use plot/imshow rather than 
        if isinstance(sicm_data, ApproachCurve):
            self.canvas.axes = self.canvas.figure.add_subplot(111)
            view_data.make_plot(self.canvas.axes)
            #self.canvas.axes.plot(*sicm_data.plot())
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def import_files_dialog(self):
        """Opens a directory to import all .sicm files (Does not search subdirectories)."""
        #dialog = QFileDialog()#self.list_widget)
        #dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filenames, _ = QFileDialog.getOpenFileNames(self,
                                                    "Import pySICM Scan Files",  # title
                                                    "..",  # path
                                                    "pySICM Files (*.sicm)",  # file formats
                                                    options=options
                                                    )
        return filenames

    def add_files_to_list(self, files):
        """
        Add files to list
        Sets each pixel equal to the median of itself, the l pixel measurements immediately before, and the l pixel 
        measurements immediately afterwards (2l+1 pixels in total). Pixels with less than l pixels before or after them
        will use the available pixels and will not attempt to find addition pixels after the 0th or n-1th index in an array
        of length n.
        :param files: 
        """
        self.list_widget.addItems(files)
        if len(files) > 1:
            message_end = " files."
        else:
            message_end = " file."
        self.statusBar().showMessage("Imported " + str(len(files)) + message_end)

    def menu_action_import_directory(self):
        """Opens a file dialog to choose .sicm files."""
        dirname = QFileDialog().getExistingDirectory(self,'Select Folder')
        sicm_files = [join(dirname,f) for f in listdir(dirname) if (isfile(join(dirname, f)) and f.endswith('.sicm'))]
        self.add_files_to_list(sicm_files)

    def menu_action_clear(self):
        """Removes all items from list widget."""
        self.list_widget.clear()
        self.statusBar().showMessage("Files removed from the list.")

    def item_changed_event(self, item):
        """Updates the figure canvas when list selection has changed.
        """

        #self.currentItem = item
        #plt.close('all')
        #self.canvas.figure.clear()
        if item:
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
            self.canvas.axes.set_title(item.text())
            #print(data_view.get_data())
            #test.show_plot()
            #test.make_plot(self.canvas)
            #data_view.set_xlims([2,8])
            #test.make_plot(self.canvas)
            #test.show_plot()
            #temp = test.get_plot()
            #test.show_plot()
            #
            self.update_plots(self.currentView,self.currentData)

    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y()
        self.old_x = self.current_x
        self.old_y = self.current_y
        self.current_x = x
        self.current_y = y
        self.clickCount +=1

    def menu_action_export_bitmap(self):
        self.currentView.make_plot(self.canvas.axes,save=True)
    def menu_action_export_vector(self):
        self.currentView.make_plot(self.canvas.axes,save=True,saveType='pdf')
    def menu_action_plot_zoom(self):
        self.toolbar.zoom()
    def menu_action_plot_pan(self):
        self.toolbar.pan()

    def menu_action_plot_reset(self):
        #print(self.currentItem)1
        #print(self.list_widget.selectedItems)
        #self.item_changed_event(self.currentItem)#self.list_widget.selectedItems)
        self.update_plots(self.currentView,self.currentData)
    def menu_action_view_colormap(self):
        color_window = SecondaryWindow()
        SecondaryWindow
    def menu_action_view_content(self):
        self.currentView.toggle_axes()
        self.update_plots(self.currentView,self.currentData)
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
        self.update_plots(self.currentView,self.currentData)

    def menu_action_view_ylimits(self):
        limits, success = QtWidgets.QInputDialog.getText(
             self, 'Y Limit Input', 'Please enter the desired y limits separated by a space')
        limits = [float(f) for f in limits.split()]
        self.currentView.set_ylims(limits)
        self.update_plots(self.currentView,self.currentData)
    def menu_action_view_ratio(self):
        ratio, success = QtWidgets.QInputDialog.getText(
             self, 'Ratio Input', 'Please enter the numerical ratio, \'equal\', or \'auto\'')
        if(self.currentView.set_aspect(ratio)):
            self.update_plots(self.currentView,self.currentData)
        else:
            #TODO Implement error message to user
            return 0
    def menu_action_view_restore(self):
        self.currentView.restore()
        self.update_plots(self.currentView,self.currentData)
    
    def menu_action_data_crop(self):
        xlimits, success = QtWidgets.QInputDialog.getText(
             self, 'X Crop Dimensions', 'Please enter the desired x dimensions separated by a space')
        xlimits = [int(f) for f in xlimits.split()]
        ylimits, success = QtWidgets.QInputDialog.getText(
             self, 'Y Crop Dimensions', 'Please enter the desired y dimensions separated by a space')
        ylimits = [int(f) for f in ylimits.split()]
        limits = np.array((xlimits,ylimits))
        self.currentView.set_data(crop(self.currentView.get_data(),limits))
        self.update_plots(self.currentView,self.currentData)

    def menu_action_data_minimum(self):
        self.currentView.set_z_data(subtract_minimum(self.currentView.get_z_data()))
        self.currentView.make_plot(self.canvas.axes)
        self.update_plots(self.currentView,self.currentData)
        #print(np.min(self.currentView.get_z_data()))

    def menu_action_data_average(self):
       pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Average)', 'Please enter the number of pixels to use on either side')
       self.currentView.set_z_data(filter_average_temporal(self.currentView.get_z_data(),int(pixels)))
       self.currentView.make_plot(self.canvas.axes)
       self.update_plots(self.currentView,self.currentData)
    def menu_action_data_median(self):
       pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Median)', 'Please enter the number of pixels to use on either side')
       self.currentView.set_z_data(filter_median_temporal(self.currentView.get_z_data(),int(pixels)))
       self.currentView.make_plot(self.canvas.axes)
       self.update_plots(self.currentView,self.currentData)

    def menu_action_data_saverage(self):
       pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Average)', 'Please enter the number of pixels around the center to use')
       self.currentView.set_z_data(filter_average_spatial(self.currentView.get_z_data(),int(pixels)))
       self.currentView.make_plot(self.canvas.axes)
       self.update_plots(self.currentView,self.currentData)
    def menu_action_data_smedian(self):
       pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Smoothing Pixels (Median)', 'Please enter the number of pixels around the center to use')
       self.currentView.set_z_data(filter_median_spatial(self.currentView.get_z_data(),int(pixels)))
       self.currentView.make_plot(self.canvas.axes)
       self.update_plots(self.currentView,self.currentData)
    
    def menu_action_data_plane(self):
        test = level_data(self.currentView,method='plane').transpose()
        #print(test)
        #print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
    
    def menu_action_data_paraboloid(self):
        test = level_data(self.currentView,method='paraboloid').transpose()
        #print(test)
        #print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
    def menu_action_data_poly(self):
        test = level_data(self.currentView,method='2Dpoly').transpose()
        #print(test)
        #print(test.shape)
        self.currentView.set_z_data(test)
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
    def menu_action_data_splines(self):
        #TODO Determine intended usage of this 
        #self.currentView.set_z_data(interpolate_cubic(self.currentView).T)
        #self.update_plots(self.currentView,self.currentData)
        #self.currentView.make_plot(self.canvas.axes)
        #interpolate_cubic(self.currentView)
        #print(f)
        #plt.imshow(interpolate_cubic(self.currentView).T, extent=(0,1,0,1))
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Interpolation (Cubic Spline)', 'Please enter the number of pixels interpolate per')
        new_z,new_x,new_y = interpolate_cubic(self.currentView,int(pixels),method='cubic')#.T
        #print(test)
        #print(test.shape)
        self.currentView.set_x_data(new_x)
        self.currentView.set_y_data(new_y)
        self.currentView.set_z_data(new_z)
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
        return
    def menu_action_data_neighbor(self):
        #TODO Determine intended usage of this 
        #self.currentView.set_z_data(interpolate_cubic(self.currentView).T)
        #self.update_plots(self.currentView,self.currentData)
        #self.currentView.make_plot(self.canvas.axes)
        #interpolate_cubic(self.currentView)
        #print(f)
        #plt.imshow(interpolate_cubic(self.currentView).T, extent=(0,1,0,1))
        pixels, success = QtWidgets.QInputDialog.getText(
            self, 'Interpolation (Cubic Spline)', 'Please enter the number of pixels interpolate per')
        new_z,new_x,new_y = interpolate_cubic(self.currentView,int(pixels),method='nearest')#.T
        #print(test)
        #print(test.shape)
        self.currentView.set_x_data(new_x)
        self.currentView.set_y_data(new_y)
        self.currentView.set_z_data(new_z)
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
        return
    
    def menu_action_data_reset(self):
        self.currentView.reset_data()
        self.update_plots(self.currentView,self.currentData)
        self.currentView.make_plot(self.canvas.axes)
    def get_current_x(self):
        return self.current_x
    def get_current_y(self):
        return self.current_y
    def get_old_x(self):
        return self.old_x
    def get_old_y(self):
        return self.old_y
    #def item_activated_event(self):#,item):
        #self.currentItem = item
        #print(self.list_widget.selectedItems)

    #def menu_action_clear(self):
        #"""Removes all items from list widget."""
        #self.list_widget.clear()
        #self.statusBar().showMessage("Files removed from the list.")

#class Example(QMainWindow):

    #def __init__(self):
        #super().__init__()

        #self.initUI()

    #def initUI(self):

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')

        #impMenu = QMenu('Import', self)
        #impAct = QAction('Import mail', self)
        #impMenu.addAction(impAct)

        #newAct = QAction('New', self)

        #fileMenu.addAction(newAct)
        #fileMenu.addMenu(impMenu)

app = QApplication(sys.argv)
windows = MainWindow()
sys.exit(app.exec())
