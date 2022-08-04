"""
This module (pySICM Viewer) is used to visualize SICM (scanning ion conductance
microscopy) data obtained with the homemade setup of the microscope in our lab:
Group: nanoscopy
Ruhr University Bochum, RUBION, Universitätsstr. 150, 44801 Bochum
The software to operate the microscope and to obtain data (pySICM) has been
written by Patrick Happel.
"""

import tarfile
from tarfile import TarFile
import json
from typing import Any
from dataclasses import dataclass
import numpy as np
import struct


APPROACH = "approach"
BACKSTEP = "backstepScan"
SETTINGS = "settings.json"
MODE = ".mode"
INFO = ".info"
Xpx = "x-px"
Ypx = "y-px"


@dataclass
class SICMdata:
    """
    Class for loading pySICM data.
    Supports only the .sicm file format used by pySICM. Depending on the scan mode
    that was used, scan data can be 2D (approach curves) or 3D (scan of an area).
    Some information on the supported file format (.sicm):
    '.sicm' files are gzipped tar archives containing several files:
        - .mode: Byte file that contains the operation mode of the microscope used
                 to obtain data.
        - <FILENAME>: the actual measurement data. This is a binary file containing
                      unsigned 16-bit integers (little endian!).
        - <FILENAME>.info: Some information on scan times.
        - settings.json: A JSON file containing scan settings.
    """
    # TODO make normal class and initialize class fields
    def __init__(self):
        self.x: np.ndarray
        self.y: np.ndarray
        self.z: np.ndarray
        self.scan_mode: str
        self.info: dict
        self.settings: dict

    def plot(self):
        """TODO add doc string"""
        pass


class ApproachCurve(SICMdata):
    """TODO add doc string"""

    def set_plot_values(self, data: list[int]):
        """TODO add doc string"""
        self.x = np.array(range(len(data)))
        self.z = np.array(data)

    def plot(self):
        """TODO add doc string"""
        return self.x, self.z

    def get_tip_openeing_diameter(self):
        """TODO add doc string"""
        print("not yet implemented")


class ScanBackstepMode(SICMdata):
    """TODO add doc string"""

    def __init__(self):
        super(ScanBackstepMode, self).__init__()

    def set_plot_values(self, data: list[int]):
        """Rearranges scan data for 3-dimensional plotting."""
        x_px = int(self.settings[Xpx])
        y_px = int(self.settings[Ypx])
        self.z = np.reshape(data, (x_px, y_px))
        self.x, self.y = np.meshgrid(range(x_px), range(y_px))

    def plot(self):
        """TODO add doc string"""
        return self.x, self.y, self.z


class SICMDataFactory:
    """
    Factory to return SICMData objects according to the scan mode.
    """
    def get_sicm_data(self, file_path: str):
        """Read all data from the tar-like .sicm-file format"""
        tar = tarfile.open(file_path, "r:gz")

        scan_mode = get_sicm_mode(tar)
        info = get_sicm_info(tar)
        settings = get_sicm_settings(tar)
        data = read_byte_data(tar)

        if scan_mode == BACKSTEP:
            sicm_data = ScanBackstepMode()
        else:
            sicm_data = ApproachCurve()

        sicm_data.scan_mode = scan_mode
        sicm_data.settings = settings
        sicm_data.info = info
        sicm_data.set_plot_values(data)

        return sicm_data


def read_byte_data(tar: TarFile) -> list[tuple[Any, ...]]:
    """Return z data from file as list"""
    data = []
    name = get_name_of_tar_member_containing_scan_data(tar)
    if name:
        data_file = tar.extractfile(tar.getmember(name))
        two_bytes = data_file.read(2)
        while two_bytes:
            data.append(struct.unpack('<H', two_bytes))
            two_bytes = data_file.read(2)
    return data


def get_sicm_mode(tar: TarFile) -> str:
    """Return a string representation of the scan mode.
    The scan mode can be found in the file '.mode' which is part
    of the .sicm "tar" file. '.mode' is a binary file. The return type, however,
    is str.
    At the moment, two modes are supported:
    - approach: Measurement of an approach curve
    - backstepMode: SICM scan using the backstep mode
    More modes can be added by extending the 'MODES' dictionary.
    """
    return str(tar.extractfile(tar.getmember(MODE)).readline(), "utf-8")


def get_name_of_tar_member_containing_scan_data(tar: TarFile) -> str:
    """Return the TarFile member which has no file extension in its name.
    .sicm files contain four files. One of which has no file extension and
    contains the actual measurement as 16bit integer (unsigned, little-endian).
    """
    file_extensions = (".mode", ".json", ".info")
    file_name = None
    for member in tar.getmembers():
        if not member.name.endswith(file_extensions):
            file_name = member.name
    return file_name


def get_sicm_info(tar: TarFile) -> dict:
    """Return content of info file as dictionary."""
    settings = {}
    for member in tar.getmembers():
        if member.name.endswith(INFO):
            settings = json.load(tar.extractfile(tar.getmember(member.name)))
    return settings


def get_sicm_settings(tar: TarFile) -> dict:
    """Return content of settings.json file as dictionary."""
    return json.load(tar.extractfile(tar.getmember(SETTINGS)))