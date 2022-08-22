def get_grid(view):
    xlims = view.get_xlims()
    xpixels = xlims[1]-xlims[0]+1
    ylims = view.get_ylims()
    ypixels = ylims[1]-ylims[0]+1
    origin =
    #Original counts from bottom left
    xsize = 
    ysize = 

    retGrid = 
    return retGrid
def get_points(window,n=2):
    point1 = [window.get_old_x(),window.get_old_y()]
    point2 = [window.get_current_x(),window.get_current_y()]
    return [point1,point2]
def measure_distance():

def measure_profile():
