"""This module handles import of raw data obtained from our custom build scanning
ion conductance microscope (SICM) which was recorded with the homebrew software pySICM.
pySICM recordings are stored in a custom file format: .sicm

Some information on the supported file format (.sicm):
    '.sicm' files are gzipped tar archives containing several files:
        - .mode: Byte file that contains the operation mode of the microscope used
                 to obtain data.
        - <FILENAME>: the actual measurement data. This is a binary file containing
                      unsigned 16-bit integers (little endian!).
        - <FILENAME>.info: Some information on scan times.
            client_start_time = datetime.datetime.now()
            client_start_timestamp = int(round(time.time() * 1e3))
            client_end_timestamp = int(round(time.time() * 1e3))
            client_duration = client_end_timestamp - client_start_timestamp
            This means that the scan duration is saved as milliseconds
        - settings.json: A JSON file containing scan settings.

It is planned to support multiple scanning modes. At this moment (2022-09-05)
only approach curves and backstep scans are supported. A factory class which takes
the file path as an argument enables import of .sicm files and returns an object
of either ApproachCurve or ScanBackstepMode.
"""
import copy
import os
import tarfile
import tempfile
import time
import traceback
from tarfile import TarFile
import json
import numpy as np
import struct

APPROACH = "approach"
BACKSTEP = "backstepScan"
FLOATING_BACKSTEP = "floatingBackstep"
SETTINGS = "settings.json"
MODE = ".mode"
INFO = ".info"
Xpx = "x-px"
Ypx = "y-px"
Xpx_raw = "x-px_raw"
Ypx_raw = "y-px-raw"
X_size = "x-Size"
Y_size = "y-Size"
X_size_raw = "x-Size-raw"
Y_size_raw = "y-Size-raw"
Manipulations = "manipulations"


class SICMdata:
    """
    This class works as an interface for SICM data recorded in different scan modes
    on our home-build scanning ion conductance microscope (SICM).

    The setup as well as the control software, which has been developed by Dr. Patrick
    Happel, support different scan modes.
    When the functionality of pySCIM_analyzer is to be extended, implemented new scan modes
    as a subclass inheriting from SICMdata.

    set_data() and get_data() should be overridden in the subclass to set the correct data fields.
    Data fields in all three dimensions are represented as numpy arrays.
    """
    def __init__(self):
        # data containing fields
        self.x: np.ndarray = np.zeros((1, 1))
        self.y: np.ndarray = np.zeros((1, 1))
        self.z: np.ndarray = np.zeros((1, 1))
        # metadata fields
        self.x_size: int = 0
        self.y_size: int = 0
        self.z_size: int = 0
        self.x_px: int = 0
        self.y_px: int = 0
        self.z_px: int = 0
        self.x_px_raw: int = 0
        self.y_px_raw: int = 0
        self.x_size_raw: int = 0
        self.y_size_raw: int = 0
        self.scan_mode: str = ""
        self.info: dict = {}
        self.settings: dict = {}
        self.previous_manipulations: list[str] = []

        # result fields
        self.fit_results = None
        self.roughness = None

    def set_settings(self, settings: dict):
        """Sets metadata obtained from settings.json
        and .mode."""
        self.settings = settings

    def get_data(self):
        """Returns a tuple containing x and z data for ApproachCurves and
         x, y and z for Scan data.

         Indices are:
         [0]: x
         [1]: z (ApproachCurves) or y (Scan)
         [2]: z (Scan only)
         """
        return self.x, self.y, self.z

    def get_scan_time(self) -> str:
        """Returns the scan time as a string.
        The format is hours:minutes:seconds."""
        try:
            time_in_s = round(self.info.get("client_duration") / 1000)
        except TypeError:
            time_in_s = 0
        return time.strftime("%H:%M:%S", time.gmtime(time_in_s))

    def get_scan_date(self) -> str:
        """
        Returns the date of the scan as a string.

        For some reason, no time information are stored in .info
        files of approach curve recordings.
        """
        try:
            date = self.info.get("client_start_time")
            date = date[:date.index(".")]
        except AttributeError:
            date = "n/a"
        return date


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
    """A class for 3-dimensional SICM scans."""

    def __init__(self):
        super(ScanBackstepMode, self).__init__()

    def set_settings(self, settings: dict):
        super().set_settings(settings)
        self.x_px = int(settings[Xpx])
        self.y_px = int(settings[Ypx])
        self.previous_manipulations = settings.get(Manipulations, [])
        try:
            self.x_px_raw = self.get_valid_int_from_field(value=settings.get(Xpx_raw, ""), default_value=self.x_px)
            self.y_px_raw = self.get_valid_int_from_field(value=settings.get(Ypx_raw, ""), default_value=self.y_px)

            self.x_size = self.get_valid_int_from_field(value=settings.get(X_size, ""), default_value=self.x_px)
            self.y_size = self.get_valid_int_from_field(value=settings.get(Y_size, ""), default_value=self.y_px)
            self.x_size_raw = self.get_valid_int_from_field(value=settings.get(X_size_raw, ""), default_value=self.x_size)
            self.y_size_raw = self.get_valid_int_from_field(value=settings.get(Y_size_raw, ""), default_value=self.y_size)

        except ValueError as e:
            # There might be cases in which the control software
            # set empty values for x_size or y_size

            #print(e)
            #print(traceback.format_exc(()))
            print("bla")

    def get_valid_int_from_field(self, value: str, default_value: int = 0) -> int:
        """This function returns an integer converted from a string value.
        In case the string can not be converted to int, a default value is returned."""
        try:
            valid_int = int(value)
        except ValueError:
            valid_int = int(default_value)
        return valid_int


    def set_data(self, data: list[int]):
        """Rearranges scan data for 3-dimensional plotting."""
        self.z = np.reshape(data, (self.y_px, self.x_px)) / 1000  # to have z data in µm instead of nm
        self.reshape_xy_meshgrids()

    def reshape_xy_meshgrids(self):
        self.x, self.y = np.meshgrid(range(self.x_px), range(self.y_px))

    def get_data(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return x, y, and z data."""
        return self.x, self.y, self.z

    def get_pixel_dimensions(self) -> (int, int):
        """Returns the number of x and y pixel for the scan."""
        return self.x_px, self.y_px

    def set_pixel_dimensions(self, x: int, y: int):
        """
        Sets numbers of pixels.

        This function should be called when the size of the scan has been changed,
        e.g., after a crop.
        The original values in the settings dict of SICMdata remain unchanged.

        :param int x: number of pixels in x
        :param int y: number of pixels in y
        """
        self.x_px = x
        self.y_px = y

    def update_dimensions(self):
        """Updates the number of pixel and the micrometer size in x and y dimensions.


        This function should be called when the scan size has changed, e.g.,
        after crop.
        """
        self._update_pixel_dimensions()
        self._update_sizes()

    def _update_pixel_dimensions(self):
        """Updates the number of pixels in x and y dimensions
        and reshapes mesh grids."""
        self.y_px, self.x_px = self.z.shape
        self.reshape_xy_meshgrids()

    def _update_sizes(self):
        """Updates the size of the scan in micrometer."""
        self.x_size = self.x_px * self.micron_to_pixel_factor_x()
        self.y_size = self.y_px * self.micron_to_pixel_factor_y()

    def micron_to_pixel_factor_x(self) -> float:
        try:
            return self.x_size_raw / self.x_px_raw
        except ZeroDivisionError:
            return 1

    def micron_to_pixel_factor_y(self) -> float:
        try:
            return self.y_size_raw / self.y_px_raw
        except ZeroDivisionError:
            return 1

def get_sicm_data(file_path: str) -> SICMdata:
    """Read all data from the tar.gz-like .sicm-file format and stores it in
    an instance of SICMdata.

    Depending on the scan mode of the file one of the following
    subclasses will be instantiated:
        - ApproachCurve
        - ScanBackstepMode (for backstepScan and floatingBackstep)
    """
    try:
        tar = tarfile.open(file_path, "r:gz")
        scan_mode = get_sicm_mode(tar)
        info = get_sicm_info(tar)
        settings = get_sicm_settings(tar)
        data = read_byte_data(tar)

        if scan_mode == BACKSTEP or scan_mode == FLOATING_BACKSTEP:
            sicm_data = ScanBackstepMode()
        elif scan_mode == APPROACH:
            sicm_data = ApproachCurve()
        else:
            sicm_data = SICMdata()
            sicm_data.scan_mode = "unknown scan mode"

        sicm_data.scan_mode = scan_mode
        sicm_data.set_settings(settings)
        sicm_data.info = info
        sicm_data.set_data(data)
    except Exception as e:
        print(e)
        print("file: " + file_path)
        sicm_data = SICMdata()
        sicm_data.scan_mode = "invalid file"

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


def get_data_as_bytes(data: SICMdata) -> list[bytes]:
    """Packs and returns data as list of bytes.
    All values will be converted from micrometer to nanometer.
    Values are packed as unsigned 2-byte integers.

    If negative values exist all z_data will be adjusted by the
    largest negative number.
    """
    z_data = data.z.flatten("C") * 1000
    z_data = z_data - np.min(z_data)
    byte_data = []
    for pixel in z_data:
        byte_data.append(struct.pack("<H", int(pixel)))
    return byte_data


def export_sicm_file(file_path: str, sicm_data: SICMdata, manipulations: list[str]):
    """
    Export an instance of SICMdata as a .sicm file.

    This file will be readable by the MATLAB SICMapp written
    by Patrick Happel and by pySICM_analyzer.

    Dev note: At the moment only export of BackstepScans is implemented as
    static functions. In the future these functions should be made class methods
    of the different scan mode subclasses.
    """
    # create a tempory directory to which files will be written before
    # storing in tar.gz-like .sicm file
    directory = tempfile.TemporaryDirectory()
    path_temp_dir = directory.name
    file_names = []
    try:
        # write files to temp directory
        file_name = _write_byte_data_file(path_temp_dir, sicm_data)
        file_names.append(file_name)
        file_name = _write_data_info_file(path_temp_dir, sicm_data)
        file_names.append(file_name)
        file_name = _write_mode_file(path_temp_dir, sicm_data)
        file_names.append(file_name)
        file_name = _write_settings_file(path_temp_dir, sicm_data)
        file_names.append(file_name)
    except FileNotFoundError as e:
        print("Error during file export as .sicm.")
    create_targz_from_list_of_files(file_path, file_names)


def _write_byte_data_file(path: str, sicm_data: SICMdata) -> str:
    """
    Creates a file in the given directory path containing the byte data
    of the SICMdata instance.

    :param str path: path to a directory
    :return: full path to the file as a string.
    """
    byte_data = get_data_as_bytes(sicm_data)

    with open(os.path.join(path, "data"), "wb") as f:
        for byte in byte_data:
            f.write(byte)
        f.close()
    return f.name


def _write_data_info_file(path: str, sicm_data: SICMdata) -> str:
    """
    Creates a file in the given directory path containing the scan info
    of the SICMdata instance.

    :param str path: path to a directory
    :return: full path to the file as a string.
    """
    with open(os.path.join(path, "data.info"), "w") as f:
        json.dump(sicm_data.info, f)
        f.close()
    return f.name


def _write_mode_file(path: str, sicm_data: SICMdata) -> str:
    """
    Creates a file in the given directory path containing the scan mode
    of the SICMdata instance.

    :param str path: path to a directory
    :return: full path to the file as a string.
    """
    with open(os.path.join(path, ".mode"), "w") as f:
        f.write(sicm_data.scan_mode)
        f.close()
    return f.name


def _write_settings_file(path: str, sicm_data: SICMdata, manipulations: list[str]) -> str:
    """
    Creates a file in the given directory path containing the scan settings
    and metadata of the SICMdata instance.

    :param str path: path to a directory
    :param list[str] manipulations: a list of strings describing manipulations of the data
    :return: full path to the file as a string.
    """
    settings_copy = copy.deepcopy(sicm_data.settings)
    _add_matedata_fields(settings_copy, sicm_data)

    sjson = json.dumps(settings_copy, separators=(',', ':'))
    with open(os.path.join(path, "settings.json"), "w") as f:
        f.write(sjson)
        f.close()
    return f.name


def _add_matedata_fields(settings_copy: dict, sicm_data: SICMdata, manipulations: list[str]):
    """
    Adds metadata fields to a copy of the settings dictionary. If the field exists
    it is updated
    """
    settings_copy[Xpx] = str(sicm_data.x_px)
    settings_copy[Ypx] = str(sicm_data.y_px)
    settings_copy[Xpx_raw] = str(sicm_data.x_px_raw)
    settings_copy[Ypx_raw] = str(sicm_data.y_px_raw)
    settings_copy[X_size] = str(sicm_data.x_size)
    settings_copy[Y_size] = str(sicm_data.y_size)
    settings_copy[X_size_raw] = str(sicm_data.x_size_raw)
    settings_copy[Y_size_raw] = str(sicm_data.y_size_raw)
    settings_copy[Manipulations] = manipulations


def create_targz_from_list_of_files(export_filename: str, files: list[str]):
    """Writes a tar.gz-like .sicm file.
     Extension check for the file name should have been handled before calling this method.

    :param str export_filename: a string containing the full path including filename for the tar.gz-like .sicm file.
    :param list[str] files: list of filesto be included in the .sicm file
    """
    with tarfile.open(export_filename, "w:gz") as tar:
        for file in files:
            path = os.path.dirname(file)
            name = os.path.basename(file)
            tar.add(os.path.join(path, name), arcname=name)


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
