import os
import tarfile
from unittest import TestCase
import numpy as np
from sicm_analyzer.sicm_data import get_data_as_bytes
from sicm_analyzer.sicm_data import SICMDataFactory, get_name_of_tar_member_containing_scan_data


class SicmDataExport(TestCase):

    def test_data_to_bytes(self):
        cwd = os.getcwd()
        testfile = os.path.join(cwd, "tests/sample_sicm_files/Zelle1 PFA.sicm")
        sicm = SICMDataFactory().get_sicm_data(testfile)
        data = self.get_raw_data_from_file()
        raw_data = np.array(data)
        converted_bytes = get_data_as_bytes(sicm)
        new_bytes = np.array(converted_bytes)
        np.testing.assert_array_equal(raw_data, new_bytes)

    def get_raw_data_from_file(self):
        data = []
        cwd = os.getcwd()
        testfile = os.path.join(cwd, "tests/sample_sicm_files/Zelle1 PFA.sicm")
        tar = tarfile.open(testfile, "r:gz")
        name = get_name_of_tar_member_containing_scan_data(tar)
        if name:
            data_file = tar.extractfile(tar.getmember(name))
            two_bytes = data_file.read(2)
            while two_bytes:
                data.append(two_bytes)
                two_bytes = data_file.read(2)
        return data
