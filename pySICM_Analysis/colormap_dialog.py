def menu_action_view_colormap(self):
    """Opens a dialog to select a predefined
    colormap or to create a custome one.
    """
    # TODO open a dialog

    self.currentView.change_color_map(self._get_new_color_map())
    self.update_figures_and_status(self.currentView, self.currentData)


def _get_new_color_map(self):
    """Color map creation should be placed in a
    seperate class.
    """
    viridis = cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    pink = np.array([10 / 256, 10 / 256, 10 / 256, 1])
    newcolors[:25, :] = pink
    newmap = ListedColormap(newcolors)

    N = 256
    vals = np.ones((N, 4))
    # custom_map = ListedColormap(cus_colors)
    return cm.get_cmap('viridis', 256)