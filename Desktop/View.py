import matplotlib
import matplotlib.pyplot as plt
from SICMViewerHelper import SICMDataFactory, ApproachCurve, ScanBackstepMode
import numpy as np

class View:

    ylims = None
    xlims = None
    aspectRatio = 'auto'
    axis_shown = "On"
    sicm_data = None
    x_data = None
    z_data = None
    y_data = None
    #mode = None
    def __init__(self,data):
        self.sicm_data = data
        self.mode = data.scan_mode
        if isinstance(self.sicm_data, ApproachCurve):
            self.x_data,self.z_data = data.plot()
            self.x_data = np.array(self.x_data)
            self.y_data = np.array(self.y_data)
            self.z_data = np.array(self.z_data)
        else:
            self.x_data,self.y_data,self.z_data = data.plot()
            self.x_data = np.array(self.x_data)
            self.z_data = np.array(self.z_data)
        

        #self.plot = plt.plot(*self.sicm_data.plot())
        #plt.show()
        #if self.mode == ''
        #self.sicm_data = factory_data
        #if isinstance(self.sicm_data,ScanBackstepMode):
            #self.plot = plt.imshow(*self.sicm_data.plot())
        #else:#if isinstance(self.sicm_data, ):
            #self.plot = plt.plot(*self.sicm_data.plot())
    def get_plot(self):
        return self.plot
    def get_data(self):
        if isinstance(self.sicm_data,ScanBackstepMode):
            return [self.x_data,self.y_data,self.z_data]
        else:#if isinstance(self.sicm_data, ):
            return [self.x_data,self.z_data]
    def get_x_data(self):
        return self.x_data
    def get_y_data(self):
        return self.y_data
    def get_z_data(self):
        return self.z_data
    def set_data(self,data):
        self.x_data,self.y_data,self.z_data = np.array(data)
    def set_x_data(self,data):
        self.x_data = np.array(data)
    def set_y_data(self,data):
        self.y_data = np.array(data)
    def set_z_data(self,data):
        self.z_data = np.array(data)
    def make_plot(self,gui):
        #print(self.sicm_data.plot())
        #fig = plt.figure()
        #sub = fig.add_subplot(1,1,1)

        #gui.axes.plot(*self.sicm_data.plot())
        if isinstance(self.sicm_data,ScanBackstepMode):
            gui.axes.imshow(self.get_z_data(),cmap=matplotlib.cm.YlGnBu_r,aspect='auto')
        else:#if isinstance(self.sicm_data, ):
            gui.axes.plot(*self.get_data())
        self.default_xlim = gui.axes.get_xlim()
        self.default_ylim = gui.axes.get_ylim()
        #gui.axes
        #sub.plot(*self.sicm_data.plot())
        #ax = fig.add_axes([0,0,1,1])
        if self.xlims:
            gui.axes.set_xlim(self.xlims)
            #ax.set_xlim(self.xlims)
        if self.ylims:
            gui.axes.set_ylim(self.ylims)
        gui.axes.set_aspect(self.aspectRatio)
        gui.axes.axis(self.axis_shown)
        #ax.set_aspect(self.aspectRatio)
        #self.plot = fig
        #gui.figure.show()
        plt.draw()
    def show_plot(self):
        if isinstance(self.sicm_data,ScanBackstepMode):
            self.plot = plt.plot(*self.sicm_data.plot())
        else:#if isinstance(self.sicm_data, ):
            self.plot = plt.plot(*self.sicm_data.plot())
        #plt.show()
        plt.draw()
    def set_aspect(self,aspect):
        if aspect == 'equal' or aspect == 'auto':
            self.aspectRatio = aspect
            return 1
        #if isinstance(aspect, float) or isinstance(aspect, int):
        try: 
            aspect = float(aspect)
            self.aspectRatio = aspect
            return 1
        except ValueError:
            return 0
    def toggle_axes(self):
        if self.axis_shown == "On":
            self.axis_shown = "Off"
        else:
            self.axis_shown = "On"
    def set_xlims(self, lims):
        if len(lims) == 2:
            if(isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.xlims = lims
                return 1
            else:
                #print("Please choose numbers for both") #Check input elsewhere?
                return 0
    def set_ylims(self, lims):
        if len(lims) == 2:
            if(isinstance(lims[0], float) and isinstance(lims[1], float)):
                self.ylims = lims
                return 1
            else:
                print("Please choose numbers for both") #Check input elsewhere?
                return 0
    def restore(self):
        self.axis_shown = "On"
        self.set_xlims(self.default_xlim)
        self.set_ylims(self.default_ylim)
        self.set_aspect("auto")
        #self.make_plot()
        #self.show_plot()
        self.change_color_map()
    def change_color_map(self):
        return 1
    def reset_data(self):
        self.set_data(self.sicm_data.plot())
    

#test = View([[1,3,4],[2,4,1],[2,4,1]])
#test.make_plot()
#test.show_plot