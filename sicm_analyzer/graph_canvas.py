import traceback

from PyQt6.QtCore import QPoint
from typing import Callable
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import Normalize
import sicm_analyzer.sicm_data
from sicm_analyzer.mouse_events import MouseInteraction, COLUMN, ROW, CROSS
from sicm_analyzer.sicm_data import SICMdata, ScanBackstepMode
from sicm_analyzer.view import View
import numpy as np
import math

SURFACE_PLOT = "surface"
RASTER_IMAGE = "raster"
APPROACH_CURVE = "approach"


def convert_axes_labels_from_px_to_microns(data: SICMdata, axes):
    """

    """
    x_ticks = axes.get_xticks()
    y_ticks = axes.get_yticks()

    if isinstance(data, sicm_analyzer.sicm_data.ScanBackstepMode):
        axes.set_xticklabels([round(tick * data.micron_to_pixel_factor_x(), 2) for tick in x_ticks])
        axes.set_yticklabels([round(tick * data.micron_to_pixel_factor_y(), 2) for tick in y_ticks])


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data.

    This class implements all functions for plotting SICM data. Line profiles
    can also be drawn.

    Drawing of rectangles on 2D raster images for defining, for example,
    regions of interest (ROI) is also supported.

    For mouse interaction with the plots two attributes are
    in this class:
        - mi: to reference an instance of MouseInteraction (see MouseInteraction documentation)
        - function_after_mouse_event: a callable can be assigned to this field which will be called
        as a consequence of the mouse interaction (e.g., a data manipulating function/method after selection
        of pixels in the plot)

    To add functionality for mouse interactions with the canvas:
        Define a method which takes a callable and maybe some arguments as parameters.
        In this method bind the callable to an instance of MouseInteraction.

    TODO: Plot settings should be controlled by a View object.
    TODO: add navigation toolbar?
    """

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        # NavToolbar should be customized before integrating in GraphCanvas
        # Furthermore, GraphCanvas needs a parent widget
        # self.toolbar = NavigationToolbar(canvas=self, parent=self)

        # These attributes are necessary for handling the various
        # mouse event functions
        self.mi = MouseInteraction()
        self.function_after_mouse_events = None
        self.clean_up_function = None
        self.show_mouse_over_label = True
        self.current_data: SICMdata = SICMdata()
        self.current_view: View = View()
        self.graph_type = ""
        self.draw_white_canvas()

    def draw_graph(self, data: SICMdata, graph_type: str = "", view: View = None):
        """
        Draws a 3D or 2D graph depending on the type. Three types are supported at the moment:
            SURFACE_PLOT: a 3-dimensional figure which can be rotated by mouse interaction
            RASTER_IMAGE: a raster image for 3D data with a color bar
            APPROACH_CURVE:

        Data needs to be checked before calling this function!

        :param SICMdata data: contains the data for plotting
        :param str graph_type: type of graph to be drawn. If no type is given, an empty canvas will be drawn
        :param View view: contains plot settings
        """
        self.figure.clear()
        self.current_data = data
        self.current_view = view
        self.graph_type = graph_type

        # if the canvas is too small for one or both of the
        # graphs matplotlib will be unable to draw the graph
        # and crashes the program
        try:
            if graph_type == SURFACE_PLOT:
                self.draw_3d_plot()

            if graph_type == RASTER_IMAGE:
                self.draw_2d_plot_raster_image()

            if graph_type == APPROACH_CURVE:
                self.draw_approach_curve(data)

            self.draw()
        except ValueError:
            pass

    def redraw_graph(self):
        self.draw_graph(self.current_data, self.graph_type, self.current_view)

    def draw_white_canvas(self):
        self.figure.clear()
        self.draw()

    def show_or_hide_axes(self, data: SICMdata, axes):
        if self.current_view.axes_shown:
            x_ticks = [0, round(data.x_px / 2, 2), data.x_px]
            y_ticks = [0, round(data.y_px / 2, 2), data.y_px]
            axes.set_xticks(x_ticks)
            axes.set_yticks(y_ticks)

            if self.current_view.show_as_px:
                axis_label = "[px]"
            else:
                convert_axes_labels_from_px_to_microns(data, axes)
                axis_label = "[µm]"

            axes.set_xlabel("x dimension " + axis_label)
            axes.set_ylabel("y dimension " + axis_label)
            try:
                # 2D plots have no z label
                if self.current_view.z_in_nm:
                    axes.set_zlabel("height in nm")
                else:
                    axes.set_zlabel("height in µm")
            except:
                pass
        else:
            axes.axis(False)

    def unit_factor(self):
        return 1000.0 if self.current_view.z_in_nm else 1.0
    def draw_3d_plot(self):
        """Draws a 3d surface plot for scanning data."""

        # if the canvas is too small for one or both of the
        # graphs matplotlib will be unable to draw the graph
        # and crashes the program
        try:
            axes = self.figure.add_axes([0.1, 0.1, 0.5, 0.9], projection="3d")

            norm = Normalize(
                vmin=np.min(self.current_data.get_data()[2]),
                vmax=np.max(self.current_data.get_data()[2]),
                clip=False
            )
            if self.current_view:

                if self.current_view.z_limits:
                    norm = Normalize(
                        vmin=self.current_view.z_limits[0],
                        vmax=self.current_view.z_limits[1],
                        clip=False
                    )
                    img = axes.plot_surface(*self.current_data.get_data(), norm=norm, cmap=self.current_view.color_map)
                    axes.set_zlim(self.current_view.z_limits)
                else:
                    img = axes.plot_surface(*self.current_data.get_data(), norm=norm, cmap=self.current_view.color_map)

                axes.set_box_aspect(aspect=self.current_view.aspect_ratio)
                axes.azim = self.current_view.azim
                axes.elev = self.current_view.elev
                self.show_or_hide_axes(self.current_data, axes)

                #TODO z in nm
                #axes.set_zticklabels([tick * self.unit_factor() for tick in axes.get_zticks()])

            else:
                img = axes.plot_surface(*self.current_data.get_data(), norm=norm)
            self.set_colorbar(img, axes)
        except Exception as e:
            print(e)
            print(traceback.print_exc())

    def draw_2d_plot_raster_image(self):
        """Draws a 2D raster image for 3-dimensional scanning data."""
        axes = self.figure.add_axes([0.15, 0.1, 0.5, 0.9])

        if self.current_view:
            self.show_or_hide_axes(self.current_data, axes)
            if self.current_view.z_limits:
                img = axes.pcolormesh(
                    self.current_data.z,
                    vmin=self.current_view.z_limits[0],
                    vmax=self.current_view.z_limits[1],
                    cmap=self.current_view.color_map
                )
            else:
                img = axes.pcolormesh(self.current_data.z, cmap=self.current_view.color_map)
        else:
            img = axes.pcolormesh(self.current_data.z)

        axes.set_aspect("equal")
        self.set_colorbar(img, axes)

    def set_colorbar(self, img, axes):
        cax = inset_axes(axes,
                         width="5%",
                         height="100%",
                         loc='right',
                         borderpad=-6
                         )
        cb = self.figure.colorbar(img, cax=cax)
        z_unit = "nm" if self.current_view.z_in_nm else "µm"
        z_label = "height in " + z_unit
        cb.set_label(label=z_label)

    def draw_roi(self):
        """This function should be generalised to prevent code duplication.
        At the moment it is a quick and dirty implementation for testing
        ROIs."""
        try:
            point1 = self.view.rois[0]
            point2 = self.view.rois[1]
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
        except Exception as e:
            # TODO specify type of error
            print(type(e))

    def draw_approach_curve(self, data: SICMdata, view: View = None):
        """Plots a """
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(*data.get_data())
        if view:
            self.axes.axis(view.axes_shown)

    def bind_mouse_events_for_showing_line_profile(self,
                                                   data: SICMdata,
                                                   view: View = None,
                                                   func: Callable = None,
                                                   clean_up_func: Callable = None,
                                                   mode: str = "row"
                                                   ):
        """Draw line profile plot.

        Dev note: Maybe in the future, custom drawn lines on the plot will be supported.
        """
        self._bind_mouse_events(self._highlight_row_or_column_and_call_func, mode=mode)
        self.function_after_mouse_events = func
        self.clean_up_function = clean_up_func
        self.current_data = data
        self.current_view = view

    def bind_mouse_events_for_draw_line(self,
                                        data: SICMdata,
                                        view: View = None,
                                        func: Callable = None,
                                        clean_up_func: Callable = None,
                                        ):
        """Draw a line on image.
        TODO
        """
        self._bind_mouse_events(self._draw_a_line_on_raster_image)
        self.function_after_mouse_events = func
        self.clean_up_function = clean_up_func
        self.current_data = data
        self.current_view = view

    def bind_mouse_events_for_pixel_mouse_over(self,
                                               data: SICMdata,
                                               view: View = None,
                                               func: Callable = None,
                                               clean_up_func: Callable = None,
                                               ):
        """
        Mouse over a pixel to get the values at this point.
        """
        self._bind_mouse_events(self._mouse_over_pixel)
        self.function_after_mouse_events = func
        self.clean_up_function = clean_up_func
        self.current_data = data
        self.current_view = view

    def _mouse_over_pixel(self, event):
        """

        """
        if event.inaxes:
            x = event.xdata
            y = event.ydata

            # prevent index out of bounds exception when cursor is not in plot range
            if int(x) in range(self.current_data.z.shape[1]) and int(y) in range(self.current_data.z.shape[0]):
                if event.name == "motion_notify_event":
                    if self.mi.mouse_point1:
                        self.draw_graph(self.current_data, RASTER_IMAGE, self.current_view)
                        y_lim_upper = self.figure.get_axes()[0].get_ylim()[1]
                        text = f"x: {x:.1f}, y: {y:.1f}, z: {self.current_data.z[int(y), int(x)]:.3f}"
                        self.figure.get_axes()[0].annotate(
                            text,
                            xy=(1, y_lim_upper+0.5),
                            color="black", weight="bold",
                            fontsize=8,
                            bbox=dict(boxstyle="square,pad=0.5", fc="gray"),
                            annotation_clip=False
                        )
                        self.draw()
                    else:
                        self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

                if event.name == "button_release_event":
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events((int(event.xdata), int(event.ydata)))
                    if self.clean_up_function:
                        self.clean_up_function()
                    self.unbind_mouse_events()

    def get_viewing_angles_from_3d_plot(self):
        """Returns the viewing angles from the 3D plot.

        Values for Azimuth and Elevation angles are returned."""
        azim = self.figure.get_axes()[0].azim
        elev = self.figure.get_axes()[0].elev
        return azim, elev

    def draw_rectangle_on_raster_image(self, data: SICMdata, view: View = None, func=None, clean_up_func=None):
        self._bind_mouse_events(self._draw_rectangle_and_call_func)
        self.function_after_mouse_events = func
        self.clean_up_function = clean_up_func
        self.current_data = data
        self.current_view = view

    def _bind_mouse_events(self, func: Callable, *args, **kwargs):
        """
        Binds a callable to mouse events on the canvas.

        Also unbinds all previous events.

        Optional arguments may be passed to the MouseInteraction instance.
        The following mouse events are bound:
            - button_press_event
            - motion_notify_event
            - button_release_event
        """
        self.unbind_mouse_events()
        self.mi = MouseInteraction(*args, **kwargs)
        self.mi.cid_press = self.figure.canvas.mpl_connect('button_press_event', func)
        self.mi.cid_move = self.figure.canvas.mpl_connect('motion_notify_event', func)
        self.mi.cid_release = self.figure.canvas.mpl_connect('button_release_event', func)

    def _draw_rectangle_and_call_func(self, event):
        """Allows to draw a rectangle on the raster image canvas and calls func with
        the points which span the drawn rectangle as arguments.

        This might be used to select a ROI (region of interest) or crop the data.
        """
        if event.inaxes:
            if event.name == "button_press_event":
                self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

            if event.name == "motion_notify_event":
                if self.mi.mouse_point1 is not None:

                    self.mi.mouse_point2 = QPoint(int(event.xdata), int(event.ydata))

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

                    rect = self.get_rectangle(origin=origin, width=width, height=height)
                    self.add_rectangle_to_raster_image(rectangles=[rect])

            if event.name == "button_release_event":
                if self.mi.mouse_point1 is not None and self.mi.mouse_point2 is not None:
                    if self.mi.mouse_point1.x() <= self.mi.mouse_point2.x():
                        self.mi.mouse_point2 = self.mi.mouse_point2
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1
                    if self.mi.mouse_point1.y() <= self.mi.mouse_point2.y():
                        self.mi.mouse_point2 = self.mi.mouse_point2
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1

                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.mouse_point1, self.mi.mouse_point2)
                    if self.clean_up_function:
                        self.clean_up_function()
                    self.unbind_mouse_events()

        if not event.inaxes:
            if event.name == "button_release_event":
                if self.mi.mouse_point1 is not None and self.mi.mouse_point2 is not None:

                    if self.mi.mouse_point1.x() <= self.mi.mouse_point2.x():
                        self.mi.mouse_point2 = self.mi.mouse_point2
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1
                    if self.mi.mouse_point1.y() <= self.mi.mouse_point2.y():
                        self.mi.mouse_point2 = self.mi.mouse_point2
                    else:
                        self.mi.mouse_point1 = self.mi.mouse_point1

                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.mouse_point1, self.mi.mouse_point2)
                    if self.clean_up_function:
                        self.clean_up_function()
                    self.unbind_mouse_events()

    def _draw_a_line_on_raster_image(self, event):
        """TODO not yet finished
        Create a Line2D object from mouse coordinates and then
        add a patch to the figure axes before figure.draw.
        """
        if event.inaxes:
            if event.name == "button_press_event":
                self.mi.mouse_point1 = (event.xdata, event.ydata)

            if event.name == "motion_notify_event":
                if self.mi.mouse_point1 is not None:
                    self.mi.mouse_point2 = (event.xdata, event.ydata)
                    line = Line2D(
                        xdata=(self.mi.mouse_point1[0], self.mi.mouse_point2[0]),
                        ydata=(self.mi.mouse_point1[1], self.mi.mouse_point2[1]),
                        color="r",
                        marker="x"
                    )
                    self._add_line_to_raster_image(line)
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(
                            (self.mi.mouse_point1[0], self.mi.mouse_point2[0]),
                            (self.mi.mouse_point1[1], self.mi.mouse_point2[1])
                        )

            if event.name == "button_release_event":
                if self.mi.mouse_point1 is not None and self.mi.mouse_point2 is not None:
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(
                            (self.mi.mouse_point1[0], self.mi.mouse_point2[0]),
                            (self.mi.mouse_point1[1], self.mi.mouse_point2[1])
                        )
                    if self.clean_up_function:
                        self.clean_up_function()
                self.unbind_mouse_events()

        if not event.inaxes:
            if event.name == "button_release_event":
                if self.mi.mouse_point1 is not None and self.mi.mouse_point2 is not None:
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(
                            (self.mi.mouse_point1[0], self.mi.mouse_point2[0]),
                            (self.mi.mouse_point1[1], self.mi.mouse_point2[1])
                        )
                    if self.clean_up_function:
                        self.clean_up_function()
                self.unbind_mouse_events()

    def _highlight_row_or_column_and_call_func(self, event):
        """
        Supports selection modes "row" and "column".
        """
        if event.inaxes:
            if event.name == "motion_notify_event":
                index = -1
                rect = None

                try:
                    self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

                    if self.mi.kwargs.get("mode") == CROSS:
                        y_index = self.mi.mouse_point1.x()
                        rect1 = self.get_column_rectangle(self.mi.mouse_point1)
                        x_index = self.mi.mouse_point1.y()
                        rect2 = self.get_row_rectangle(self.mi.mouse_point1)
                        self.add_rectangle_to_raster_image(rectangles=[rect1, rect2])
                        self.function_after_mouse_events(y_index, x_index)
                    else:
                        if self.mi.kwargs.get("mode") == ROW:
                            index = self.mi.mouse_point1.y()
                            rect = self.get_row_rectangle(self.mi.mouse_point1)
                        if self.mi.kwargs.get("mode") == COLUMN:
                            index = self.mi.mouse_point1.x()
                            rect = self.get_column_rectangle(self.mi.mouse_point1)
                        if rect:
                            self.add_rectangle_to_raster_image(rectangles=[rect])
                    if self.function_after_mouse_events:
                        self.function_after_mouse_events(self.mi.kwargs.get("mode"), index)

                except Exception as e:
                    print(traceback.format_exc())
                    print(type(e))

            if event.name == "button_press_event":
                self.mi.mouse_point1 = QPoint(int(event.xdata), int(event.ydata))

            if event.name == "button_release_event":
                # remove the rectangle
                self.draw_graph(self.current_data, RASTER_IMAGE, self.current_view)
                if self.clean_up_function:
                    self.clean_up_function()
                self.unbind_mouse_events()

        if not event.inaxes:
            if event.name == "button_release_event":
                # remove the rectangle
                self.draw_graph(self.current_data, RASTER_IMAGE, self.current_view)
                if self.clean_up_function:
                    self.clean_up_function()
                self.unbind_mouse_events()

    def get_rectangle(self, origin: tuple[int, int], width: int, height: int) -> Rectangle:
        """Returns a rectangle object which can be drawn on the canvas.

        :param tuple[int, int] origin: x,y-coordinates for the origin from which
        the rectangle is drawn
        :param int width: width of the rectangle
        :param int height: height of the rectangle
        """
        return Rectangle(xy=origin, width=width, height=height,
                         fill=True, facecolor='r', alpha=0.4,
                         linewidth=2, edgecolor='r',
                         figure=self.figure
                         )

    def get_row_rectangle(self, point: QPoint) -> Rectangle or None:
        """Returns a rectangle with a height of 1 pixel.

        :param QPoint point: coordinates from which the origin
        and dimensions of the rectangle are determined
        """
        try:
            origin = (0, point.y())
            x2 = self.current_data.z.shape[1] - 1
            width = x2 + 1
            height = 1

            return self.get_rectangle(origin=origin, width=width, height=height)
        except TypeError:
            return None

    def get_column_rectangle(self, point: QPoint) -> Rectangle or None:
        """Returns a rectangle with a width of 1 pixel.

        :param QPoint point: coordinates from which the origin
        and dimensions of the rectangle are determined
        """
        try:
            origin = (point.x(), 0)
            y2 = self.current_data.z.shape[0] - 1
            width = 1
            height = y2 + 1

            return self.get_rectangle(origin=origin, width=width, height=height)
        except TypeError:
            return None

    def add_rectangle_to_raster_image(self, rectangles: list[Rectangle]):
        """Adds a rectangle shape to the current 2D plot."""
        self.draw_graph(self.current_data, RASTER_IMAGE, self.current_view)
        for rectangle in rectangles:
            self.figure.get_axes()[0].add_patch(rectangle)
            unit = " px"
            width = rectangle.get_width()
            height = rectangle.get_height()
            try:
                if not self.current_view.show_as_px:
                    if isinstance(self.current_data, sicm_analyzer.sicm_data.ScanBackstepMode):
                        unit = " µm"
                        width = rectangle.get_width() * self.current_data.micron_to_pixel_factor_x()
                        height = rectangle.get_height() * self.current_data.micron_to_pixel_factor_y()

                x_text = str(round(width, 2)) + unit
                y_text = str(round(height, 2)) + unit

                # rectangle coordinates
                rx, ry = rectangle.get_xy()
                h = rectangle.get_height()
                w = rectangle.get_width()

                # show size of rectangle inside the rectangle
                self.figure.get_axes()[0].annotate(x_text, xy=(rx+w/2, ry), color="w", weight="bold", fontsize=8)
                self.figure.get_axes()[0].annotate(y_text, xy=(rx, ry+h/2), color="w", weight="bold", fontsize=8)
            except Exception as e:
                print(e)
        self.draw()

    def _add_line_to_raster_image(self, line: Line2D):
        if isinstance(self.current_data, ScanBackstepMode):
            self.draw_graph(self.current_data, RASTER_IMAGE, self.current_view)
            self.figure.get_axes()[0].add_patch(line)
            ### TODO refactor
            if self.current_view.show_as_px:
                unit = " px"
                xx = line.get_xdata()
                yy = line.get_ydata()
            else:
                unit = " µm"
                xx = [x * self.current_data.micron_to_pixel_factor_x() for x in line.get_xdata()]
                yy = [y * self.current_data.micron_to_pixel_factor_y() for y in line.get_ydata()]

            dist = math.dist((xx[0], yy[0]), (xx[1], yy[1]))
            text = str(round(dist, 2)) + unit
            self.figure.get_axes()[0].annotate(
                text,
                xy=((line.get_xdata()[0]+line.get_xdata()[1])/2, (line.get_ydata()[0]+line.get_ydata()[1])/2),
                color="w", weight="bold", fontsize=8
            )
            self.draw()

    def unbind_mouse_events(self):
        """This function disconnects mouse events.

        The following mouse events are disconnected:
            - button_press_event
            - motion_notify_event
            - button_release_event

        Furthermore, references for function_after_mouse_event
        and MouseInteraction are set to None.
        """
        try:
            self.figure.canvas.mpl_disconnect(self.mi.cid_press)
            self.figure.canvas.mpl_disconnect(self.mi.cid_move)
            self.figure.canvas.mpl_disconnect(self.mi.cid_release)
        except AttributeError:
            pass
        self.function_after_mouse_events = None
        self.clean_up_function = None
        self.mi = None

    def draw_line_plot(self, x_data, y_data, data, view):
        """Draws a simple line plot with x and y data."""
        self.figure.clear()
        axes = self.figure.add_subplot(1, 1, 1)
        axes.plot(x_data, y_data)

        if view.show_as_px:
            axis_label = "[px]"
        else:
            convert_axes_labels_from_px_to_microns(data, axes)
            axis_label = "[µm]"

        axes.set_xlabel(f"distance {axis_label}")
        axes.set_ylabel("height [µm]")
        self.figure.tight_layout()
        self.figure.subplots_adjust(bottom=0.20, top=0.90, left=0.15, right=0.75)
        self.draw()

    def draw_xy_line_profiles(self, x_x_data, x_y_data, y_x_data, y_y_data, data, view):
        self.figure.clear()
        axes = self.figure.add_subplot(1, 1, 1)
        axes.plot(x_x_data, x_y_data, label="row")
        axes.plot(y_x_data, y_y_data, label="column")

        # TODO test what happens if x pixel dimension differs from y
        if view.show_as_px:
            axis_label = "[px]"
        else:
            convert_axes_labels_from_px_to_microns(data, axes)
            axis_label = "[µm]"

        axes.set_xlabel(f"distance {axis_label}")
        axes.set_ylabel("height [µm]")

        self.figure.legend(loc=7)
        self.figure.tight_layout()
        self.figure.subplots_adjust(bottom=0.20, top=0.90, left=0.15, right=0.75)
        self.draw()
