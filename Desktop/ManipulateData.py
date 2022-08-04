import numpy as np
from scipy.interpolate import griddata

def subtract_minimum(data):
    return data-np.min(data)

#def z_to_temporal(data):

#def temporal_to_z(data,shape):
#Helper function to 

def filter_median_temporal(data,l=1):
    shape = data.shape
    flattened = data.flatten()
    z = np.zeros(len(flattened))
    #print(z.shape)
    #y = np.zeros(data.size()[0]-2*l,)
    for i in np.arange(0,len(flattened)):
        z[i] = np.median(flattened[np.max([i-l,0]):np.min([i+(l+1),len(flattened)])]) #May need to be i+2. Test this!
    #for i in l
    return z.reshape(shape)
def filter_average_temporal(data,l=1):
    shape = data.shape
    flattened = data.flatten()
    z = np.zeros(len(flattened))
    #print(z.shape)
    #y = np.zeros(data.size()[0]-2*l,)
    for i in np.arange(0,len(flattened)):
        z[i] = np.mean(flattened[np.max([i-l,0]):np.min([i+(l+1),len(flattened)])]) #May need to be i+2. Test this!
    #for i in l
    return z.reshape(shape)
def filter_median_spatial():
    return 1
def filter_average_spatial():
    return 1
def apply_default_scale():
    return 1
#def crop(data,gui_ob):

#    return data[,]

#def transpose_z():

def level_plane():
    return

def interpolate_cubic(view_ob):
    x = view_ob.get_x_data().flatten()
    y = view_ob.get_y_data().flatten()
    z = view_ob.get_z_data().flatten()
    grid_x, grid_y = np.mgrid[0:1:len(x), 0:1:len(y)]
    rng = np.random.default_rng()
    points = np.array((x,y)).T#np.insert(x, np.arange(len(y)), y)
    print(points.shape)
    inter = griddata(points, z, (grid_x, grid_y), method='cubic')
    return inter
def interpolate_neighbor(view_ob):
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
    points = np.concatenate((view_ob.get_x_data().flatten(),view_ob.get_y_data().flatten()),axis=1)
    inter = griddata(points, view_ob.get_z_data().flatten(), (grid_x, grid_y), method='nearest')
    return inter
