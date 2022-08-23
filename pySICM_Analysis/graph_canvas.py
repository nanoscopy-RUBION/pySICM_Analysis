from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from sicm_data import ScanBackstepMode, ApproachCurve


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
        If the data is from a backstep scan, a 3D plot . Plotting data and details are based upon the

        :param view_object: View object which contains the data and display settings for the graph
        """
        self.figure.clear()
        if isinstance(view_object.sicm_data, ScanBackstepMode):
            self.axes = self.figure.add_subplot(2, 1, 1, projection='3d')
            plot = self.axes.plot_surface(*view_object.get_modified_data(), cmap=view_object.color_map)

            self.figure.get_axes()[0].azim = view_object.azim
            self.figure.get_axes()[0].elev = view_object.elev
            self.figure.get_axes()[0].proj_type = 'ortho'
            self.axes.axis(view_object.axes_shown)
            self.figure.colorbar(plot)

            ax = self.axes = self.figure.add_subplot(2, 1, 2)
            # use pcolormesh for scalable pixelmaps
            # img = self.axes.pcolormesh(view_data.z_data, cmap=view_data.color_map)
            img = self.axes.imshow(view_object.z_data, cmap=view_object.color_map)
            self.axes.axis(view_object.axes_shown)
            self.figure.colorbar(img)

        if isinstance(view_object.sicm_data, ApproachCurve):
            self.axes = self.figure.add_subplot(111)
            self.axes.plot(*view_object.get_modified_data())
            self.axes.axis(view_object.axes_shown)

        self.figure.tight_layout()
        self.draw()

    def get_viewing_angles_from_3d_plot(self):
        azim = self.figure.get_axes()[0].azim
        elev = self.figure.get_axes()[0].elev
        return azim, elev
