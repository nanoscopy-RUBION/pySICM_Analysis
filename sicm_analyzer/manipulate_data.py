import numpy as np
from PyQt6.QtCore import QPoint
from scipy.interpolate import griddata
from skimage.draw import disk

from sicm_analyzer.sicm_data import SICMdata, ScanBackstepMode


# Simple Manipulations
# ______________________________________
def crop(data: ScanBackstepMode, point1: QPoint, point2: QPoint):
    """Reduces the dimensions of the data to the area of a rectangle
    formed by the two points 1 and 2.

    Dev note: If the gui framework is changed and PyQt (Qt) is no longer used
    the data type of point1 and 2 must be changed.
    """
    width = abs(point1.x() - point2.x())
    height = abs(point1.y() - point2.y())

    if point1.x() < point2.x():
        orig_x = point1.x()
    else:
        orig_x = point2.x()
    if point1.y() < point2.y():
        orig_y = point1.y()
    else:
        orig_y = point2.y()

    # note: the shape in 2D arrays is defined as Y * X
    data.z = data.z[orig_y:orig_y + height, orig_x:orig_x + width]
    data.update_dimensions()


def subtract_z_minimum(data: SICMdata):
    """Subtracts the z minimum of a data
    from all z data points."""
    data.z = data.z - np.min(data.z)


def transpose_z_data(data: ScanBackstepMode):
    """Transposes the z array."""
    data.z = data.z.transpose()
    data.update_dimensions()


def invert_z_data(data: ScanBackstepMode):
    """Reflects all z values by x, y plane."""
    data.z = data.z * (-1)


def height_diff_to_neighbour(data: ScanBackstepMode):
    """
    Calculates the difference between each value and its right neighbour.
    Last point in a row is set to 0.
    """
    z = data.z
    for i in range(z.shape[0]):
        for j in range(z.shape[1] - 1):
            z[i, j] = z[i, j] - z[i, j+1]
        z[i, z.shape[1]-1] = 0


# Filter Manipulations
# ______________________________________
def filter_median_temporal(data: ScanBackstepMode, px_neighbours=1):
    """
    Sets each pixel equal to the median of itself, the l pixel measurements immediately before, and the l pixel 
    measurements immediately afterwards (2l+1 pixels in total).

    Pixels with less than l pixels before or after them
    will use the available pixels and will not attempt to find addition pixels after the 0th or n-1th index in an array
    of length n.

    Note: This function is only valid if data was scanned line-wise and each line beginning on the same end.
    This feature may be extended to support different scan modes.

    :param data: This is the Z data that is to be smoothed. It can either be as a single array or in an ndarray.
    :param px_neighbours: This is the number of measurements on either side (taken either immediately before or after) used to
    adjust each pixel. 
    :returns: new Z data adjusted using the described method. The existing object is not modified.
    """
    shape = data.z.shape
    flattened = data.z.flatten('C')
    z = np.zeros(len(flattened))

    for i in np.arange(0, len(flattened)):
        z[i] = np.median(flattened[np.max([i - px_neighbours, 0]):np.min([i + (px_neighbours + 1), len(flattened)])])
    data.z = z.reshape(shape, order='C')


def filter_average_temporal(data: ScanBackstepMode, px_neighbours=1):
    """
    Sets each pixel equal to the average of itself, the l pixel measurements immediately before, and the l pixel 
    measurements immediately afterwards (2l+1 pixels in total).

    Pixels with less than l pixels before or after them
    will use the available pixels and will not attempt to find addition pixels after the 0th or n-1th index in an array
    of length n.

    Note: This function is only valid if data was scanned line-wise and each line beginning on the same end.
    This feature may be extended to support different scan modes.

    :param data: This is the Z data that is to be smoothed. It can either be as a single array or in an ndarray.
    :param px_neighbours: This is the number of measurements on either side (taken either immediately before or after) used to
    adjust each pixel.
    :returns: new Z data adjusted using the described method. The existing object is not modified.
    """
    shape = data.z.shape
    flattened = data.z.flatten('C')
    z = np.zeros(len(flattened))

    for i in np.arange(0, len(flattened)):
        z[i] = np.mean(flattened[np.max([i - px_neighbours, 0]):np.min([i + (px_neighbours + 1), len(flattened)])])
    data.z = z.reshape(shape, order='C')


def filter_median_spatial(data: ScanBackstepMode, px_radius=1):
    """
    Sets each pixel equal to the median of all points included in a disc-shaped field centered on the point itself with
    a given px_radius.
    If the pixel radius equals 1, the data will not be changed.

    :param data: This is the Z data that is to be smoothed. It can either be as a single array or in an ndarray.
    :param px_radius: This is the number of measurements on either side (taken either immediately before or after) used to
    adjust each pixel.
    :returns: new Z data adjusted using the described method. The existing object is not modified.
    """
    shape = data.z.shape
    z = np.zeros(shape)

    for i in np.arange(shape[0]):
        for j in np.arange(shape[1]):
            z[i, j] = np.median(data.z[disk((i, j), px_radius, shape=shape)])
    data.z = z


def filter_average_spatial(data: ScanBackstepMode, px_radius=1):
    """
    Sets each pixel equal to the average of all points included in a disc-shaped field centered on the point itself with
    a given px_radius.
    If the pixel radius equals 1, the data will not be changed.

    :param data: This is the Z data that is to be smoothed. It can either be as a single array or in an ndarray.
    :param px_radius: This is the number of measurements on either side (taken either immediately before or after) used to
    adjust each pixel.
    :returns: new Z data adjusted using the described method. The existing object is not modified.
    """
    shape = data.z.shape
    z = np.zeros(shape)

    for i in np.arange(shape[0]):
        for j in np.arange(shape[1]):
            z[i, j] = np.mean(data.z[disk((i, j), px_radius, shape=shape)])
    data.z = z


def fitting_objective(real, pred):
    retVal = 0
    for i in real.shape[0]:
        retVal += np.abs(real[i] - pred[i])
    print("Retval is " + str(retVal))
    return retVal


def level_data(data: ScanBackstepMode, method='plane'):
    """
    This method is intended to correct for a variety of possible shapes that . 

    :param data: View object which contains the data
    :param method: TODO
    :returns: An adjusted NDArray of z-data which corresponds to the original data with the specified geometry subtracted.
    This NDArray will be the 
    """
    # TODO reorganize the code... this function is too large
    # reshape data to vector
    real_z = data.z.flatten('F')
    real_x = data.x.flatten('F')
    real_y = data.y.flatten('F')

    if method == 'plane' or method == 'linewise' or method == 'linewise_mean' or method == 'linewise_y':
        eq = np.array([np.ones(real_z.shape[0]), real_x, real_y]).transpose()
    elif method == '2Dpoly':
        eq = np.array([np.ones(real_z.shape[0]), real_x, real_y, real_x ** 2, + (real_x ** 2) * real_y,
                       + (real_x ** 2) * (real_y ** 2), (real_y ** 2) * real_x, (real_y ** 2),
                       real_x * real_y]).transpose()
    elif method == 'paraboloid':
        eq = np.array([np.ones(real_z.shape[0]), np.reciprocal(real_x) ** 2, np.reciprocal(real_y) ** 2]).transpose()
    coeff, r, rank, s = np.linalg.lstsq(eq, real_z, rcond=1)

    xy_coord = np.array([data.x.flatten('F'), data.y.flatten('F')]).transpose()

    # The coefficients calculated above are then used to create a . This will be
    if method == 'plane' or method == 'linewise' or method == 'linewise_mean' or method == 'linewise_y':
        pred_z = [coeff[0] + coeff[1] * i[0] + coeff[2] * i[1] for i in xy_coord]
    if method == '2Dpoly':
        pred_z = [
            coeff[0] + coeff[1] * i[0] + coeff[2] * i[1] + coeff[3] * (i[0] ** 2) + coeff[4] * (i[0] ** 2) * i[1] +
            coeff[5] * (i[0] ** 2) * (i[1] ** 2) + coeff[6] * (i[1] ** 2) + coeff[7] * i[0] * (i[1] ** 2) + coeff[8] *
            i[0] * i[1] for i in xy_coord]
    if method == 'paraboloid':
        # pred_z = [coeff[0] + ((coeff[1]**2))/(i[0]**2) + ((coeff[2]**2))/(i[1]**2) for i in xy_coord]
        pred_z = [coeff[0] + (1 / (coeff[1] ** 2)) * (i[0] ** 2) + (1 / (coeff[2] ** 2)) * (i[1] ** 2) for i in
                  xy_coord]

    adj_z = real_z - pred_z

    #print("max: %s  min: %s" % (np.max(adj_z), np.min(adj_z)))
    # this mask is used to exclude all data points which are larger than the 25th percentile
    mask = np.where(adj_z > np.percentile(adj_z, 25))

    # fit without outliers
    coeff, r, rank, s = np.linalg.lstsq(eq[mask[0]], adj_z[mask[0]], rcond=1)

    if method == 'plane' or method == 'linewise' or method == 'linewise_mean' or method == 'linewise_y':
        pred_z = [coeff[0] + coeff[1] * i[0] + coeff[2] * i[1] for i in xy_coord]
    adj_z = adj_z - pred_z
    adj_z = adj_z.reshape(data.z.shape, order='F')#.transpose()
    '''if method == 'linewise':
        #xz_coord = np.array([view_ob.get_x_data(), adj_z])#.transpose()
        #adj_z = np.empty()
        for i in adj_z.shape[0]:
            temp = np.polyfit(real_x[i],adj_z[i],1)
            adj_z.append()
        #adj_z = [np.for i in xz_coord]
        #coeff, r, rank, s = np.linalg.lstsq(eq, real_z,rcond=1)
        #np.polyfit()'''
    if method == 'linewise_mean':
        adj_z = [i - np.mean(i) for i in pred_z]
    if method == 'linewise_y':
        pass
    #print("max: %s  min: %s" % (np.max(adj_z), np.min(adj_z)))

    data.z = adj_z


def interpolate_cubic(data: SICMdata, num_points, method='nearest'):
    """
    Interpolate Cubic
    Sets x-axis limits for the visual display of the data. This does not crop the data and the rest can still be viewed by panning.
    Will check to ensure the values are floats but does not check that the lower bound is first.

    :param data:
    :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
    :returns: 1 upon successful setting and 0 upon failure
    """
    x = data.x  # .flatten()
    y = data.y  # .flatten()
    z = data.z.flatten()
    # grid_x, grid_y = np.mgrid[0:len(x):1/num_points, 0:len(y):1/num_points]
    grid_x_new, grid_y_new = np.mgrid[0:x.shape[0]:1 / num_points, 0:x.shape[1]:1 / (num_points + 1)]
    # rng = np.random.default_rng()
    # points = np.array((x,y)).T#np.insert(x, np.arange(len(y)), y)
    grid_x_old, grid_y_old = np.mgrid[0:x.shape[0], 0:x.shape[1]]
    grid_x_old = grid_x_old.flatten()
    grid_y_old = grid_y_old.flatten()
    # print(grid_x_new.shape)
    # print(z.shape)
    # print(grid_x_old.shape)
    inter = griddata((grid_x_old, grid_y_old), z, (grid_x_new, grid_y_new), method=method)  # (grid_x,grid_y)
    return [inter, grid_x_new, grid_y_new]


'''def interpolate_neighbor(view_ob):
    """
    Interpolate Neighbor
    Sets x-axis limits for the visual display of the data. This does not crop the data and the rest can still be viewed by panning.
    Will check to ensure the values are floats but does not check that the lower bound is first.

    :param lims: List containing two floats which define the lower and upper bound of the y-axis, respectively
    :returns: 1 upon successful setting and 0 upon failure
    """
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
    points = np.concatenate((view_ob.get_x_data().flatten(),view_ob.get_y_data().flatten()),axis=1)
    inter = griddata(points, view_ob.get_z_data().flatten(), (grid_x, grid_y), method='nearest')
    return inter'''
