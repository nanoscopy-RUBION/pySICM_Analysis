from unittest import TestCase
import numpy as np
from sicm_analyzer.measurements import get_roughness, root_mean_square_error
from sicm_analyzer.sicm_data import SICMdata, get_sicm_data


class RoughnessTests(TestCase):

    def test_calculate_rmse_simple_data(self):
        data = [2, 3, 4, 2]
        arr = np.array(data)
        data = np.reshape(arr, (2, 2))
        expected_rmse = 0.8291562  # calculated by hand
        self.assertAlmostEqual(root_mean_square_error(data), expected_rmse, delta=0.001)

    def test_calculate_rmse_full_scan(self):
        """Expected rmse was calculated with excel."""
        data = np.array([
            [43.078, 46.24, 33.021, 33.698, 35.607, 36.882, 37.396, 37.931, 37.58, 40.768],
            [34.158, 32.564, 33.006, 33.73, 35.236, 36.396, 39.592, 37.492, 36.79, 36.016],
            [32.4, 32.793, 33.068, 33.641, 34.609, 37.789, 35.898, 35.782, 38.02, 41.211],
            [32.572, 32.922, 33.24, 33.898, 34.247, 34.625, 37.832, 34.65, 34.55, 34.388],
            [32.56, 32.795, 33.269, 33.499, 33.525, 33.738, 34.495, 34.498, 34.133, 33.177],
            [32.56, 35.36, 33.151, 35.337, 38.541, 33.158, 36.073, 33.889, 37.132, 31.806],
            [32.241, 35.451, 37.297, 32.015, 31.981, 32.595, 33.206, 33.132, 36.34, 31.47],
            [40.243, 31.907, 31.703, 31.391, 30.865, 34.059, 32.611, 35.506, 38.012, 33.209],
            [40.523, 43.567, 31.469, 31.5, 31.219, 31.521, 34.571, 32.068, 35.263, 38.45],
            [31.39, 34.592, 37.69, 31.884, 35.096, 30.807, 31.583, 31.443, 31.098, 33.845]
        ])
        data = data
        #data = data - np.min(data)
        z = np.reshape(data, (10, 10))
        x = np.linspace(0, 9, num=10)
        y = np.linspace(0, 45, num=10)
        x, y = np.meshgrid(x, y)

        sicm_data = SICMdata()
        sicm_data.x = x
        sicm_data.y = y
        sicm_data.z = z

        print(get_roughness(sicm_data))

    def test_calculate_roughness(self):
        path = "./tests/sample_sicm_files/Zelle3 PFA.sicm"
        sicm_data = get_sicm_data(path)
        print(get_roughness(sicm_data))

    def test_calculate_roughness_2(self):
        path = "./tests/sample_sicm_files/Zelle2 PFA.sicm"
        sicm_data = get_sicm_data(path)
        print(get_roughness(sicm_data))

    def test_calculate_roughness_3(self):
        path = "./tests/sample_sicm_files/Zelle3 30x30_30 PFA.sicm"
        sicm_data = get_sicm_data(path)
        print(get_roughness(sicm_data))

    def test_calculate_roughness_4(self):
        path = "./tests/sample_sicm_files/Zelle2Membran PFA.sicm"
        sicm_data = get_sicm_data(path)
        print(get_roughness(sicm_data))