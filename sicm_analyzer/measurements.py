import math
from typing import Any

import numpy as np
from symfit.core.minimizers import BFGS
from symfit import Poly, variables, parameters, Model, Fit
from symfit.core.objectives import LeastSquares
from sicm_analyzer.sicm_data import SICMdata


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


def polynomial_fifth_degree(x_data, y_data, z_data: np.array):
    """Returns data fitted to a polynomial of 5th degree with two
    variables x and y."""
    x, y, z = variables('x, y, z')
    p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05 = parameters(
        "p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05"
    )
    p00.value = 10
    p10.value = 0.01
    p20.value = 0.01
    p30.value = 0.01
    p40.value = 0.01
    p50.value = 0.01
    p01.value = 0.01
    p02.value = 0.01
    p03.value = 0.01
    p04.value = 0.01
    p05.value = 0.01
    p11.value = 0.01
    p21.value = 0.01
    p31.value = 0.01
    p41.value = 0.01
    p12.value = 0.01
    p13.value = 0.01
    p14.value = 0.01
    p22.value = 0.01
    p32.value = 0.01
    p23.value = 0.01

    model_dict = {
        z: Poly(
            {
                (0, 0): p00,
                (1, 0): p10,
                (0, 1): p01,
                (2, 0): p20,
                (1, 1): p11,
                (0, 2): p02,
                (3, 0): p30,
                (2, 1): p21,
                (1, 2): p12,
                (0, 3): p03,
                (4, 0): p40,
                (3, 1): p31,
                (2, 2): p22,
                (1, 3): p13,
                (0, 4): p04,
                (5, 0): p50,
                (4, 1): p41,
                (3, 2): p32,
                (2, 3): p23,
                (1, 4): p14,
                (0, 5): p05,
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
    return z_fitted, fit_result



def _print_fit_results_to_console(fit_result):
    """A helper function for debugging."""
    print("###############################################")
    print("Fit results:")
    print(fit_result)
    print("###############################################")


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
