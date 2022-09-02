from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
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

        cb = self.figure.colorbar(img)
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


