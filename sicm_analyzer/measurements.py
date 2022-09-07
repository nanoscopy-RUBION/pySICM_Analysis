import math

import numpy as np


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
