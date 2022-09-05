from PyQt5.QtCore import QPoint
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pySICM_Analysis.mouse_events import MouseInteraction
from pySICM_Analysis.view import View

SURFACE_PLOT = "surface"
RASTER_IMAGE = "raster"
APPROACH_CURVE = "approach"


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data."""

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

        self.mi = MouseInteraction()
        self.function_after_mouse_events = None
        self.current_view: View = None

    def draw_graph(self, view_object: View, graph_type: str = ""):
        """
        Draws a 3D or 2D graph depending on the type. Three types are supported at the moment:
            SURFACE_PLOT: a 3-dimensional figure which can be rotated by mouse interaction
            RASTER_IMAGE: a raster image for 3D data with a color bar
            APPROACH_CURVE:

        Data needs to be checked before calling this function!

        :param view_object: View object which contains the data and display settings for the graph
        :param graph_type: type of graph to be drawn. If no type is given, an empty canvas will be drawn
        """
        self.figure.clear()

        if graph_type == SURFACE_PLOT:
            self.draw_3d_plot(view_object)

        if graph_type == RASTER_IMAGE:
            self.draw_2d_plot_raster_image(view_object)

        if graph_type == APPROACH_CURVE:
            self.draw_approach_curve(view_object)

        self.figure.tight_layout()
        self.draw()

    def convert_axes_labels_from_px_to_microns(self, view_object: View, axes):
        """"""
        x_size = view_object.sicm_data.x_size
        x_px = view_object.sicm_data.x_px
        y_size = view_object.sicm_data.y_size
        y_px = view_object.sicm_data.y_px
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

    def show_or_hide_axis(self, view_object, axes):
        if view_object.axes_shown:
            if view_object.show_as_px:
                axis_label = "px"
            else:
                self.convert_axes_labels_from_px_to_microns(view_object, axes)
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

    def draw_3d_plot(self, view_object: View):
        """Draws a 3d surface plot for scanning data."""
        axes = self.figure.add_subplot(1, 1, 1, projection='3d')
        axes.plot_surface(*view_object.get_modified_data(), cmap=view_object.color_map)
        axes.set_box_aspect(aspect=view_object.aspect_ratio)
        axes.azim = view_object.azim
        axes.elev = view_object.elev
        self.show_or_hide_axis(view_object, axes)

    def draw_2d_plot_raster_image(self, view_object: View):
        """Draws a 2D raster image for 3-dimensional scanning data."""
        axes = self.figure.add_subplot(1, 1, 1)
        # use pcolormesh for scalable pixelmaps
        img = axes.pcolormesh(view_object.z_data, cmap=view_object.color_map)
        # img = self.axes.imshow(view_object.z_data, cmap=view_object.color_map)
        axes.set_aspect("equal")

        self.show_or_hide_axis(view_object, axes)
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        #cb = self.figure.colorbar(img)
        cb = self.figure.colorbar(img, cax=cax)
        cb.set_label(label="height in µm")

    def draw_approach_curve(self, view_object: View):
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(*view_object.get_modified_data())
        self.axes.axis(view_object.axes_shown)

    def draw_line_profile(self, view_object: View, *args):
        print(*args)

    def get_viewing_angles_from_3d_plot(self):
        azim = self.figure.get_axes()[0].azim
        elev = self.figure.get_axes()[0].elev
        return azim, elev

    def draw_rectangle_on_raster_image(self, current_view: View, func=None):
        self._bind_mouse_events(self._draw_rectangle_and_call_func)
        self.function_after_mouse_events = func
        self.current_view = current_view

    def _bind_mouse_events(self, func):
        """Binds func1 to mouse events on the canvas.
        Function 2 is optional and will be called after the mouse button
        release event has occured."""
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
                    self.draw_2d_plot_raster_image(self.current_view)
                    self.mi.mouse_point2 = QPoint(int(event.xdata), int(event.ydata))

                    print("P1: %s, P2: %s" % (self.mi.mouse_point1, self.mi.mouse_point2))

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
                                     linewidth=1, edgecolor='r',
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
                    print("CROP P1: %s, P2: %s" % (self.mi.mouse_point1, self.mi.mouse_point2))
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.mouse_point1, self.mi.mouse_point2)
                        self.function_after_mouse_events = None
                    self.mi = None

