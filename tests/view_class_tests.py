import unittest

from pySICM_Analysis.graph_canvas import GraphCanvas
from pySICM_Analysis.sicm_data import SICMDataFactory
from pySICM_Analysis.view import View


class ViewDataTests(unittest.TestCase):

    def setUp(self):
        sicm_file = "./test_sicm_files/Zelle1 PFA.sicm"
        self.data = SICMDataFactory().get_sicm_data(sicm_file)
        self.graph = GraphCanvas()
        self.graph.update_plots(View(self.data))

    def tearDown(self):
        pass

    def test_x_axis_label_conversion_from_px_to_microns(self):
        x_px = 10
        x_size = 50

        size_px_ratio = x_size / x_px
        if x_px < x_size:
            ticks = self.graph.figure.get_axes()[1].get_xticks()
            labels = []
            for tick in ticks:
                label = round(tick * size_px_ratio, 2)
                labels.append(label)
        if x_px > x_size:
            ticks = self.graph.figure.get_axes()[1].get_xticks()
            labels = []
            for tick in ticks:
                label = round(tick * size_px_ratio, 2)
                labels.append(label)

        x_ticks = self.graph.figure.get_axes()[1].get_xticks()
        x_ticklabels = self.graph.figure.get_axes()[1].get_xticklabels()


        print(f"x_tick: {x_ticks}")
        print(f"x_labels: {x_ticklabels}")
