import matplotlib
import matplotlib.pyplot as plt
from SICMViewerHelper import SICMDataFactory, ApproachCurve, ScanBackstepMode
import numpy as np


class View:
    """
    View Class
    Class which contains the data and viewing settings for . One instance of the view class is linked to each file imported.
    This relationship starts when the item is first selected from the list. The relationship is preversed , although certain 
    features (such as rotation of )
    """
    ylims = None
    xlims = None
    aspectRatio = 'auto'
    axis_shown = True
    sicm_data = None
    x_data = None
    z_data = None
    y_data = None
    default_xlim = None
    default_ylim = None

    def __init__(self, data):
        self.sicm_data = data
        self.mode = data.scan_mode
        if isinstance(self.sicm_data, ScanBackstepMode):  # self.mode == "backstepScan":
            self.x_data, self.y_data, self.z_data = data.plot()
            self.x_data = np.array(self.x_data)
            self.y_data = np.array(self.y_data)
            self.z_data = np.array(self.z_data)
        else:
            self.x_data, self.z_data = data.plot()
            self.x_data = np.array(self.x_data)
            self.z_data = np.array(self.z_data)

    def get_plot(self):
        """
        Returns the underlying data from the SICMFactory class used to build the class. Notably, this data is NOT
        modified by data manipulation. To obtain the manipulated data, use get_data instead.
        :returns: Unmodified copy of data extracted from imported file.
        """
        return self.plot

    def get_data(self):
        if isinstance(self.sicm_data, ScanBackstepMode):
            return np.array([self.x_data, self.y_data, self.z_data])
        else:  # if isinstance(self.sicm_data, ):
            return [self.x_data, self.z_data]

    def get_x_data(self):
        return self.x_data

    def get_y_data(self):
        return self.y_data

    def get_z_data(self):
        return self.z_data

    def set_data(self, data):
        self.x_data, self.y_data, self.z_data = np.array(data)

    def set_x_data(self, data):
        self.x_data = np.array(data)

    def set_y_data(self, data):
        self.y_data = np.array(data)

    def set_z_data(self, data):
        self.z_data = np.array(data)

    def get_xlim(self):
        return self.xlims

    def get_ylim(self):
        return self.ylims

    def make_plot(self, gui, save=False, saveType='png'):
        """
        Make plot is the core function used to create new instances of the . This must be called after changing view properties
        or manipulating data, or the 

        :param gui: This is the canvas access of the GUI upon which the plot will be displayed. In this program, it should generally
        be the
        :param save:
        :param saveType:
        """
        if isinstance(self.sicm_data, ScanBackstepMode):
            img = gui.axes.imshow(self.get_z_data(), cmap=matplotlib.cm.YlGnBu_r, aspect='auto')
            # img = gui.axes.plot(self.get_z_data())#,cmap=matplotlib.cm.YlGnBu_r,aspect='auto')
        else:  # if isinstance(self.sicm_data, ):
            img = gui.axes.plot(*self.get_data())
        if not self.default_xlim:
            self.default_xlim = gui.axes.get_xlim()
        if not self.default_ylim:
            self.default_ylim = gui.axes.get_ylim()
        # gui.axes
        # sub.plot(*self.sicm_data.plot())
        # ax = fig.add_axes([0,0,1,1])
        if self.xlims:
            gui.axes.set_xlim(self.xlims)
            # ax.set_xlim(self.xlims)
        if self.ylims:
            gui.axes.set_ylim(self.ylims)
        gui.axes.set_aspect(self.aspectRatio)
        gui.axes.axis(self.axis_shown)
        # ax.set_aspect(self.aspectRatio)
        # self.plot = fig
        # gui.figure.show()
        if save:
            # plt.imsave("Test.png",self.get_data())
            # plt.figure(img)
            plt.imsave('Test.' + saveType, self.get_z_data())
            # plt.savefig("TestSaveFig.png")
            # img.savefig('TestSaveFig.'+saveType)
        plt.draw()

    def show_plot(self):
        # This does not work, should be deleted
        if isinstance(self.sicm_data, ScanBackstepMode):
            self.plot = plt.plot(*self.sicm_data.plot())
        else:  # if isinstance(self.sicm_data, ):
            self.plot = plt.plot(*self.sicm_data.plot())
        # plt.show()
        plt.draw()

    def set_aspect(self, aspect):

        if aspect == 'equal' or aspect == 'auto':
            self.aspectRatio = aspect
            return 1
        try:
            aspect = float(aspect)
            self.aspectRatio = aspect
            return 1
        except ValueError:
            return 0

    def toggle_axes(self):
        """
        Changes the state of the axis for the 2D plot, hiding it if it is displayed and displaying it if it is hidden
        """
        self.axis_shown = not self.axis_shown

    def show_axis(self):
        return self.axis_shown

    def set_xlims(self, lims):
        """
        Set Xlims
        Sets x-axis limits for the visual display of the data. This does not crop the data and the rest can still be viewed by panning.
        Will check to ensure the values are floats but does not check that the lower bound is first.

        :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
        :returns: 1 upon successful setting and 0 upon failure
        """
        if len(lims) == 2:
            if (isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.xlims = lims
                return 1
            else:
                # print("Please choose numbers for both") #Check input elsewhere?
                return 0

    def set_ylims(self, lims):
        """
        Set Y-limits for the visual display of the data. This does not crop the data and the rest can still be viewed by panning.
        Will check to ensure the values are floats but does not check that the lower bound is first.

        :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
        :returns: this is a description of what is returned
        """
        if len(lims) == 2:
            if (isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.ylims = lims
                return 1
            else:
                print("Please choose numbers for both")  # Check input elsewhere?
                return 0

    def restore(self):
        """
        Restore
        Resets all viewing options (graph limits, whether axises are shown, aspect ratio, etc) to their default values.
        Does NOT reset any changes to the data being displayed in the graph. The 'reset_data' function in the View package
        should be used for that purpose.
        """
        self.axis_shown = "On"
        # print(self.default_xlim)
        # print(self.default_ylim)
        self.set_xlims(self.default_xlim)
        self.set_ylims(self.default_ylim)
        self.set_aspect("auto")
        self.change_color_map()

    def change_color_map(self):
        return 1

    def reset_data(self):
        """
        Reset_Data
        Sets each pixel equal to the median of itself, the l pixel measurements immediately before, and the l pixel 
        measurements immediately afterwards (2l+1 pixels in total). Pixels with less than l pixels before or after them
        will use the available pixels and will not attempt to find addition pixels after the 0th or n-1th index in an array
        of length n.
        """
        self.set_data(self.sicm_data.plot())
