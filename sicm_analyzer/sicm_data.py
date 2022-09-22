"""This module handles import of raw data obtained from our custom build scanning
ion conductance microsope (SICM) which was recorded with the homebrew software pySICM.
pySICM recordings are stored in a custom file format: .sicm

Some information on the supported file format (.sicm):
    '.sicm' files are gzipped tar archives containing several files:
        - .mode: Byte file that contains the operation mode of the microscope used
                 to obtain data.
        - <FILENAME>: the actual measurement data. This is a binary file containing
                      unsigned 16-bit integers (little endian!).
        - <FILENAME>.info: Some information on scan times.
        - settings.json: A JSON file containing scan settings.

It is planned to support multiple scanning modes. At this moment (2022-09-05)
only approach curves and backstep scans are supported. A factory class which takes
the file path as an argument enables import of .sicm files and returns an object
of either ApproachCurve or ScanBackstepMode.
"""
import os
import tarfile
from tarfile import TarFile
import json
import numpy as np
import struct

APPROACH = "approach"
BACKSTEP = "backstepScan"
SETTINGS = "settings.json"
MODE = ".mode"
INFO = ".info"
Xpx = "x-px"
Ypx = "y-px"
X_size = "x-Size"
Y_size = "y-Size"


class SICMdata:
    """
    This class works as an interface for SICM data recorded in different scan modes.
    Each scan mode should be implemented as a subclass inheriting from SICMdata.
    set_data() should be overridden in the subclass to set the correct data fields.
    Data fields in all three dimensions represent numpy arrays.
    """
    def __init__(self):
        # data containing fields
        self.x: np.ndarray = np.zeros(1)
        self.y: np.ndarray = np.zeros(1)
        self.z: np.ndarray = np.zeros(1)
        # metadata fields
        self.x_size: int = 0
        self.y_size: int = 0
        self.z_size: int = 0
        self.x_px: int = 0
        self.y_px: int = 0
        self.z_px: int = 0
        self.scan_mode: str = ""
        self.info: dict = {}
        self.settings: dict = {}

    def set_settings(self, settings: dict):
        """Sets metadata obtained from settings.json
        and .mode."""
        pass

    def get_data(self):
        """Returns x and z data for ApproachCurves and
         x, y and z for Scan data."""
        pass


class ApproachCurve(SICMdata):
    """ApproachCurves are two-dimensional data sets.
     Therefore, data is stored in x and z fields."""

    def __init__(self):
        super(ApproachCurve, self).__init__()

    def set_data(self, data: list[int]):
        self.x = np.array(range(len(data)))
        self.y = np.zeros(1)
        self.z = np.array(data)

    def get_data(self):
        return self.x, self.z


class ScanBackstepMode(SICMdata):
    """TODO add doc string"""

    def __init__(self):
        super(ScanBackstepMode, self).__init__()

    def set_settings(self, settings: dict):
        self.settings = settings
        self.x_px = int(settings[Xpx])
        self.y_px = int(settings[Ypx])
        try:
            self.x_size = int(settings[X_size])
            self.y_size = int(settings[Y_size])
        except ValueError as e:
            # there seem to be cases in which no x_size value is set in settings.json
            print("No x_size or y_size value in settings.json.")
            self.x_size = self.x_px
            self.y_size = self.y_px

    def set_data(self, data: list[int]):
        """Rearranges scan data for 3-dimensional plotting."""
        self.z = np.reshape(data, (self.x_px, self.y_px)) / 1000  # to have z data in µm instead of nm
        self.x, self.y = np.meshgrid(range(self.x_px), range(self.y_px))

    def get_data(self):
        """"""
        return self.x, self.y, self.z


class SICMDataFactory:
    """
    Factory to return SICMData objects according to the scan mode.
    """
    def get_sicm_data(self, file_path: str) -> SICMdata:
        """Read all data from the tar-like .sicm-file format"""
        tar = tarfile.open(file_path, "r:gz")
        scan_mode = get_sicm_mode(tar)
        info = get_sicm_info(tar)
        settings = get_sicm_settings(tar)
        data = read_byte_data(tar)

        if scan_mode == BACKSTEP:
            sicm_data = ScanBackstepMode()
        elif scan_mode == APPROACH:
            sicm_data = ApproachCurve()
        else:
            sicm_data = SICMdata()

        sicm_data.scan_mode = scan_mode
        sicm_data.set_settings(settings)

        sicm_data.info = info
        sicm_data.set_data(data)

        return sicm_data


def read_byte_data(tar: TarFile) -> list[int]:
    """Return z data from file as list"""
    data = []
    name = get_name_of_tar_member_containing_scan_data(tar)
    if name:
        data_file = tar.extractfile(tar.getmember(name))
        two_bytes = data_file.read(2)
        while two_bytes:
            pack = struct.unpack('<H', two_bytes)
            data.append(pack[0])
            two_bytes = data_file.read(2)
    return data


def get_data_as_bytes(data: SICMdata):
    """Packs and returns data as list of bytes.

    """
    z_data = data.z.flatten("C") * 1000
    byte_data = []
    for pixel in z_data:
        byte_data.append(struct.pack("<H", int(pixel)))
    return byte_data


def export_sicm_file(file_to_save, sicm_data: SICMdata):
    """

    """
    temporary_files_for_sicm_data_package(sicm_data)
    create_targz_from_list_of_files(file_to_save)
    _clear_temporary_files()


def temporary_files_for_sicm_data_package(sicm_data: SICMdata):
    """Writes all necessary files for the sicm file format package.
    """
    path = os.getcwd()

    with open(os.path.join(path, "cropped.info"), "w") as f:
        json.dump(sicm_data.info, f)
        f.close()
    with open(os.path.join(path, ".mode"), "w") as f:
        f.write(sicm_data.scan_mode)
        f.close()
    x_px, y_px = sicm_data.z.shape
    old_x_px = sicm_data.x_px
    old_y_px = sicm_data.y_px

    sicm_data.settings["x-px"] = str(x_px)
    sicm_data.settings["y-px"] = str(y_px)

    sjson = json.dumps(sicm_data.settings, separators=(',', ':'))
    with open(os.path.join(path, "settings.json"), "w") as f:
        f.write(sjson)
        f.close()
    sicm_data.settings["x-px"] = old_x_px
    sicm_data.settings["y-px"] = old_y_px
    byte_data = get_data_as_bytes(sicm_data)

    with open(os.path.join(path, "cropped"), "wb") as f:
        for byte in byte_data:
            f.write(byte)
        f.close()


def create_targz_from_list_of_files(filename: str):
    """Writes a tar.gz file and adds a list of files to it.

    filename: a string cocntaining the file path and file name
    """
    files = ["cropped.info", "cropped", ".mode", "settings.json"]
    path = os.getcwd()
    with tarfile.open(filename, "w:gz") as tar:
        for f in files:
            tar.add(os.path.join(path, f), arcname=f)
        tar.close()


def _clear_temporary_files():
    """Deletes all four temporary files which were
    created during sicm data export."""
    try:
        os.remove("cropped.info")
        os.remove(".mode")
        os.remove("settings.json")
        os.remove("cropped")
    except OSError:
        print("Error - File was not deleted")

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
