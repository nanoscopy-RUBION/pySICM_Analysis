import math
from typing import Any

import numpy as np
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
    #_print_fit_results_to_console(fit_result)
    z_fitted = model(x=x_data, y=y_data, **fit_result.params).z
    return z_fitted




def get_grid(view):
    xlims = view.get_xlims()
    xpixels = xlims[1]-xlims[0]+1
    ylims = view.get_ylims()
    ypixels = ylims[1]-ylims[0]+1
    #origin =
    #Original counts from bottom left
    #xsize =
    #ysize =

    #retGrid =
    #return retGrid


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
    rmse = math.sqrt(np.mean(diff**2))
    return rmse


def get_roughness(data: SICMdata) -> tuple[float, Any]:
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
    #fitted_data, fit_results = polynomial_fifth_degree(data.x, data.y, data.z)
    #corrected_data = data.z - fitted_data

    #roughness = root_mean_square_error(corrected_data)
    roughness = root_mean_square_error(data.z)
    return roughness#, fit_results


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

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        summation = np.sum(curve)
        n = len(curve)
        rtn[counter] = summation / n
        counter += 1
    return rtn


def get_root_mean_sq_roughness(data: SICMdata):
    """ 2.2 root-mean-square roughness (R_q)

    n: number of samples along the assessment length"""

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        sum_sqrs = np.sum(np.square(curve))
        n = len(curve)
        mean = sum_sqrs / n
        rtn[counter] = np.sqrt(mean)
        counter += 1
    return rtn


def get_ten_point_height_ISO(data: SICMdata):
    """ 2.3 ten point height (R_z(ISO))

    n: number of samples along the assessment length
    P_i: 5 highest peaks along assessment length
    V_i: 5 lowest valleys along assessment length

    """

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        try:
            if len(curve) < 10:
                raise ValueError
        except ValueError:
            print("Unable to compute parameter: the length of each approach curve must be at least 10.")
        n = len(curve)
        height_sorted = np.sort(curve)
        peaks = height_sorted[-5:]
        valleys = height_sorted[:5]
        diff = sum(peaks) - sum(valleys)
        rtn[counter] = diff / n
        counter += 1
    return rtn


def get_ten_point_height_DIN(data: SICMdata):
    """ 2.3 ten point height (R_z(DIN))

    n: number of samples along the assessment length
    P_i: 5 highest peaks along assessment length
    V_i: 5 lowest valleys along assessment length

    """

    rtn = np.zeros(len(data.z))
    counter = 0
    for curve in data.z:
        try:
            if len(curve) < 10:
                raise ValueError
        except ValueError:
            print("Unable to compute parameter: the length of each approach curve must be at least 10.")
        n = len(curve)
        height_sorted = np.sort(curve)
        peaks = height_sorted[-5:]
        valleys = height_sorted[:5]
        total = sum(peaks) + sum(valleys)
        rtn[counter] = total / (2 * n)
        counter += 1
    return rtn


def get_max_peak_height_from_mean(data: SICMdata):
    """ 2.4 maximum height of the profile above the mean line (R_p) """

    rtn = np.zeros(len(data.z))
    means = get_arithmetic_average_height(data)
    counter = 0
    for curve in data.z:
        avg = means[counter]
        max_peak = np.max(curve)
        rtn[counter] = max_peak - avg
        counter += 1
    return rtn


def get_max_valley_depth_from_mean(data: SICMdata):
    """ 2.5 maximum depth of the profile below the mean line (R_v) """

    rtn = np.zeros(len(data.z))
    means = get_arithmetic_average_height(data)
    counter = 0
    for curve in data.z:
        avg = means[counter]
        min_valley = np.min(curve)
        rtn[counter] = avg - min_valley
        counter += 1
    return rtn



if __name__ == '__main__':

    path2 = "/Users/claire/GitHubRepos/pySICM_Analysis/tests/sample_sicm_files/Zelle2Membran PFA.sicm"
    test = get_sicm_data(path2)

    # np.savetxt("testSICMdata.csv", test.z, delimiter=",")  # TODO fix this
    print(len(test.z))
    print(get_max_peak_height_from_mean(test))
