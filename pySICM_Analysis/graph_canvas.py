from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from pySICM_Analysis.sicm_data import ScanBackstepMode, ApproachCurve


class GraphCanvas(FigureCanvasQTAgg):
    """Canvas for drawing graphs from .sicm data."""

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def update_plots(self, view_object):
        """
        Redraws plots on the canvas.
        If the data is from an approach curve, a single 2D plot will be displayed.
        If the data is from a backstep scan, a 3D plot .
        Plotting data and details are based upon the

        :param view_object: View object which contains the data and display settings for the graph
        """
        self.figure.clear()
        if isinstance(view_object.sicm_data, ScanBackstepMode):
            if view_object.show_as_px:
                axis_label = "px"
            else:
                axis_label = "µm"

            self.axes = self.figure.add_subplot(2, 1, 1, projection='3d')
            self.axes.plot_surface(*view_object.get_modified_data(), cmap=view_object.color_map)

            self.figure.get_axes()[0].azim = view_object.azim
            self.figure.get_axes()[0].elev = view_object.elev
            self.figure.get_axes()[0].proj_type = 'ortho'
            self.axes.axis(view_object.axes_shown)

            self.axes.set_xlabel(axis_label)
            self.axes.set_ylabel(axis_label)

            self.axes = self.figure.add_subplot(2, 1, 2)
            # use pcolormesh for scalable pixelmaps
            img = self.axes.pcolormesh(view_object.z_data, cmap=view_object.color_map)
            #img = self.axes.imshow(view_object.z_data, cmap=view_object.color_map)
            self.axes.set_aspect("equal")
            self.axes.axis(view_object.axes_shown)

            self.axes.set_xlabel(axis_label)
            self.axes.set_ylabel(axis_label)

            # TEST
            if not view_object.show_as_px:
                x_size = view_object.sicm_data.x_size
                x_px = view_object.sicm_data.x_px
                y_size = view_object.sicm_data.y_size
                y_px = view_object.sicm_data.y_px
                x_ticks = self.figure.get_axes()[1].get_xticks()
                y_ticks = self.figure.get_axes()[1].get_yticks()
                if x_px != x_size:
                    self.axes.set_xticklabels(self.get_tick_labels_in_microns(x_ticks, x_px, x_size))
                if y_px != y_size:
                    self.axes.set_yticklabels(self.get_tick_labels_in_microns(y_ticks, y_px, y_size))
            # ENDTEST

            cb = self.figure.colorbar(img)
            cb.set_label(label="height in µm")

        if isinstance(view_object.sicm_data, ApproachCurve):
            self.axes = self.figure.add_subplot(111)
            self.axes.plot(*view_object.get_modified_data())
            self.axes.axis(view_object.axes_shown)

        self.figure.tight_layout()
        self.draw()

    def get_tick_labels_in_microns(self, ticks, n_px, n_size):
        labels = []
        if n_px != n_size:
            for tick in ticks:
                label = round(tick * (n_size / n_px), 2)
                labels.append(label)
        return labels

    def draw_3d_plot(self, view_object):
        """Draws a 3d surface plot."""
        pass

    def draw_2d_plot(self, view_object):
        pass

    def draw_line_profile(self, view_object, *args):
        print(*args)

    def get_viewing_angles_from_3d_plot(self):
        azim = self.figure.get_axes()[0].azim
        elev = self.figure.get_axes()[0].elev
        return azim, elev


