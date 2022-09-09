import math

import numpy as np
from symfit import Poly, variables, parameters, Model, Fit


def polynomial_fifth_degree(x_data, y_data, z_data: np.array):
    """Returns data fitted to a polynomial of 5th degree with two
    variables x and y."""
    x, y, z = variables('x, y, z')
    p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05 = parameters(
        "p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05"
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
    fit = Fit(model, x=x_data, y=y_data, z=z_data)
    fit_result = fit.execute()
    print(fit_result)
    z_fitted = model(x=x_data, y=y_data, **fit_result.params).z
    return z_fitted
    # Remove outliers
    pc75 = np.percentile(z_fitted.flatten('F'), 75)
    pc25 = np.percentile(z_fitted.flatten('F'), 25)
    print(pc75)
    print(pc25)


    # Every data point beyond 1.5 IQRs is an outlier
    iqr = pc75 - pc25  # interquartile range
    upper_limit = pc75 + 1.5 * iqr
    lower_limit = pc25 - 1.5 * iqr
    print("upper: %s" % upper_limit)
    print("lower: %s" % lower_limit)
    print("mean before: %s" % np.mean(z_fitted))
    print(len(z_fitted[np.where((z_fitted < lower_limit) | (z_fitted > upper_limit))]))
    print(len(z_fitted[np.where((z_fitted >= lower_limit) & (z_fitted <= upper_limit))]))
    print(z_fitted[np.where((z_fitted < lower_limit) | (z_fitted > upper_limit))])
    print(z_fitted[np.where((z_fitted >= lower_limit) & (z_fitted <= upper_limit))])
    print("mean after: %s" % np.mean(z_fitted[np.where((z_fitted < lower_limit) | (z_fitted > upper_limit))]))

    #no_outliers = flat(flat >= lowerlimit & flat <= upperlimit)

    print(root_mean_square_error(z_fitted[np.where((z_fitted >= lower_limit) & (z_fitted <= upper_limit))]))


    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.pcolormesh(z_data)
    ax2.pcolormesh(z_fitted)
    plt.show()


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

    FORMEL einfügen
    """

    mean = np.mean(data)
    diff = data - mean
    rmse = math.sqrt(np.mean(diff**2))
    return rmse

def get_roughness(data) -> float:
    """Compute roughness.


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

def measure_distance():
    pass


def measure_profile():
    pass
