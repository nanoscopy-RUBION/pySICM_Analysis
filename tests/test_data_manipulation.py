import unittest

import numpy as np

from sicm_analyzer.manipulate_data import filter_median_spatial, filter_average_spatial, filter_average_temporal, filter_median_temporal
from sicm_analyzer.manipulate_data import transpose_z_data
from sicm_analyzer.sicm_data import ScanBackstepMode
from sicm_analyzer.view import View


class DataManipulationFilterTests(unittest.TestCase):

    def setUp(self):
        self.test_data = ScanBackstepMode()
        self.expected_data = ScanBackstepMode()

    def tearDown(self):
        self.test_data = None
        self.expected_data = None

    def test_shape_is_unchanged_after_filter_median_temporal(self):
        shape = (2, 4)
        data = np.zeros(shape=shape)
        self.test_data.z = data
        filter_median_temporal(self.test_data)
        self.assertEqual(self.test_data.z.shape, shape)

    def test_filter_median_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_median_temporal(self.test_data, 1)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_filter_median_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_median_temporal(self.test_data, 2)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_shape_is_unchanged_after_filter_median_spatial(self):
        shape = (7, 4)
        data = np.zeros(shape=shape)
        self.test_data.z = data
        filter_median_spatial(self.test_data)
        self.assertEqual(self.test_data.z.shape, shape)

    def test_filter_median_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_median_spatial(self.test_data, 1)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_filter_median_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_median_spatial(self.test_data, 2)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_shape_is_unchanged_after_filter_average_temporal(self):
        shape = (11, 14)
        data = np.zeros(shape=shape)
        self.test_data.z = data
        filter_average_temporal(self.test_data)
        self.assertEqual(self.test_data.z.shape, shape)

    def test_filter_average_temporal_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1.5, 2, 3, 4, 5, 6, 7, 7.5]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_average_temporal(self.test_data, 1)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_filter_average_temporal_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [2, 2.5, 3, 4, 5, 6, 6.5, 7]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_average_temporal(self.test_data, 2)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_shape_is_unchanged_after_filter_average_spatial(self):
        shape = (7, 9)
        data = np.zeros(shape=shape)
        self.test_data.z = data
        filter_average_spatial(self.test_data)
        self.assertEqual(self.test_data.z.shape, shape)

    def test_filter_average_spatial_with_l_1(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_average_spatial(self.test_data, 1)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

    def test_filter_average_spatial_with_l_2(self):
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = [3.5, 4, 5, 5.5, 3.5, 4, 5, 5.5]
        shape = (2, 4)
        self.test_data.z = np.array(test_data, dtype=float).reshape(shape)
        self.expected_data.z = np.array(expected, dtype=float).reshape(shape)

        filter_average_spatial(self.test_data, 2)
        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)


class DataManipulationSimpleTests(unittest.TestCase):
    def setUp(self):
        self.test_data = ScanBackstepMode()
        self.expected_data = ScanBackstepMode()

    def tearDown(self):
        self.test_data = None
        self.expected_data = None

    def test_tranpose_z_function_returns_correct_data_type(self):
        shape = (4, 4)
        self.test_data.z = np.zeros(shape)
        self.expected_data.z = np.zeros(shape)
        transpose_z_data(self.test_data)
        self.assertIsInstance(self.test_data.z, type(self.expected_data.z))

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
        self.test_data.z = test_data

        expected_data = np.array(expected_data)
        expected_data = expected_data.reshape(shape)
        self.expected_data.z = expected_data

        transpose_z_data(self.test_data)

        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)

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
        self.test_data.z = test_data

        expected_data = np.array(expected_data)
        expected_data = expected_data.reshape(expected_shape)
        self.expected_data.z = expected_data

        transpose_z_data(self.test_data)

        np.testing.assert_array_equal(self.test_data.z, self.expected_data.z)
