from datetime import time

from PyQt5.QtCore import QPoint


class MouseInteraction:

    def __init__(self):
        self.cid_move = None
        self.cid_press = None
        self.cid_release = None

        self.mouse_point1 = None
        self.mouse_point2 = None

    def set_point_1_on_click(self, event):
        if event.name == "button_press_event":
            self.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))
            print(self.mouse_point1)


def click_on_raster_image(event):
    """A test function for getting the correct pixel after clicking on it.
    TODO Clean up and move to another class
    """
    from pySICM_Analysis.gui_main import SecondaryWindow
    axes = event.canvas.figure.get_axes()[0]
    print(event)
    if event.inaxes == axes:
        print("oben")
    else:

        self.w = SecondaryWindow(self.main_window)
        self.w.add_canvas(GraphCanvas())
        self.w.show()

        self.last_change = None
        self.X = None
        self.Y = None

        print("unten")
        print("x: %s, y: %s" % (event.xdata, event.ydata))
        # coordinates need to be adjusted when imshow is used
        # instead of pcolormesh for 2D plots
        x = int(event.xdata)  # + 0.5)
        y = int(event.ydata)  # + 0.5)

        self.w.canvas.figure.clear()
        self.w.canvas.axes = self.w.canvas.figure.add_subplot(111)
        self.w.canvas.axes.plot(self.currentView.x_data[y, :], self.currentView.z_data[y, :])

        if not self.last_change:
            self.X = x
            self.Y = y
            self.last_change = self.currentView.z_data[y, x]
            # self.currentView.z_data[y, x] = 0.0
            self.figure_canvas_2d.draw_graph(self.currentView)
        else:
            print("Last: %s" % self.last_change)
            self.currentView.z_data[self.Y, self.X] = self.last_change
            # self.last_change = self.currentView.z_data[y, x]
            self.currentView.z_data[y, x] = 0.0
            self.X = x
            self.Y = y
            self.figure_canvas_2d.draw_graph(self.currentView)
            print(self.X, self.Y)
        print(self.currentView.z_data[x, y])




def origin_point(canvas, event):
    if event.name == "button_press_event":
        self.P1 = QPoint(int(event.xdata), int(event.ydata))
        self.cid_release = self.figure_canvas_2d.figure.canvas.mpl_connect('button_release_event', self.rectangle_test)
        self.cid_move = self.figure_canvas_2d.figure.canvas.mpl_connect('motion_notify_event', self.rectangle_test)


def mouse_over_value(event):
    print("z: %s µm " % self.get_data_from_point(QPoint(int(event.xdata), int(event.ydata))))
    print("Coords: X %s | Y %s " % (event.xdata, event.ydata))
    time.sleep(0.2)


def about():

    if not self.cid:
        if len(self.figure_canvas_2d.figure.get_axes()) > 1:
            self.cid_press = self.figure_canvas_2d.figure.canvas.mpl_connect('button_press_event', self.origin_point)
            self.cid = self.figure_canvas_2d.figure.canvas.mpl_connect('button_press_event', self.click_on_raster_image)
            self.cid = self.figure_canvas_2d.figure.canvas.mpl_connect("motion_notify_event", self.mouse_over_value)
    else:
        figure_canvas.figure.canvas.mpl_disconnect(self.cid)
        cid = None

def get_data_from_point(self, point: QPoint):
    """"""
    return self.currentView.z_data[point.y(), point.x()]