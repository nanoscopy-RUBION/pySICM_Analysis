import copy
import unittest
import numpy as np
from pySICM_Analysis.manipulate_data import filter_median_spatial, filter_average_spatial, filter_average_temporal, filter_median_temporal
from pySICM_Analysis.manipulate_data import transpose_z_data, subtract_z_minimum
from pySICM_Analysis.view import View


class DataManipulationFilterTests(unittest.TestCase):

    def setUp(self):
        self.test_view = View(None)
        self.expected_view = View(None)

    def tearDown(self):
        self.test_view = None
        self.expected_view = None

    def test_shape_is_unchanged_after_filter_median_temporal(self):
        shape = (2, 4)
        data = np.zeros(shape=shape)
        self.test_view.z_data = data
        filter_median_temporal(self.test_view)
        self.assertEqual(self.test_view.z_data.shape, shape)

    def test_filter_median_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_median_temporal(self.test_view, 1)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_filter_median_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_median_temporal(self.test_view, 2)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_shape_is_unchanged_after_filter_median_spatial(self):
        shape = (7, 4)
        data = np.zeros(shape=shape)
        self.test_view.z_data = data
        filter_median_spatial(self.test_view)
        self.assertEqual(self.test_view.z_data.shape, shape)

    def test_filter_median_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_median_spatial(self.test_view, 1)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_filter_median_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_median_spatial(self.test_view, 2)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_shape_is_unchanged_after_filter_average_temporal(self):
        shape = (11, 14)
        data = np.zeros(shape=shape)
        self.test_view.z_data = data
        filter_average_temporal(self.test_view)
        self.assertEqual(self.test_view.z_data.shape, shape)

    def test_filter_average_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_average_temporal(self.test_view, 1)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_filter_average_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_average_temporal(self.test_view, 2)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_shape_is_unchanged_after_filter_average_spatial(self):
        shape = (7, 9)
        data = np.zeros(shape=shape)
        self.test_view.z_data = data
        filter_average_spatial(self.test_view)
        self.assertEqual(self.test_view.z_data.shape, shape)

    def test_filter_average_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_average_spatial(self.test_view, 1)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_filter_average_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        self.test_view.z_data = np.array(test_data, dtype=float).reshape(shape)
        self.expected_view.z_data = np.array(expected, dtype=float).reshape(shape)

        filter_average_spatial(self.test_view, 2)
        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)


class DataManipulationSimpleTests(unittest.TestCase):
    def setUp(self):
        self.test_view = View(None)
        self.expected_view = View(None)

    def tearDown(self):
        self.test_view = None
        self.expected_view = None

    def test_tranpose_z_function_returns_correct_data_type(self):
        shape = (4, 4)
        self.test_view.z_data = np.zeros(shape)
        self.expected_view.z_data = np.zeros(shape)
        transpose_z_data(self.test_view)
        self.assertIsInstance(self.test_view.z_data, type(self.expected_view.z_data))

    def test_square_shaped_transpose_z(self):
        test_data = [
            1, 2, 3, 4,
            5, 6, 7, 8,
            9, 1, 2, 3,
            4, 5, 6, 7
        ]
        expected_data = [
            1, 5, 9, 4,
            2, 6, 1, 5,
            3, 7, 2, 6,
            4, 8, 3, 7
        ]
        shape = (4, 4)

        test_data = np.array(test_data)
        test_data = test_data.reshape(shape)
        self.test_view.z_data = test_data

        expected_data = np.array(expected_data)
        expected_data = expected_data.reshape(shape)
        self.expected_view.z_data = expected_data

        transpose_z_data(self.test_view)

        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)

    def test_n_x_m_shaped_transpose_z(self):
        test_data = [
            1, 2, 3, 4,
            5, 6, 7, 8,
        ]
        expected_data = [
            1, 5,
            2, 6,
            3, 7,
            4, 8
        ]
        test_shape = (2, 4)
        expected_shape = (4, 2)

        test_data = np.array(test_data)
        test_data = test_data.reshape(test_shape)
        self.test_view.z_data = test_data

        expected_data = np.array(expected_data)
        expected_data = expected_data.reshape(expected_shape)
        self.expected_view.z_data = expected_data

        transpose_z_data(self.test_view)

        np.testing.assert_array_equal(self.test_view.z_data, self.expected_view.z_data)
