import unittest
import numpy as np
from pySICM_Analysis.manipulate_data import filter_median_spatial, filter_average_spatial, filter_average_temporal, filter_median_temporal


class DataManipulationFilterTests(unittest.TestCase):

    def setUp(self):
        self.shape = (5, 3)
        self.data = np.zeros(shape=self.shape)

    def test_shape_is_unchanged_after_filter_median_temporal(self):
        arr = filter_median_temporal(self.data)
        self.assertEqual(arr.shape, self.shape)

    def test_filter_median_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_median_temporal(arr_data, 1)
        np.testing.assert_array_equal(result, expected)

    def test_filter_median_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_median_temporal(arr_data, 2)
        np.testing.assert_array_equal(result, expected)

    def test_shape_is_unchanged_after_filter_median_spatial(self):
        arr = filter_median_spatial(self.data)
        self.assertEqual(arr.shape, self.shape)

    def test_filter_median_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_median_spatial(arr_data, 1)
        np.testing.assert_array_equal(result, expected)

    def test_filter_median_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_median_spatial(arr_data, 2)
        np.testing.assert_array_equal(result, expected)

    def test_shape_is_unchanged_after_filter_average_temporal(self):
        arr = filter_average_temporal(self.data)
        self.assertEqual(arr.shape, self.shape)

    def test_filter_average_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_average_temporal(arr_data, 1)
        np.testing.assert_array_equal(result, expected)

    def test_filter_average_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_average_temporal(arr_data, 2)
        np.testing.assert_array_equal(result, expected)

    def test_shape_is_unchanged_after_filter_average_spatial(self):
        arr = filter_average_spatial(self.data)
        self.assertEqual(arr.shape, self.shape)

    def test_filter_average_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_average_spatial(arr_data, 1)
        np.testing.assert_array_equal(result, expected)

    def test_filter_average_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        expected = np.array(expected, dtype=float).reshape(shape)
        arr_data = np.array(test_data, dtype=float).reshape(shape)
        result = filter_average_spatial(arr_data, 2)
        np.testing.assert_array_equal(result, expected)
