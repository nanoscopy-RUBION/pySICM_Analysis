import math
from typing import Any


import numpy as np
import scipy.signal
from matplotlib import pyplot as plt
# from scipy.signal import argrelmax, argrelmin, argrelextrema, find_peaks
from scipy import signal
from symfit.core.minimizers import BFGS
from symfit import Poly, variables, parameters, Model, Fit
from symfit.core.objectives import LeastSquares
from sicm_analyzer.sicm_data import SICMdata, get_sicm_data
from scipy.spatial import Delaunay


# TODO generalization of polynomial fit functions
def polynomial_second_degree(x_data, y_data, z_data: np.array):
    """Returns data fitted to a polynomial of 2nd degree with two
    variables x and y."""
    x, y, z = variables('x, y, z')
    p00, p10, p01, p20, p11, p02 = parameters(
        "p00, p10, p01, p20, p11, p02"
    )

    model_dict = {
        z: Poly(
            {
                (0, 0): p00,
                (1, 0): p10,
                (0, 1): p01,
                (2, 0): p20,
                (1, 1): p11,
                (0, 2): p02,
            },
            x, y
        ).as_expr()
    }
    model = Model(model_dict)

    # perform fit
    fit = Fit(model, x=x_data, y=y_data, z=z_data, objective=LeastSquares, minimizer=[BFGS])
    fit_result = fit.execute()
    # _print_fit_results_to_console(fit_result)
    z_fitted = model(x=x_data, y=y_data, **fit_result.params).z
    return z_fitted


def get_grid(view):
    xlims = view.get_xlims()
    xpixels = xlims[1] - xlims[0] + 1
    ylims = view.get_ylims()
    ypixels = ylims[1] - ylims[0] + 1
    # origin =
    # Original counts from bottom left
    # xsize =
    # ysize =

    # retGrid =
    # return retGrid


def get_points(window, n=2):
    point1 = [window.get_old_x(), window.get_old_y()]
    point2 = [window.get_current_x(), window.get_current_y()]
    return [point1, point2]


def get_surface_area_of_roi(data: SICMdata, roi=None) -> float:
    """Returns the surface area of a selected region of interest.

    Dev Note: ROI is not supported at the moment. the surface
    area for the whole scan will be returned.
    """
    points = np.vstack((data.x, data.y, data.z)).reshape((3, -1)).T
    triangulation = Delaunay(points[:, :2]).simplices


def root_mean_square_error(data: np.array) -> float:
    """Returns the root mean square error of data.

    TODO FORMEL einfügen
    """
    mean = np.mean(data)
    diff = data - mean
    rmse = math.sqrt(np.mean(diff ** 2))
    return rmse


def get_roughness(data: SICMdata):  # -> tuple[float, Any]:
    """Returns the roughness of SICM data.
    No data manipulation is performed in this step!

    Documentation from the matlab version:
    Compute the roughness of the data
    Currently, the following method is used:
    1) Subtract a paraboloid from the data
    2) Remove outliers
    3) Compute the RMSE of the data

    Examples:

    r = roughness(data)

    Computes and returns the roughness

    [r, outliers_removed] = roughness(data)

    Computes the roughness and returns the data without outliers.
    Instead of the outlieres, NaN is inserted

    [r, outliers_removed, fo] = roughness(data)

    As above, but additionally returns the fitobject.

    [r, outliers_removed, fo, go] = roughness(data)

    As above, but additionally returns the goodness of the fit.

    SEE ALSO: SUBTRACTPARABOLOID, MEDIAN, BOXPLOT
    """
    '''
    pxsz = 1
    if nargin > 1:
        pxsz = varargin{1}

    # paraboiloid filter?
    [flat, fo, go] = subtractParaboloid(data, pxsz)

    # Remove outliers
    p75 = prctile(flat(:), 75)
    p25 = prctile(flat(:), 25)

    # Every data point beyond 1.5 IQRs is an outlier
    upperlimit = p75 + 1.5 * (p75 - p25)
    lowerlimit = p25 - 1.5 * (p75 - p25)

    no_outliers = flat(flat >= lowerlimit & flat <= upperlimit)

    # RMSE calculation
    r = root_mean_square_error(no_outliers(:))

    

    if nargout > 1:
        tmp = flat
        tmp(tmp < lowerlimit | tmp > upperlimit) = NaN
        varargout{1} = tmp

    if nargout > 2:
        varargout{2} = fo

    if nargout > 3:
        varargout{3} = go
    '''
    # fitted_data, fit_results = polynomial_fifth_degree(data.x, data.y, data.z)
    # corrected_data = data.z - fitted_data

    # roughness = root_mean_square_error(corrected_data)
    roughness = root_mean_square_error(data.z)
    return roughness  # , fit_results


def get_lower_and_upper_limit_for_outlier_determination(values: np.array):
    """Calculates the lower and upper limits for
    outlier determination. For this purpose, 25% and 75%
    percentiles are determined. These values are adjusted by
    1.5-times the interquartile range (IQR)"""
    # determine 25% and 75% quartiles
    pc75 = np.percentile(values.flatten('F'), 75)
    pc25 = np.percentile(values.flatten('F'), 25)

    # interquartile range
    iqr = pc75 - pc25

    # Every data point beyond 1.5 IQRs is an outlier
    upper_limit = pc75 + 1.5 * iqr
    lower_limit = pc25 - 1.5 * iqr

    print("upper: %s" % upper_limit)
    print("lower: %s" % lower_limit)
    print(z_fitted[np.where((z_fitted < lower_limit) | (z_fitted > upper_limit))])
    print(z_fitted[np.where((z_fitted >= lower_limit) & (z_fitted <= upper_limit))])
    print("mean after: %s" % np.mean(z_fitted[np.where((z_fitted < lower_limit) | (z_fitted > upper_limit))]))

    # no_outliers = flat(flat >= lowerlimit & flat <= upperlimit)

    print(root_mean_square_error(z_fitted[np.where((z_fitted >= lower_limit) & (z_fitted <= upper_limit))]))


def measure_distance():
    pass


def measure_profile():
    pass


# Amplitude parameters
def get_arithmetic_average_height(data: SICMdata):
    """ 2.1 arithmetic average height (R_a), AKA centre line average

    n: number of samples along assessment length
    """
    values = data.z.flatten()
    avg = np.average(values)
    return avg


def get_root_mean_sq_roughness(data: SICMdata):
    """ 2.2 root-mean-square roughness (R_q)

    n: number of samples along the assessment length"""

    values = data.z.flatten()
    mean = np.average(np.square(values))
    return np.sqrt(mean)


def get_ten_point_height_ISO(data: SICMdata):
    """ 2.3 ten point height (R_z(ISO))

    n: number of samples along the assessment length
    P_i: 5 highest peaks along assessment length
    V_i: 5 lowest valleys along assessment length

    """

    values = data.z.flatten()
    values_sorted = np.sort(values)
    peaks = values_sorted[-5:]
    valleys = values_sorted[:5]
    diff = sum(peaks) - sum(valleys)
    return diff / len(values)


def get_ten_point_height_DIN(data: SICMdata):
    """ 2.3 ten point height (R_z(DIN))

    n: number of samples along the assessment length
    P_i: 5 highest peaks along assessment length
    V_i: 5 lowest valleys along assessment length

    """

    values = data.z.flatten()
    values_sorted = np.sort(values)
    peaks = values_sorted[-5:]
    valleys = values_sorted[:5]
    total = sum(peaks) + sum(valleys)
    return total / len(values)


def get_max_peak_height_from_mean(data: SICMdata):
    """ 2.4 maximum height of the profile above the mean line (R_p) """
    values = data.z.flatten()
    avg = np.average(values)
    max_peak = np.max(values)
    return max_peak - avg


def get_max_valley_depth_from_mean(data: SICMdata):
    """ 2.5 maximum depth of the profile below the mean line (R_v) """

    values = data.z.flatten()
    avg = np.average(values)
    min_peak = np.min(values)
    return avg - min_peak


def get_mean_height_of_peaks(data: SICMdata):
    """ 2.6 mean of the maximum height of peaks (R_pm) """
    # relies on line-wise evaluation of profiles

    rtn = np.zeros(len(data.z))
    counter = 0

    for curve in data.z:
        peak = np.max(curve)
        rtn[counter] = peak
        counter += 1

    return np.average(rtn)


def get_mean_depth_of_valleys(data: SICMdata):
    """ 2.7 mean of the maximum depth of valleys obtained for each sampling length (R_vm)"""
    # relies on line-wise evaluation of profiles

    rtn = np.zeros(len(data.z))
    counter = 0

    for curve in data.z:
        valley = np.min(curve)
        rtn[counter] = valley
        counter += 1

    return np.average(rtn)


def get_max_height_of_profile(data: SICMdata):
    """ 2.8 vertical distance between the highest peak and lowest value"""
    return get_max_peak_height_from_mean(data) + get_max_valley_depth_from_mean(data)


def get_maximum_height_single_profile(data: SICMdata):
    """ 2.9 vertical distance between the highest peak and lowest valley for each sampling length
    returns an array of length data.z that contains the max height for each single profile"""

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        max_peak = np.max(curve)
        min_valley = np.min(curve)
        rtn[counter] = max_peak - min_valley
        counter += 1
    return rtn


def get_mean_maximum_peak_valley_heights(data: SICMdata):
    """ 2.10 mean of values in 2.9 array"""

    vals = get_maximum_height_single_profile(data)
    return np.average(vals)


def get_largest_peak_to_valley_height(data: SICMdata):
    """ 2.11 maximum of the array that 2.10 returns"""

    vals = get_maximum_height_single_profile()
    return np.max(vals)


def get_third_point_height(data: SICMdata):
    """" 2.12 calculated per sample length - returns the maximum of the calculated values """

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        ordered = curve.sort()
        third_peak = ordered[-3]
        third_valley = ordered[2]
        rtn[counter] = third_peak - third_valley
        counter += 1
    return np.max(rtn)


def get_mean_of_third_point_height(data: SICMdata):
    """ 2.13 mean of all third point parameters """

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        ordered = curve.sort()
        third_peak = ordered[-3]
        third_valley = ordered[2]
        rtn[counter] = third_peak - third_valley
        counter += 1
    return np.average(rtn)


def get_profile_solidarity_factor(data: SICMdata):
    """ 2.14 ratio between the maximum depth of valleys and maximum height of the profile (k) """
    k = get_max_valley_depth_from_mean(data) / get_max_height_of_profile(data)
    return k


def get_skewness(data: SICMdata):
    """ 2.15 third central moment of profile amplitude probability density function - assessment length (R_sk)"""

    values = data.z.flatten()

    summation = np.sum(np.power(values, 3))
    skew = summation / len(values) / get_root_mean_sq_roughness(data) ** 3

    return skew


def get_kurtosis_coefficient(data: SICMdata):
    """ 2.16 fourth central moment of profile amplitude probability density function """

    values = data.z.flatten()

    summation = np.sum(np.power(values, 4))
    kurtosis = summation / len(values) / get_root_mean_sq_roughness(data) ** 4

    return kurtosis


def get_amplitude_density_function(data: SICMdata):
    """ 2.17 amplitude density = probably density (ADF)"""
    return


def get_auto_correlation_function(data: SICMdata):
    """ 2.18 auto correlation function"""
    return


def get_correlation_length(data: SICMdata):
    """ 2.19  describes correlation characteristics of the ACF (beta)"""
    return


def get_power_spectral_density(data: SICMdata):
    """ 2.20 power spectral density (PSD)"""
    return


# Spacing parameters
def get_high_spot_count(data: SICMdata, threshold: float):
    """ 3.1 high spot count: no of high regions of profile above a line parallel to the mean (HSC)"""
    # TODO check if scipy.signal.find_peaks() would be more suitable for this
    values = data.z.flatten()
    high_spots = 0
    isHighSpot = False

    for z in values:
        if z > threshold:
            if isHighSpot:
                continue
            else:
                high_spots += 1
                isHighSpot = True
        else:
            isHighSpot = False

    return high_spots


def get_peak_count(data: SICMdata, margin):
    """ 3.2 Peak count (P_c) number of local peaks """
    values = data.z.flatten()
    reachedLow = False
    reachedHigh = False
    count = 0

    high = np.average(values) + margin
    low = np.average(values) - margin

    for z in values:
        if z < low and (not reachedLow):
            reachedLow = True
        if z > high and reachedLow:
            reachedHigh = True
        if z < low and reachedHigh:
            count += 1
            reachedLow = False
            reachedHigh = False

    return count


def get_mean_spacing_of_adjacent_local_peaks(data: SICMdata):
    values = data.z.flatten()

    threshold = get_max_height_of_profile(data) * 0.1
    # TODO check if this threshold is right
    indices = scipy.signal.find_peaks(values)[0]
    # a = indices["peak_heights"]
    print("indicies: ")
    print(indices)

    rtn = []

    for i in range(len(indices)):
        index = indices[i]
        maxima = values[index]
        rtn.append(maxima)

    print(rtn)

    # Create a plot
    plt.plot(values)  # 'o' for regular points
    plt.scatter(indices, rtn, marker='X', color='red',
                label='Marked')
    plt.grid(True)
    plt.show()

    return np.average(rtn)


if __name__ == '__main__':
    path2 = "/Users/claire/GitHubRepos/pySICM_Analysis/tests/sample_sicm_files/Zelle2Membran PFA.sicm"
    test = get_sicm_data(path2)

    print(test.z)

    print(len(test.z))
    print("")
    print("2.1 arithmetic average: ")
    print(get_arithmetic_average_height(test))
    print("2.2 root-mean-square roughness: ")
    print(get_root_mean_sq_roughness(test))
    print("2.4 find max value: ")
    print(get_max_peak_height_from_mean(test))
    print("2.5 find min value: ")
    print(get_max_valley_depth_from_mean(test))
    print("2.15 skewness: ")
    print(get_skewness(test))
    print("3.1 high spot count: ")
    print(get_high_spot_count(test, 32.8))
    print("3.3 get mean spacing of local adjacent peaks")
    print(get_mean_spacing_of_adjacent_local_peaks(test))


