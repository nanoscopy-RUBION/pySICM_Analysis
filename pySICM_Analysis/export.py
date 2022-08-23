from matplotlib import pyplot as plt


def export_file():
    """TODO implementation
    Exports the current view object as ... file.
    Need to think about the file format. .sicm might not be
    suitable after manipulating the data """
    # json to store metadata
    print("TODO: Export to file")


def _figure_save_configuration(self):
    """Helper function for setting up which part
    of the plot should be saves."""
    fig = self.canvas.figure
    ax = fig.get_axes()[0]
    # Save just the portion _inside_ the second axis's boundaries
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('ax2_figure.svg', bbox_inches=extent)

    # Pad the saved area by 10% in the x-direction and 20% in the y-direction
    fig.savefig('ax2_figure_expanded.svg', bbox_inches=extent.expanded(1.1, 1.2))


def menu_action_export_bitmap():
    # TODO filedialog for saving

    self.canvas.figure.savefig(fname="testfigure.svg", format="svg")
    self._figure_save_configuration()
    print("TODO: Export as bitmap")


def menu_action_export_vector():
    print("TODO: Export as pdf")
