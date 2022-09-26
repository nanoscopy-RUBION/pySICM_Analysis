from PyQt6.QtCore import QPoint
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sicm_analyzer.mouse_events import MouseInteraction
from sicm_analyzer.sicm_data import SICMdata
from sicm_analyzer.view import View

SURFACE_PLOT = "surface"
RASTER_IMAGE = "raster"
APPROACH_CURVE = "approach"


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data."""

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        # NavToolbar should be customized before integrating in GraphCanvas
        # Furthermore, GraphCanvas needs a parent widget
        #self.toolbar = NavigationToolbar(canvas=self, parent=self)

        # These attributes are necessary for handling the various
        # mouse event functions
        self.mi = MouseInteraction()
        self.function_after_mouse_events = None
        self.current_data: SICMdata = None
        self.current_view: View = None

    def draw_graph(self, data: SICMdata, graph_type: str = "", view: View = None):
        """
        Draws a 3D or 2D graph depending on the type. Three types are supported at the moment:
            SURFACE_PLOT: a 3-dimensional figure which can be rotated by mouse interaction
            RASTER_IMAGE: a raster image for 3D data with a color bar
            APPROACH_CURVE:

        Data needs to be checked before calling this function!

        :param data: View object which contains the data and display settings for the graph
        :param graph_type: type of graph to be drawn. If no type is given, an empty canvas will be drawn
        :param view:
        """
        self.figure.clear()

        if graph_type == SURFACE_PLOT:
            self.draw_3d_plot(data, view)

        if graph_type == RASTER_IMAGE:
            self.draw_2d_plot_raster_image(data, view)

        if graph_type == APPROACH_CURVE:
            self.draw_approach_curve(data)

        self.figure.tight_layout()
        self.draw()

    def convert_axes_labels_from_px_to_microns(self, data: SICMdata, axes):
        """

        """
        x_size = data.x_size
        x_px = data.x_px
        y_size = data.y_size
        y_px = data.y_px
        x_ticks = axes.get_xticks()
        y_ticks = axes.get_yticks()
        if x_px != x_size:
            axes.set_xticklabels(self.get_tick_labels_in_microns(x_ticks, x_px, x_size))
        if y_px != y_size:
            axes.set_yticklabels(self.get_tick_labels_in_microns(y_ticks, y_px, y_size))

    def get_tick_labels_in_microns(self, ticks, n_px, n_size):
        labels = []
        if n_px != n_size:
            for tick in ticks:
                label = round(tick * (n_size / n_px), 2)
                labels.append(label)
        return labels

    def show_or_hide_axes(self, data: SICMdata, view: View, axes):
        if view.axes_shown:
            if view.show_as_px:
                axis_label = "px"
            else:
                self.convert_axes_labels_from_px_to_microns(data, axes)
                axis_label = "µm"

            axes.set_xlabel(axis_label)
            axes.set_ylabel(axis_label)
            try:
                # 2D plots have no zlabel
                axes.set_zlabel("µm")  # z data is always in µm
            except:
                pass
        else:
            axes.axis(False)

    def draw_3d_plot(self, data: SICMdata, view: View = None):
        """Draws a 3d surface plot for scanning data."""
        axes = self.figure.add_subplot(1, 1, 1, projection='3d')

        if view:
            img = axes.plot_surface(*data.get_data(), cmap=view.color_map)
            axes.set_box_aspect(aspect=view.aspect_ratio)
            axes.azim = view.azim
            axes.elev = view.elev
            self.show_or_hide_axes(data, view, axes)
        else:
            img = axes.plot_surface(*data.get_data())

        cb = self.figure.colorbar(img)
        cb.set_label(label="height in µm")


    def draw_2d_plot_raster_image(self, data: SICMdata, view: View = None):
        """Draws a 2D raster image for 3-dimensional scanning data."""
        axes = self.figure.add_subplot(1, 1, 1)
        # use pcolormesh for scalable pixelmaps
        # img = self.axes.imshow(view_object.z_data, cmap=view_object.color_map)
        #if data.rois:
        #    self.draw_roi(data)

        if view:
            self.show_or_hide_axes(data, view, axes)
            img = axes.pcolormesh(data.z, cmap=view.color_map)
        else:
            img = axes.pcolormesh(data.z)
        axes.set_aspect("equal")
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cb = self.figure.colorbar(img, cax=cax)
        cb.set_label(label="height in µm")

    def draw_roi(self, data: SICMdata):
        """This function should be generalised to prevent code duplication.
        At the moment it is a quick and dirty implementation for testing
        ROIs."""
        try:
            point1 = view_object.rois[0]
            point2 = view_object.rois[1]
            if point1.x() < point2.x():
                orig_x = point1.x()
            else:
                orig_x = point2.x()
            if point1.y() < point2.y():
                orig_y = point1.y()
            else:
                orig_y = point2.y()
            origin = (orig_x, orig_y)

            width = abs(point1.x() - point2.x())
            height = abs(point1.y() - point2.y())
            rect = Rectangle(xy=origin, width=width, height=height,
                             fill=False,
                             linewidth=2, edgecolor='g',
                             figure=self.figure
                             )
            self.figure.get_axes()[0].add_patch(rect)
        except:
            pass

    def draw_approach_curve(self, data: SICMdata, view: View = None):
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(*data.get_data())
        if view:
            self.axes.axis(view.axes_shown)

    def draw_line_profile(self, data: SICMdata, view: View = None, func=None):
        """Draw line profile plot.
        TODO distinguish between column and row mode
        Maybe later custom drawn lines on the plot will be supported.
        """
        self._bind_mouse_events(self._highlight_row_or_column_and_call_func)
        self.function_after_mouse_events = func
        self.current_data = data
        self.current_view = view


    def get_viewing_angles_from_3d_plot(self):
        azim = self.figure.get_axes()[0].azim
        elev = self.figure.get_axes()[0].elev
        return azim, elev

    def draw_rectangle_on_raster_image(self, data: SICMdata, view: View = None, func=None):
        self._bind_mouse_events(self._draw_rectangle_and_call_func)
        self.function_after_mouse_events = func
        self.current_data = data
        self.current_view = view

    def _bind_mouse_events(self, func):
        """Binds func1 to mouse events on the canvas.
        Function 2 is optional and will be called after the mouse button
        release event has occurred."""
        self.mi = MouseInteraction()
        self.mi.cid_press = self.figure.canvas.mpl_connect('button_press_event', func)
        self.mi.cid_move = self.figure.canvas.mpl_connect('motion_notify_event', func)
        self.mi.cid_release = self.figure.canvas.mpl_connect('button_release_event', func)

    def _draw_rectangle_and_call_func(self, event):
        """Allows to draw a rectangle on the raster image canvas and calls func with
        the points of the drawn rectangle as arguments."""
        if event.inaxes:
            if event.name == "button_press_event":
                self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

            if event.name == "motion_notify_event":
                if self.mi.mouse_point1 is not None:
                    self.figure.clear()
                    self.draw_2d_plot_raster_image(self.current_data, self.current_view)
                    self.mi.mouse_point2 = QPoint(int(event.xdata), int(event.ydata))

                    #print("P1: %s, P2: %s" % (self.mi.mouse_point1, self.mi.mouse_point2))

                    if self.mi.mouse_point1.x() < self.mi.mouse_point2.x():
                        orig_x = self.mi.mouse_point1.x()
                    else:
                        orig_x = self.mi.mouse_point2.x()
                    if self.mi.mouse_point1.y() < self.mi.mouse_point2.y():
                        orig_y = self.mi.mouse_point1.y()
                    else:
                        orig_y = self.mi.mouse_point2.y()
                    origin = (orig_x, orig_y)

                    width = abs(self.mi.mouse_point1.x() - self.mi.mouse_point2.x()) + 1
                    height = abs(self.mi.mouse_point1.y() - self.mi.mouse_point2.y()) + 1
                    rect = Rectangle(xy=origin, width=width, height=height,
                                     fill=True, facecolor='r', alpha=0.4,
                                     linewidth=2, edgecolor='r',
                                     figure=self.figure
                                     )
                    self.figure.get_axes()[0].add_patch(rect)
                    self.draw()

            if event.name == "button_release_event":
                if self.mi.mouse_point1 is not None and self.mi.mouse_point2 is not None:
                    self.figure.canvas.mpl_disconnect(self.mi.cid_press)
                    self.figure.canvas.mpl_disconnect(self.mi.cid_move)
                    self.figure.canvas.mpl_disconnect(self.mi.cid_release)
                    if self.mi.mouse_point1.x() <= self.mi.mouse_point2.x():
                        self.mi.mouse_point2 = self.mi.mouse_point2 + QPoint(1, 0)
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1 + QPoint(1, 0)
                    if self.mi.mouse_point1.y() <= self.mi.mouse_point2.y():
                        self.mi.mouse_point2 = self.mi.mouse_point2 + QPoint(0, 1)
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1 + QPoint(0, 1)
                    #print("CROP P1: %s, P2: %s" % (self.mi.mouse_point1, self.mi.mouse_point2))
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.mouse_point1, self.mi.mouse_point2)
                        self.function_after_mouse_events = None
                    self.mi = None

    def _draw_a_line_on_raster_image(self):
        """TODO not yet finished
        Create a Line2D object from mouse coordinates and then
        add a patch to the figure axes before figure.draw.
        """
        p1 = [self.mi.mouse_point1.x(), self.mi.mouse_point2.x() + 1]
        p2 = [self.mi.mouse_point1.y(), self.mi.mouse_point2.y() + 1]
        line = Line2D(p1, p2, color="r")
        self.figure.get_axes()[0].add_patch(line)

    def _highlight_row_or_column_and_call_func(self, event):
        """
        mode can either be "row" or "column"
        """
        if event.inaxes:
            if event.name == "motion_notify_event":
                try:
                    self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))
                    x1 = 0
                    y1 = self.mi.mouse_point1.y()
                    x2 = self.current_data.z.shape[0]-1
                    y2 = y1 + 1

                    self.figure.clear()
                    self.draw_2d_plot_raster_image(self.current_data, self.current_view)

                    origin = (x1, y1)

                    width = x2 + 1
                    height = 1
                    rect = Rectangle(xy=origin, width=width, height=height,
                                     fill=True, facecolor='r', alpha=0.4,
                                     linewidth=2, edgecolor='r',
                                     figure=self.figure
                                     )
                    self.figure.get_axes()[0].add_patch(rect)
                    self.draw()
                except:
                    pass

            if event.name == "button_press_event":
                self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

            if event.name == "button_release_event":
                self.figure.clear()
                self.draw_2d_plot_raster_image(self.current_data, self.current_view)
                self.draw()

                if self.mi.mouse_point1 is not None:
                    self.figure.canvas.mpl_disconnect(self.mi.cid_press)
                    self.figure.canvas.mpl_disconnect(self.mi.cid_move)
                    self.figure.canvas.mpl_disconnect(self.mi.cid_release)

                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.mouse_point1.y())
                        self.function_after_mouse_events = None
                    self.mi = None

    def plot_line_profile(self, x_data, y_data):
        self.figure.clear()
        axes = self.figure.add_subplot(1, 1, 1)
        axes.plot(x_data, y_data)
        self.draw()

    def _get_coordinate_of_click_on_click(self, event) -> QPoint or None:
        """Returns a QPoint with coordinates of mouse click event or None if the click event
        was not inside the graph.
        """
        if event.inaxes and event.name == "button_press_event":
            return QPoint(int(event.xdata), int(event.ydata))
        else:
            return None
