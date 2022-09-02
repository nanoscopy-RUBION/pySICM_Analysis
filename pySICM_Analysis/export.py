from matplotlib import pyplot as plt


def export_file():
    """TODO implementation
    Exports the current view object as ... file.
    Need to think about the file format. .sicm might not be
    suitable after manipulating the data """
    # json to store metadata
    print("TODO: Export to file")


def export_top_plot_as_svg(figure):
    """Helper function for setting up which part
    of the plot should be saves."""
    ax = figure.get_axes()[0]
    # Save just the portion _inside_ the second axis's boundaries
    extent = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    figure.savefig('../tests/outputs/ax2_figure.svg', bbox_inches=extent)

    # Pad the saved area by 10% in the x-direction and 20% in the y-direction
    figure.savefig('../tests/outputs/ax2_figure_expanded.svg', bbox_inches=extent.expanded(1.1, 1.2))


def menu_action_export_bitmap():
    # TODO filedialog for saving

    self.canvas.figure.savefig(fname="testfigure.svg", format="svg")
    self.export_top_plot_as_svg()
    print("TODO: Export as bitmap")


def menu_action_export_vector():
    print("TODO: Export as pdf")
