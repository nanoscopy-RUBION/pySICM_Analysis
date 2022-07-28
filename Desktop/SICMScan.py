import numpy as np

def volume(self):
# Computes the volume of the data in the scan. Note: The data is taken as
# it is, nothing is subtracted first!
#
# Examples:
#    vol = obj.volume()
# 
#      Computes the volume of the data in `obj`
#      
#  If you want the volume without the z-offset, use:
#
#    obj.subtractMin()
#    vol = obj.volume()
    return self.stepx * self.stepy * sum(self.zdata_lin)


#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'prop'
#+GMD Name: 'Volume'
#+GMD Depends: {'x','y','z'}
#+GMD Changes: {}
#+GMD Immediate: 1
#+GMD Unit: '[x]×[y]×[z]'
#+END GUIMETADATA

def updateZDataFromFit(self, T, newObject=False):
# This function updates the z-data from the fitobjects in the
# approachcurves property.
#
    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.updateZDataFromFit(T)
        return o

    #TODO Figure out how to translate to Python
    self.zdata_grid = cellfun(...
        @(x)(x.inversefitfunc(...
            x.fitobject.I0,...
            x.fitobject.C,...
            x.fitobject.D,...
            x.fitobject.I0 * T)), ...
            self.approachcurves)
    return None

def update_from_ysize_(self):
# Internal function: Updates every data related to the y-coordinate
    self.stepy = self.ysize / self.ypx
    [xg, yg] = self.generate_xygrids_()
    self.ydata_grid = np.transpose(yg)
    self.ydata_lin = self.ydata_grid()

def update_from_xsize_(self):
# Internal function: Updates every data related to the x-coordinate.
    self.stepx = self.xsize / self.xpx
    [xg, yg] = self.generate_xygrids_()
    self.xdata_grid = np.transpose(xg)
    self.xdata_lin = self.xdata_grid

def upd_zlin_(self):
# Internal function: Shorthand to update zdata_lin from zdata_grid
    self.zdata_lin = self.zdata_grid.copy[:]

def transposeZ(self, newObject=False):
# Transposes the zdata_grid 
    if not newObject:
        self.zdata_grid = np.transpose(self.zdata_grid)
        self.zdata_lin = self.zdata_grid[:]
    else:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.transposeZ();    
        return o
    return None
    
#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: 'Transpose Z'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {'z'}
#+GMD Immediate: 0
#+GMD Menu: 'Simple Manipulations'
#+END GUIMETADATA

def transposeXY(self, newObject=False):
# Transposes the xdata_grid and ydata_grid    
    if newObject==False:
        self.xdata_grid = np.transpose(self.xdata_grid)
        self.ydata_grid = np.transpose(self.ydata_grid)
        self.xdata_lin = self.xdata_grid[:]
        self.ydata_lin = self.ydata_grid[:]
        tmp = self.xsize
        self.xsize = self.ysize
        self.ysize = tmp
        return None
    else:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.transposeXY()
        return o

def transposeAll(self):
# Transposes the xdata_grid and ydata_grid    
    if newObject==False:
        self.xdata_grid = np.tranpose(self.xdata_grid)
        self.ydata_grid = np.tranpose(self.ydata_grid)
        self.zdata_grid = np.transpose(self.zdata_grid)
        self.xdata_lin = self.xdata_grid[:]
        self.ydata_lin = self.ydata_grid[:]
        self.zdata_lin = self.zdata_grid[:]
        return None
    else:
        o = SICM.SICMScan.fromSICMScan_(self);
        o.transposeAll();        
        return o

function varargout = surface(self, varargin)
def surface(self,):
# Plots an (interpolated) 3D plot of the data. 
#
#    Example:
#      foo = SICMScan.FromExampleData;
#      surface(foo);
# 
#        Generates a plot of the example data in `foo`. 
#
#
#      surface(foo, 5);
# 
#        Generates a plot of the example data in `foo`, with 5
#        interpolation steps between the pixels.
#
#      You can pass optional arguments to the original surface-function,
#      however, in this case you have provide an interpolation:
#
#      surface(foo, 5, 'EdgeColor', [0 0 0]);
# 
#        Generates a plot of the example data in `foo`, with 5
#        interpolation steps between the pixels and a black EdgeColor.
#
#      surface(foo, 1, 'EdgeColor', [0 0 0]);
# 
#        Generates a plot of the example data in `foo` without
#        interpolation between the pixels and a black EdgeColor.

    interp = 1
    start = 0
    
    if nargin > 1:
        if isa(varargin{1},'matlab.graphics.axis.Axes'):
            ax = varargin{1}
            if nargin > 2
                interp = varargin{2}
                start = 3
            end
        else:
            ax = gca
            interp = varargin{1}
            start = 2
        end
    else:
        ax = gca
    [xg, yg] = self.generate_xygrids_(interp)
    zg = self.zdata_grid
    if interp > 1:
        zg = griddata(self.xdata_lin,self.ydata_lin, self.zdata_lin, xg, yg)    
    if start > 0:
        a = surface(ax, xg,yg,zg,'EdgeColor','None',varargin{start:end})
    else:
        a = surface(ax, xg,yg,zg,'EdgeColor','None')
    return a

def subtractMin(self, newObject=False):
    # Subtract the minimum in the data set from all data points.
    #
    # Examples:
    #    obj.subtractMin()
    #   
    #    Subtracts the minimum value from obj.zdata_lin and
    #    obj.zdata_grid 
    #
    #    newobj = obj.subtractMin()
    #
    #    As above, but returns a new object and does not alter
    #    `obj`
    #
    # See also MIN
    if newObject==False:
        self.subtract_(np.min(self.zdata_lin))
        return None
    else:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.subtractMin()
        return o

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: 'Subtract minimum'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {'z'}
#+GMD Immediate: 0
#+GMD Menu: 'Simple Manipulations'
#+END GUIMETADATA

def subtract_(self, value):
# Internal function: Subractvalue from all z-data
    self.zdata_grid = self.zdata_grid - value
    self.upd_zlin_()

def slope(self, scale=1): #Scale not currently used
# Computes the slope along the horizontal axes. 
#
#    Examples: 
#      
#      obj.slope()
#        
#        Computes the slope of the data in obj and returns it.
#     scale = 1;
#     if nargin > 1
#         scale = varargin{1};
#     end
#     sz = size(self.zdata_grid);
#     d = zeros(sz(1), sz(2) - 1);
#     for i = 1:sz(1)
#         d(i, :) = diff(self.zdata_grid(i,:));
#     end
    return np.diff(self.zdata_grid) #Computes derivative, find best python equivalent

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'img'
#+GMD Name: 'Slope'
#+GMD Depends: {'x','y','z'}
#+GMD Changes: {}
#+GMD Immediate: 1
#+END GUIMETADATA

classdef SICMScan <  SICM.importer & matlab.mixin.Copyable
class SICMScan(SICM.importer):
# This class provides tools to analyse, display and process SICM data.
#
# To generate an object `obj` of this class, use:
#
#    obj = SICMScan()
#
# However, this is rarely used. The static methods FROMFILE and
# FROMZDATAGRID return an object of this class that is populated with data.
# To test the class, FROMEXAMPLEDATA generates a SICMScan object with
# exemplary data.
#
# This class is inherited from the hiddenHandle class to simplify the
# programming since Matlab uses lazy copying otherwise.
# 
# See also FROMFILE, FROMZDATAGRID, FROMEXAMPLEDATA
    properties (SetObservable)
        zdata_grid = NaN; # z-data of the scan as a grid
        starttime = NaN; # Start time of the scan in arbitrary time units
        endtime = NaN; # End time of the scan in arbitrary time units
        duration = NaN; # Scan duration
        info = struct();
        ROIs = {}; # A collection of regions of interest.
        UnitX = '';
        UnitY = '';
        UnitZ = '';
        
    end
    properties (SetAccess = protected, GetAccess = public, SetObservable)
        IsDirty = false;
    end
    properties (SetAccess = protected, SetObservable)
        approachcurves = []; # A grid holding SICM.AppCurves for all data points, if available.
        xsize = NaN; # Size of the scan in x-direction in length unit
        ysize = NaN; # Size of the scan in y-direction in length unit
        xpx = NaN; # number of pixels in x-direction
        ypx = NaN; # number of pixels in y-direction
        stepx = NaN; # size of a pixel in x-direction
        stepy = NaN; # size of a pixel in y-direction
        xdata_lin = NaN; # x-data of all data point in a onedimensional vector
        ydata_lin = NaN; # y-data of all data point in a onedimensional vector
        zdata_lin = NaN; # z-data of all data point in a onedimensional vector
        xdata_grid = NaN; # x-data of all data points as a grid
        ydata_grid = NaN; # y-data of all data points as a grid

    end
    properties (Dependent)

    end
    properties (Hidden)
        # The importers property holds information about the different
        # importer functions known in the system. The property is a cell
        # containing different structs. The strucs should look like the
        # following:
        #   'name':
        #    A name assigned to the importer, not yet used, just for
        #    internal information. 
        #
        #   'exts': 
        #   The extensions processed by the importer, as required for the
        #   uigetfile method 
        #
        #   'expl': 
        #   A short information about the file type(s), as required for
        #   uigetfile 
        #
        #   'extlist':
        #   A cell array containing the extensions (including the
        #   preceeding .) that can be processed by the importer. More or
        #   less the same as 'exts', but in a format that is can be used
        #   with strcmp to simplify finding the correct importer.
        #
        #   'handle':
        #   A function handle pointing to a funtion that reads the data.
        #   The function should have one input argument, the filename, and
        #   return an SICMScan object
        #
        # See also UIGETFILE, STRCMP, FUNCTIONS
        importers = {
            struct(...
                'name'   , 'Binary data import, PH', ...
                'exts'   , '*.sicm;',...
                'expl'   , 'Binary data files (*.sicm)',...
                'extlist', {'.sicm'},...
                'handle' , @SICM.readBinarySICMData...
            ),...
            struct(...  
                'name'   , 'ASCII data import, PH', ...
                'exts'   , '*.sic; *.ras;',...
                'expl'   , 'ASCII data files (*.sic, *.ras)',...
                'extlist', {{'.sic', '.ras'}},...
                'handle' , @local_ReadAsciiData...
            )...
        }
    end
    
    methods (Static)
        
        o = FromZDataGrid(zdatagrid)
        o = FromFile(varargin)
        o = FromExampleData()

        # The following functions are intended for internal use

        o = fromSICMScan_(obj)
zx    
    methods (Access = public)

        function self = SICMScan(varargin)
            # Generate a SICMScan object
            #
            # This function generates an empty SICMScan object. In most
            # cases, you want to generate a SICMScan object from data or
            # from a file, see below.
            #
            # See also FROMZDATAGRID, FROMFILE
            #
            #
            mc = metaclass(self);

            for p = mc.PropertyList'
                if ~p.Hidden && ~strcmp(p.Name, 'IsDirty')
                    addlistener(self, p.Name, 'PostSet', @(~,~)self.dirtify());
                end
                
            end
        end
    
        # Functions that provide programming information
        
        info = getInterfaceInformation(self);
        
        # 
        # Functions for completing the data. 
        #
        setPx (self, xpx, ypx)
        varargout = setXSize (self, xsize)
        varargout = setYSize (self, ysize)
        
        

        #
        # Functions for data manipulation
        #
        
        varargout = addXOffset(self, xoffset)
        varargout = addYOffset(self, yoffset)
        
        varargout = subtractMin(self)
        varargout = scaleZ(self, factor, varargin)
        varargout = scaleZDefault(self)
        
        varargout = flatten(self, method, varargin)
        varargout = normalize(self)
        
        varargout = applyMask(self, mask)
        
        # Functions to read an manipulate the approach curves
        varargout = readAllAppCurves(self, fhandle)
        varargout = eachAppCurve(self, handle)
        
        varargout = inverse(self);
        varargout = filter(self, method, varargin);
        varargout = crop(varargin);
        varargout = profile(self, varargin); 
        h = distance(self);
        
        d = slope(self, varargin);
        r = rms(self);
        
        varargout = interpolate(self, steps, varargin);
        varargout = interpolate_wrapper(self, method, steps);
        varargout = transposeXY(self);
        varargout = transposeAll(self);
        varargout = transposeZ(self);
        varargout = changeXY(self);
        
        
        #
        # Methods, mostly for display
        #

        varargout = surface(self, varargin)
        varargout = plot(self, varargin)
        varargout = imagesc(self)
        varargout = reviewAllApproachCurves(self);
        reviewProblematicFits(self, varargin);
        app = getAppCurve(self, idx, varargin);
        t = fduration(self, varargin);
        
        #
        # Methods for data analysing 
        #
        m = min(self);
        m = max(self);
        v = volume(self);
        c = centroid(self, threshold);
        a = area(self);
        rmse = rmse(self);
        r = roughness(self, varargin);
        r = roughness1D(self, width, n, varargin);
        
        #
        # Call for launching gui
        #
        
        varargout = gui(self);
        
        #
        # Getting and setting additional information (accessing the info
        # struct). Defined inline here
        #  
        function val = getInfo(self, field, default)
            if isfield(self.info, field)
                val = self.info.(field);
            else
                val = default;
            end
        end
        function setInfo(self, field, value)
            self.info.(field) = value;
        end
        
        function setClean(self)
            self.IsDirty = false;
        end
    end
    
    methods (Access = private)
        setXSize_(self, xsize)
        setYSize_(self, ysize)
        setPx_(self, xpx, ypx)
        varargout = generate_xygrids_(self, varargin)
        
        update_from_xsize_(self)
        update_from_ysize_(self)
        
        upd_zlin_(self)
        
        subtract_(self, what)
        multiply_(self, factor)
        
        function dirtify(self)
            self.IsDirty = true;
        end
    end
end

def local_ReadAsciiData(filename):

    fid = fopen(filename);
    res = textscan(fid, '#s #s #s');
    fclose(fid);
    
    
    xlin = str2double(strrep(res{1}, ',', '.'));
    ylin = str2double(strrep(res{2}, ',', '.'));
    zlin = str2double(strrep(res{3}, ',', '.'));
    
    # There might be NaNs in xlin. Remove them.
    xlin = xlin[~np.isnan(xlin)]
    ylin = ylin[~np.isnan(ylin)]

    
    xoffset = min(xlin);
    yoffset = min(ylin);
    
    stepx = max(diff(xlin));
    stepy = max(diff(ylin));
    
    xpx = length(unique(xlin));
    ypx = length(unique(ylin));
    
    # Alas, a proper method SICMScan.FromLinearData(x,y,z) is missing...

    
    # Here, x and y is changed intentionally!
    [xg,yg] = meshgrid((0:xpx-1),(0:ypx-1));
    zg = griddata(xg(:),yg(:),zlin,xg,yg);
    
    o = SICM.SICMScan.FromZDataGrid(zg);
    o.setXSize(xpx*stepx);
    o.setYSize(ypx*stepy);
    o.addXOffset(xoffset);
    o.addYOffset(yoffset);
    return o


def setYSize_(self, ysize):
# Helper function: Sets the ysize property
   self.ysize = ysize

def setYSize(self, ysize,newObject=False):
    # Set the Y size  of the scan object to ysize. If available,
    # the data in ydata_lin and ydata_grid will be updated.
    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self);
        o.setYSize(ysize)
        return o
    self.setYSize_(ysize)
    self.update_from_ysize_()
    return None

def setXSize_(self, xsize):
# Helper function: sets the xsize-property
    self.xsize = xsize;

def setXSize (self, xsize, newObject=False):
    # Set the X size  of the scan object to xsize. If available,
    # the data in xdata_lin and xdata_grid will be updated.
    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self);
        o.setXSize(xsize)
        return o

    self.setXSize_(xsize);
    self.update_from_xsize_();
    return None

def setPx(self, xpx, ypx):
    # Set the x and y pixels of the object
    self.setPx_(xpx, ypx)

def setPx_(self, xpx, ypx):
# Internal function: Sets properties xpx and ypx and the corresponding
# grids
    self.xpx = xpx;
    self.ypx = ypx;
    self.generate_xygrids_();

function varargout = scaleZDefault(self)
    # Scales the z-data
    #
    # Scales the data by the factor 100/2^16, as we use it for our SICM.
    #
    # Examples:
    #    obj.scaleZDefault()

    if nargout == 0
        self.scaleZ(100/2^16);
    else
        o = SICM.SICMScan.fromSICMScan_(self);
        o.scaleZDefault;
        varargout{1} = o;
    end
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: 'Apply default scale'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {'z'}
#+GMD Immediate: 0
#+GMD Menu: 'Simple Manipulations'
#+END GUIMETADATA

function varargout = scaleZ(self, factor, varargin)
    # Scales the z-data
    #
    # Scales the data by `factor`
    #
    # Examples:
    #    obj.scale(factor)
    #
    #    Scales the data by `factor`.
    #
    #    newobj = obj.scale(factor)
    #     
    #    As above, but returns a new object instead of altering
    #    obj.
    #
    #    newobj = obj.scale(2, offset)
    #
    #    This first subtracts `offset` from the data, than scales
    #    it by a factor of 2.
    #    This is useful to transfer the data from binary values to
    #    micrometers. Assume that in a setup the DC card  maps -10V
    #    to 10V to 2^16 bits. The piezo maps 0V to 10V to 100µm.
    #    The data will be between 2^15 and 2^16. To transfer the
    #    data from binary to true lengths, use:
    #    obj.scale(100/(2^16-2^15), 2^15)
    if nargout == 0
        if nargin > 2
            self.subtract_(varargin{1});
        end
        self.multiply_(factor);
    else
        o = SICM.SICMScan.fromSICMScan_(self);
        o.scaleZ(factor, varargin{:});
        varargout{1} = o;
    end
end

function r = roughness1D(self, width, n, varargin)
# roughness1D  Computes the roughness linewise
#
# Arguments
#   width: number of pixels to take into account. Should be odd.
#   n: degree of the polynomial subtracted from the data
#   varargin: p,v pairs. Currently:
#          'Callback': function_handle
#          Called when the roughness for one line has finished. Parameters
#          are current line count and total line count
# Examples:
#   r = scan.roughness1D(11,5)
#   

    if mod(width,2) == 0
        warning('SICMScan:ParameterNotOdd', 'Increasing n by one!');
        width = width + 1;
    end
    cb = [];
    if nargin > 3
        if strcmp(varargin{1}, 'Callback')
            cb = varargin{2};
        end
    end

    halfwidth = (width-1) / 2;
    for y = 1:self.ypx
        if ~isempty(cb)
            cb(y, self.ypx);
        end
        for x = halfwidth+1:self.xpx-halfwidth
            l = self.zdata_grid(x-halfwidth:x+halfwidth, y);
            xcoords = (-halfwidth:halfwidth)';
            ftr = polyfit(xcoords, l, n);
            pvals = polyval(ftr, xcoords);
            yvals = l - pvals;
            er = (yvals-mean(yvals)).^2;
            r(x-halfwidth, y) = sqrt(mean(er));
            
        end
        
    end
    if ~isempty(cb)
        cb(y, self.ypx);
    end
end

function r = roughness(self, varargin)
# Computes the roughness (RMSE) of the scan.
#
# In general, the roughness is computed as follows:
#
# 1) A 2D-polynomial of n-th degree is fitted to the data and then
#    subtracted from the data.
# 2) The RMSE is computed
#
# The function has three optional parameters.
#
#   r = scan.roughness(n, threshold, width)
#
#         n: Is the degree of the 2D-polynomial. Max degree is 5. Default
#            value is 5.  
#
# threshold: Is a height value used applied to the data. If set, only
#            values above (note: See next parameter) this value are
#            included in the fitting of the polynomial and the RMSE
#            computation. Default threshold is -Inf.
#
#     width: Does not compute the roughness of the entire scan, but of
#            squared sections of the scan with the corresponding width.
#            Note that width has to be a odd number, otherwise width is
#            increased by 1. 
#            Here, the threshold parameter is interpreted slightly
#            different: 
#            - If the central pixel of of the square window is below the
#              threshold, the roughness of the pixels below the threshold
#              is computed, otherwise the roughness of the pixels above the
#              threshold is computed.
#            If width is given a matrix of roughness values is returned.


# Defaults:

n = 5;
threshold = -Inf;
width = NaN;


if nargin > 1
    n = varargin{1};
end
if n > 5
    n = 5;
    warning('Reduced n to five.');
end

if nargin > 2
    threshold = varargin{2};
end

if nargin > 3
    width = varargin{3};
end

if isnan(width)
    exclude = self.zdata_grid < threshold;
    scan = self.flatten( 'polyXX', n, 'Exclude', exclude(:) );
    scan.zdata_grid(exclude) = NaN;
    r = scan.rmse();
else
    if mod(width,2) == 0
        width = width + 1;
        warning('Increased width by one.');
    end
    half_width = (width-1)/2;
    nx = 0;
    ny = 0;
    r = zeros(self.xpx - 2*half_width,self.ypx - 2*half_width);
    total = (size(r,1)-1-width)*(size(r,2)-1-width);
    fprintf('Will compute #g roughness values. This might take a while.\n', total);
    fprintf('Temporarilly switching off the warning for bad equation design for fitting.\n')
    warning('off', 'curvefit:fit:equationBadlyConditioned');
    report = floor(total/100);
    fprintf('Will report every #gth computation.\n', report);
    n_total = 0;
#    tic;
    #for y = 1 : self.ypx - width - 1
    #    ny = ny +1;
    #    for x = 1 : self.xpx - width - 1
    #        n_total = n_total + 1;
    #        if mod(n_total, report) == 0
    #            fprintf('Computed the #gth roughness point', n_total);
    #            toc;
    #        end
    #        nx = nx + 1;
    #        scan = self.crop(y,x,width,width);
    #        sg = sign(self.zdata_grid(x+half_width ,y + half_width) - threshold);
    #        scan.scaleZ(sg);
    #        try
    #            r(nx,ny) = sg * scan.roughness(n, sg * threshold);
    #        catch
    #            r(nx,ny) = NaN;
    #        end
    #    end
    #    nx = 0;
    #end
    
    # trying to implement the two loops from above as a single one. 
    
    sz = size(self.zdata_grid) - width;
    
    parfor idx = 1 : total
        scan = NaN;
        sg = NaN;
        warning('off', 'curvefit:fit:equationBadlyConditioned');
        if mod(idx, report) == 0
            fprintf('Computed the #gth roughness point', n_total);
        end      
        
        [row, col] = ind2sub(sz, idx);
        try
            # crop uses col<->row syntax (bad!)
            scan = self.crop(col, row, width, width);
            sg = sign(self.zdata_grid(row + half_width ,col + half_width) - threshold);
            scan.scaleZ(sg);

        catch
            idx_x
            idx_y
            idx
        end
        try
            r(idx) = sg * scan.roughness(n, sg * threshold);
        catch
            r(idx) = NaN;
    	end
    end
    # 
    fprintf('Enabling the warning again.')
    warning('on', 'curvefit:fit:equationBadlyConditioned');
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'prop'
#+GMD Name: 'Roughness'
#+GMD Depends: {'z'}
#+GMD Changes: {}
#+GMD Immediate: 1
#+GMD Unit: '[z]'
#+END GUIMETADATA

function rmse = rmse(self)
# Computes the root of the mean of the squared error of the scan.
# Note that no flattening is applied. 
#
# This function is save to be used with NaNs in the data. 

mean_ = nanmean(self.zdata_grid(:));
diff_ = self.zdata_grid(:) - mean_;

rmse = sqrt(nanmean(diff_.^2));

function r = rms(self)
# Compute the root mean square of the scan:

    delta = self.zdata_lin - mean(self.zdata_lin);
    
    r = sqrt(mean(delta.^2));
    
end

function reviewProblematicFits(self, varargin)
# Displays every approach curve the fitproblems property of which indicates
# fit problems. Shows a yes|no|cancel button to indicate whter the fit is
# ok.
    figure;
    sz = size(self.approachcurves);
    for i = 1:length(self.zdata_lin)
        app = self.getAppCurve(i);
        if app.fitproblems == 1
            app.plotAll();
            title(sprintf('Approach curve index #g (#g, #g)', ...
                i, ind2sub(sz,i)));
            if nargin == 2
                l = get(gca, 'XLim');
                t = varargin{1} * app.fitobject.I0;
                plot(l, [t t], 'k--');
            end
            hold off;
            choice = questdlg('Is the fit ok?', ...
            'Review fits', ...
            'Yes','No (Launch fit tool)','Cancel','No (Launch fit tool)');
        
            switch choice
                case 'Yes'
                    self.approachcurves{i}.fitIsOk();
                case 'No (Launch fit tool)'
                    app.fittool();
                    return
                case 'Cancel'
                    return
            end
        end
    end
end

function l = reviewAllApproachCurves(self)
# Displays every approach curve and asks whether the index of the curve
# should be saved. an array of the saved indices will be returned.

    sz = size(self.approachcurves);
    l = ones(1,length(self.zdata_lin)) * NaN;
    for i = 1:length(self.zdata_lin)
        plot(self.approachcurves{sub2ind(sz,i)});
        choice = questdlg('Save the index of the curve?', ...
            'Review approach curves', ...
            'Yes','No','Cancel','No');
        
        switch choice
            case 'Yes'
                l(i) = 1;
        
            case 'Cancel'
            	return
        end
        l = find(l==1);
    end
end

function varargout = readAllAppCurves(self, fhandle)
# Reads all Approach Curves into the approachcurves-property. Requires a
# function handle that returns the file name of the approach curve. 
#
# The function handle must accept three arguments: x,y,i. Here, x is the
# x-value of the current data point, y is the y-value and i is the index of
# the data point (as a matlan index, hence starting at 1)
#
# Assume the approach curves are stored as:
#
# appCurve-no0.ac
# appCurve-no1.ac
# ...
#
# a good function would be
#
#   @(x,y,i)(sprintf('appCurve-no#g.ac',i))
#
#  Example:
#
#    obj.readAllAppCurves(@(x,y,i)(sprintf('appCurve-no#g.ac',i)))
#
#     Will read all appcurves as described above
#
#    newobj = obj.readAllAppCurves(@(x,y,i)(sprintf('appCurve-no#g.ac',i)))
#
#       As above, but returns a new object instead of modifying the
#       original one. 

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.readAllAppCurves(fhandle);
        varargout{1} = o;
        return
    end
    
    
    self.approachcurves = cell(...
        size(self.zdata_grid,1),...
        size(self.zdata_grid,2)); 
    
    # Loop through all data points
    for i = 1:length(self.zdata_lin)
        [y,x] = ind2sub(size(self.zdata_grid), i);
        fname = feval(fhandle,x,y,i);
        self.approachcurves(y,x) = {SICM.SICMAppCurve.FromFile(fname)};
    end

function varargout = profile (self, varargin)
# Determination of a height profile. Uses the improfile function of
# matlab.
#
# Examples:
# --------
#
# p = scan.profile()
#   Opens an image of the scan and allows to select a profile as in the
#   matlab function improfile. 
#  
# p = scan.profile(<arguments>)
#
#   If called with non-empty arguments, these arguments are passed to
#   improfile. Note that in this case, the call to improfile is:
#
#   improfile(self.xdata_lin, self.ydata_lin, self.zdata_grid, <arguments>)
#
# For return values, see the improfile docs.
# See also IMPROFILE

if nargin > 1
    [varargout{1:nargout}] = improfile(...#
        self.zdata_grid, varargin{:} );

else
    figure; 
    self.imagesc();
    [varargout{1:nargout}] = improfile();
end

# The following is for debugging 
#plot(self);
#hold on;
#plot3([p1(1) p2(1)],[p1(2) p2(2)],[101 101],'r-');


#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meas'
#+GMD Name: 'Measure Profile'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {}
#+GMD Immediate: 0
#+GMD Menu: 'Measurements'
#+END GUIMETADATA

function varargout = plot(self, varargin)
# Plots a 3D-plot of the data 
#
# Simply calls SURFACE
#
# See also SURFACE
   a = self.surface(varargin{:}); 
   if nargout > 0
       varargout{1} = a;
   end
end

function varargout = normalize(self)
# Normalizes the z-data
#
#    Examples:
#
#       obj.normaliez()
#
#         Normalizes the z-data of `obj`to be between 0 and 1.
#
#       newobj = obj.normalize()
#
#         As above, but returns a new SICMScan object instead of modifying
#         the data of `obj`.

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.normalize();
        varargout{1} = o;
        return
    end
    
    self.subtract_(min(self));
    self.multiply_(1./max(self));
end

function multiply_(self, factor)
# Internal function: Multiply every z-value by factor
    self.zdata_grid = self.zdata_grid*factor;
    self.upd_zlin_();
end

function m = min(self)
# Returns the minimum z-value
    m = min(self.zdata_lin);
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'prop'
#+GMD Name: 'Min'
#+GMD Depends: {'z'}
#+GMD Changes: {}
#+GMD Immediate: 1
#+GMD Unit: '[z]'
#+END GUIMETADATA

function m = max(self)
# Returns the maximum z-value
    m = max(self.zdata_lin);
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'prop'
#+GMD Name: 'Max'
#+GMD Depends: {'z'}
#+GMD Changes: {}
#+GMD Immediate: 1
#+GMD Unit: '[z]'
#+END GUIMETADATA

function varargout = inverse(self)
# This function inverses the z-data of the object.
#
# Examples:
#    obj.inverse()
#       The data of obj is inversed.
#
#    newobj = obj.inverse()
#
#    Returns a new object with the inversed data of obj. obj is not
#    modified.

    # If an output argument is specified, copy the object and call
    # the inverse() method of this object. Then return it and leave the
    # method.
    if nargout == 1
       o = SICM.SICMScan.fromSICMScan_(self);
       o.inverse();
       varargout{1} = o;
       return
    end

    # now do the work:
    self.multiply_(-1);
end

function varargout = interpolate_wrapper( self, method, steps )
# wrapper for the interpolation method with arguments in different order,
# as required for the GUI.

if nargout > 0
    varargout{1} = self.interpolate( steps, method );
else
    self.interpolate( steps, method );
end


#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: {'by cubic splines', 'by nearest neighbour'}
#+GMD FixedArgs: {'spline', 'nearest'}
#+GMD VarArgs: {struct('type','int','desc','Interpolation steps'),struct('type','int','desc','Interpolation steps')}
#+GMD Depends: {}
#+GMD Changes: {'x','y','z'}
#+GMD Immediate: 0
#+GMD Menu: 'Interpolation'
#+END GUIMETADATA

function varargout = interpolate(self, steps, varargin)

# Interpolating the data using different methods
#
#    Examples: 
#      
#      obj.interpolate(steps, method)
#        
#        interpolate the data with 'steps' interpolation steps unsing
#        method 'method'. If 'method' is not provided, 'spline' is used as
#        default.
#
#      newobj = obj.interpolate(steps, method)
#
#        As above, but returns a new SICMScan object with the interpolated
#        data.
#
#  
# The methods available are can be found in the documentation of the 
# griddedInterpolant class of Matlab.
#
# SEE ALSO: griddedinterpolant

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.interpolate(steps, varargin{:})
        varargout{1} = o;
        return
    end

    method = 'spline';

    if nargin == 3
        method = varargin{1};
    end

    if self.xdata_grid(1,1) == self.xdata_grid(2,1)
        F = griddedInterpolant(self.xdata_grid', self.ydata_grid', ...
            self.zdata_grid', method);
    else
        F = griddedInterpolant(self.xdata_grid, self.ydata_grid, ...
            self.zdata_grid, method);
    end
    min_x = min(self.xdata_lin);
    min_y = min(self.ydata_lin);
    max_x = max(self.xdata_lin);
    max_y = max(self.ydata_lin);
    [xg, yg] = ...
        meshgrid(min_x:self.stepx/steps:max_x, ...
                 min_y:self.stepy/steps:max_y);
    zg = F(xg', yg');
    self.zdata_grid = zg';
    self.xdata_grid = xg;
    self.ydata_grid = yg;
    self.upd_zlin_();
    self.xdata_lin = self.xdata_grid(:);
    self.ydata_lin = self.ydata_grid(:);

    self.xpx = length(min_x:self.stepx/steps:max_x);
    self.ypx = length(min_y:self.stepy/steps:max_y);
    self.stepx = self.xsize / self.xpx;
    self.stepy = self.ysize / self.ypx;
    
function varargout = imagesc(self)

    a = imagesc(self.zdata_grid);
    
    if nargout == 1
        varargout{1} = a;
    end
end

function info = getInterfaceInformation(self)
# reads the available additional information in the GUI-metadata at the end
# of the *.m-files and returns them as a structure
    [p, ~, ~] = fileparts(which(class(self)));

    dirinfo = dir([p filesep '*.m']);
    info = {};
    for finfo = dirinfo'
        if finfo.isdir
            continue
        end
        gmd = lcl_read_gmd([p filesep finfo.name]);
        if ~isempty(gmd) && isfield(gmd, 'Type')
            type = gmd.Type;
            if strcmp(type(1), '''')
                type = type(2:end);
            end
            if strcmp(type(end), '''')
                type = type(1:end-1);
            end
            
            gmd = rmfield(gmd, 'Type');
            [~,gmd.file,gmd.fileext] = fileparts(finfo.name);
            if ~isfield(info, type)
                info.(type) = {};
            end
            info.(type)(end+1) = {gmd};
            
        end
    
    end

end

function gmd = lcl_read_gmd(fn)
    gmd = {};
    fid = fopen(fn, "r");
    inGMD = false;
    while ~feof(fid)
        tline = fgetl(fid);     
        if ~inGMD
            matches = strfind(tline, '#+BEGIN GUIMETADATA: Do not delete');
            if ~isempty(matches)
                inGMD = true;
            end
        else
            [tok,~] = regexp(tline, '#\+GMD\s(?<field>\w*):\s(?<value>.*)', 'names');
            
            if numel(tok) > 0
                fchar = lcl_unquote(tok.field);
                gmd.(fchar) = eval(tok.value);
            end
        end   
    end
    fclose(fid);
end

function str = lcl_unquote(str)
    wasstring = false;
    if isstring(str)
        wasstring = true;
        str = char(str);
    end
    if strcmp(str(1), '''')
        str = str(2:end);
    end
	if strcmp(str(end), '''')
        str = str(1:end-1);
    end
    if wasstring
        str = string(str);
    end
end

function app = getAppCurve(self, idx, varargin)
# return the approach curve with index idx

if nargin == 3
    idx2 = varargin{1};
    app = self.approachcurves{idx, idx2};
else
    app = self.approachcurves{...
            ind2sub(size(self.zdata_grid), idx)...
        };
end

function varargout = generate_xygrids_(self, varargin)
# Helper function: Generate (interpolated) x- and y-grids
#
#    Examples: 
#      self.generate_xygrids_()
#   
#        Generates the x- and y-data grids of the object `self`. It considers 
#        self.stepx and self.stepy, if available, otherwise uses a step 
#        size of 1 (corresponding to values as pixels numbers). This also
#        updates xdata_lin and ydata_lin.
#
#      [xg, yg] = self.generate_xygrids_()
#
#        As above, but instead of changing the object `self`, it returns
#        the grids.
#
#      [xg, yg] = self.generate_xygrids_(interp)
#
#        As above, but the grids are interpolated. Instead of generating a
#        grid with spacing 1, the spacing is 1/interp

    interp = 1;
    if nargin > 1
        interp = varargin{1};
    end
    stepx_ = self.stepx;
    stepy_ = self.stepy;
    if isnan(stepx_)
        stepx_ = 1;
    end
    if isnan(stepy_)
        stepy_ = 1;
    end
    
    xoff = 0;
    yoff = 0;
    if ~isnan(self.xdata_lin)
        xoff = min(self.xdata_lin);
    end
    if ~isnan(self.ydata_lin)
        yoff = min(self.ydata_lin);
    end
    
    [xg, yg] = meshgrid((0:1/interp:self.xpx-1)*stepx_, (0:1/interp:self.ypx-1)*stepy_);
    xg = xg' + xoff;
    yg = yg' + yoff;
    if nargout == 0
        self.xdata_grid = xg;
        self.ydata_grid = yg;
        self.xdata_lin = xg(:);
        self.ydata_lin = yg(:);
    else
        varargout{1}=xg;
        varargout{2}=yg;
    end
end

function o = FromZDataGrid(zdatagrid)
	# Convert a grid of z-data into a SICMScan object.
    #
    # See also SICMSCAN, FROMFILE
    o = SICM.SICMScan();
    o.zdata_grid = zdatagrid';
    o.zdata_lin = zdatagrid(:);
    sz = size(zdatagrid);
    o.setPx(sz(2), sz(1));
    o.setXSize(sz(2));
    o.setYSize(sz(1));
    o.setClean();
end

function o = fromSICMScan_(obj)
    # Internal function
    # This function copies a SICMScan object.
    
    o = obj.copy();
    o.setClean();
end

function o = FromFile(varargin)
    # Reads data from a file into a SICMScan object
    #
    #    To allow importing different types of data, this functions
    #    uses different importer functions. They are stored in the
    #    constant importer property of the SICMScan class.
    #
    #    Examples:
    #      obj = SICMScan.FromFile
    #
    #      Opens a file dialog and reads the selected file in an
    #      SICMScan object.
    #
    #      obj = SICMScan.Fromfile(filename)
    #      Reads the file `filename` into a SICMScan object
    #
    #    See also IMPORTER
    
    # temporary  instance of the class
    tmp = SICM.SICMScan;
    if nargin == 0
        [finame, pname] = tmp.getFilename_();
        if finame == 0
            return
        end
        filename = fullfile(pname, finame);
    else
        filename = varargin{1};
    end
 
    o = tmp.getObjectFromFilename_(filename);
    o.info.filename = filename;
    delete(tmp);
    o.setClean();

end

function o = FromExampleData()
# Generates an SICMScan object from exemplary data.

z = [54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 54.9000000000000 54.9000000000000 54.9000000000000 54.9000000000000 54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 55 54.9500000000000 54.9500000000000 54.9500000000000 54.9500000000000 55 55.0490000000000 55 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0490000000000 55.0990000000000 55.0990000000000 55.0990000000000 55.0990000000000 55.0990000000000 55.0990000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.2000000000000 55.2000000000000 55.1500000000000 55.2000000000000 55.2500000000000 55.2000000000000 55.2500000000000 55.2000000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2990000000000 55.2990000000000 55.2990000000000 55.2990000000000 55.2990000000000 55.3490000000000 55.5990000000000 55.5490000000000 55.3490000000000 55.2990000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5990000000000 55.5990000000000 55.5990000000000 55.5990000000000;55.3050000000000 55.1540000000000 55.1540000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.1540000000000 55.2050000000000 55.2050000000000 55.2050000000000 55.2050000000000 55.2050000000000 55.2050000000000 55.2050000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.2550000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.3540000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5550000000000 55.5550000000000 55.5050000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.5550000000000 55.6040000000000 55.6540000000000 55.6540000000000;55.2090000000000 55.2090000000000 55.1100000000000 55.1100000000000 55.0600000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1100000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1100000000000 55.1100000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.1590000000000 55.2090000000000 55.2090000000000 55.2090000000000 55.2090000000000 55.2090000000000 55.2090000000000 55.2590000000000 55.2590000000000 55.2590000000000 55.2590000000000 55.2090000000000 55.2090000000000 55.3100000000000 55.2590000000000 55.2590000000000 55.2590000000000 55.3100000000000 55.3100000000000 55.3100000000000 55.2590000000000 55.3100000000000 55.3100000000000 55.3100000000000 55.3600000000000 55.3100000000000 55.3100000000000 55.3100000000000 55.3600000000000 55.4090000000000 55.3600000000000 55.3600000000000 55.3100000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.3600000000000 55.4090000000000 55.4090000000000 55.4590000000000 55.4090000000000 55.4090000000000 55.4090000000000 55.4090000000000 55.4590000000000 55.4590000000000 55.4590000000000 55.5090000000000 55.4590000000000 55.4590000000000 55.5090000000000 55.5090000000000 55.5090000000000 55.5090000000000 55.5090000000000 55.5600000000000 55.5600000000000 55.5090000000000 55.5090000000000 55.5600000000000 55.5600000000000 55.5600000000000 55.5600000000000 55.5600000000000 55.6100000000000 55.6100000000000 55.5600000000000 55.6100000000000 55.6100000000000;55.2150000000000 55.1650000000000 55.2150000000000 55.1650000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1650000000000 55.1650000000000 55.1650000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1150000000000 55.1650000000000 55.2150000000000 55.2150000000000 55.2150000000000 55.1650000000000 55.1650000000000 55.2150000000000 55.1650000000000 55.1650000000000 55.1650000000000 55.1650000000000 55.2150000000000 55.2150000000000 55.2150000000000 55.2150000000000 55.2150000000000 55.2640000000000 55.2640000000000 55.2150000000000 55.2150000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.3140000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3140000000000 55.3650000000000 55.3650000000000 55.3650000000000 55.3140000000000 55.3140000000000 55.3650000000000 55.3650000000000 55.4150000000000 55.4150000000000 55.9650000000000 55.4650000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5640000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.6150000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.6150000000000 55.6150000000000 55.5640000000000 55.5640000000000 55.6150000000000;55.2700000000000 55.1690000000000 55.1690000000000 55.1690000000000 55.1690000000000 55.1190000000000 55.1690000000000 55.1190000000000 55.1690000000000 55.1690000000000 55.1690000000000 55.1190000000000 55.1690000000000 55.1690000000000 55.1690000000000 55.1190000000000 55.1690000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2700000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2200000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.2700000000000 55.3190000000000 55.3190000000000 55.3190000000000 55.3190000000000 55.3190000000000 55.3190000000000 55.3690000000000 55.3690000000000 55.3190000000000 55.4700000000000 55.4700000000000 55.4190000000000 55.3690000000000 55.3690000000000 55.3690000000000 55.3690000000000 55.3690000000000 55.3690000000000 55.4190000000000 55.3690000000000 55.4190000000000 55.3690000000000 55.4190000000000 55.4700000000000 55.4190000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.4700000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.4700000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.6190000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.6190000000000 55.5690000000000 55.6190000000000 55.5690000000000 55.6190000000000 55.6190000000000 55.6190000000000 55.6190000000000;55.2240000000000 55.2240000000000 55.1740000000000 55.1250000000000 55.1740000000000 55.1740000000000 55.1250000000000 55.1740000000000 55.1250000000000 55.1250000000000 55.1250000000000 55.1250000000000 55.1250000000000 55.1250000000000 55.1740000000000 55.1740000000000 55.1740000000000 55.1740000000000 55.2750000000000 55.2750000000000 55.3250000000000 55.3250000000000 55.3250000000000 55.2750000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.1740000000000 55.1740000000000 55.1740000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.2240000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.2750000000000 55.3250000000000 55.3750000000000 55.3250000000000 55.3250000000000 55.4740000000000 55.4740000000000 55.3250000000000 55.3750000000000 55.3250000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.4240000000000 55.4240000000000 55.3750000000000 55.4240000000000 55.4240000000000 55.4240000000000 55.4740000000000 55.4240000000000 55.4740000000000 55.4740000000000 55.4740000000000 55.4740000000000 55.4740000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5750000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5750000000000 55.5250000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6740000000000;55.1800000000000 55.1800000000000 55.1800000000000 55.1300000000000 55.1300000000000 55.1300000000000 55.1300000000000 55.1300000000000 55.1800000000000 55.1300000000000 55.1300000000000 55.1800000000000 55.1800000000000 55.1800000000000 55.1300000000000 55.1800000000000 55.1800000000000 55.1800000000000 55.1800000000000 55.2290000000000 55.2290000000000 55.1800000000000 55.2290000000000 55.2290000000000 55.2290000000000 55.1800000000000 55.2290000000000 55.2290000000000 55.2790000000000 55.2790000000000 55.2290000000000 55.2290000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.2790000000000 55.3300000000000 55.3300000000000 55.2790000000000 55.3300000000000 55.3300000000000 55.3300000000000 55.3300000000000 55.3300000000000 55.3300000000000 55.3300000000000 55.3800000000000 55.3800000000000 55.3800000000000 55.3800000000000 55.3800000000000 55.3800000000000 55.4790000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.3800000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5290000000000 55.5800000000000 55.5800000000000 55.5800000000000 55.5800000000000 55.5800000000000 55.5800000000000 55.6300000000000 55.6300000000000 55.6300000000000;55.2350000000000 55.1850000000000 55.1850000000000 55.1850000000000 55.1850000000000 55.1340000000000 55.1340000000000 55.1850000000000 55.1340000000000 55.1850000000000 55.1340000000000 55.1340000000000 55.1340000000000 55.1340000000000 55.1850000000000 55.2350000000000 55.3840000000000 55.4350000000000 55.4850000000000 55.5840000000000 55.6850000000000 55.6340000000000 55.4850000000000 55.4850000000000 55.8340000000000 55.6850000000000 55.6340000000000 55.5840000000000 55.5340000000000 55.5340000000000 55.3340000000000 55.2840000000000 55.2840000000000 55.2350000000000 55.2350000000000 55.2840000000000 55.2350000000000 55.2350000000000 55.2350000000000 55.2840000000000 55.3340000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.2840000000000 55.3340000000000 55.3340000000000 55.3340000000000 55.3340000000000 55.3340000000000 55.3340000000000 55.3340000000000 55.3840000000000 55.6850000000000 55.7350000000000 55.4850000000000 55.3840000000000 55.3840000000000 55.3840000000000 55.3840000000000 55.3840000000000 55.3840000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000;55.1890000000000 55.1890000000000 55.1390000000000 55.1390000000000 55.1890000000000 55.1890000000000 55.1390000000000 55.1390000000000 55.1390000000000 55.1390000000000 55.1390000000000 55.1390000000000 55.1390000000000 55.1890000000000 55.1890000000000 55.2400000000000 55.4900000000000 55.5900000000000 55.5900000000000 55.5400000000000 55.6390000000000 55.6890000000000 55.5900000000000 55.5900000000000 55.6890000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5400000000000 55.6390000000000 55.7900000000000 55.4390000000000 55.2900000000000 55.2400000000000 55.2400000000000 55.2400000000000 55.2400000000000 55.2400000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.2900000000000 55.3400000000000 55.3400000000000 55.3400000000000 55.3400000000000 55.3400000000000 55.3400000000000 55.3400000000000 55.3890000000000 55.3890000000000 55.4390000000000 55.4390000000000 55.3890000000000 55.6890000000000 55.7400000000000 55.4390000000000 55.4390000000000 55.3890000000000 55.4390000000000 55.4390000000000 55.4390000000000 55.4390000000000 55.4390000000000 55.4390000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.4900000000000 55.5400000000000 55.5400000000000 55.5400000000000 55.5400000000000 55.5400000000000 55.5400000000000 55.5400000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.6390000000000 55.5900000000000 55.6390000000000 55.5900000000000 55.6390000000000 55.6890000000000 55.6390000000000;55.2440000000000 55.2440000000000 55.2440000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.1940000000000 55.2440000000000 55.2440000000000 55.4940000000000 55.5950000000000 55.5950000000000 55.4940000000000 55.4940000000000 55.5950000000000 55.6940000000000 55.6940000000000 55.7440000000000 55.6940000000000 55.5950000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.6450000000000 55.7440000000000 55.6940000000000 55.4440000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.3450000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.3450000000000 55.3950000000000 55.3450000000000 55.3450000000000 55.3450000000000 55.3450000000000 55.3950000000000 55.3450000000000 55.3450000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.3950000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.5440000000000 55.4940000000000 55.4940000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000;55.2000000000000 55.2000000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.2000000000000 55.1500000000000 55.1500000000000 55.0990000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.1500000000000 55.2500000000000 55.5490000000000 55.5490000000000 55.4000000000000 55.4000000000000 55.4500000000000 55.5000000000000 55.5990000000000 55.6500000000000 55.7000000000000 55.5990000000000 55.5490000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.7500000000000 55.9000000000000 55.8490000000000 55.5990000000000 55.4500000000000 55.2990000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2990000000000 55.2990000000000 55.2990000000000 55.2500000000000 55.2990000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.2500000000000 55.3490000000000 55.2990000000000 55.2990000000000 55.3490000000000 55.2990000000000 55.3490000000000 55.3490000000000 55.4000000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4500000000000 55.4500000000000 55.4000000000000 55.4000000000000 55.5000000000000 55.4500000000000 55.4500000000000 55.5000000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.4500000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5490000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5990000000000;55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1040000000000 55.1540000000000 55.1540000000000 55.2550000000000 55.5050000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4550000000000 55.5050000000000 55.5550000000000 55.6540000000000 55.7050000000000 55.6540000000000 55.5550000000000 55.4550000000000 55.4550000000000 55.5550000000000 55.7050000000000 55.7550000000000 55.7550000000000 55.7050000000000 55.8540000000000 55.5050000000000 55.4040000000000 55.5050000000000 55.8540000000000 55.9550000000000 55.9550000000000 56.0550000000000 55.5050000000000 55.3050000000000 55.3050000000000 55.2550000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3540000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3050000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.4040000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 56.1040000000000 55.6040000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.6040000000000;55.2100000000000 55.1600000000000 55.1600000000000 55.1600000000000 55.1110000000000 55.1600000000000 55.1110000000000 55.1600000000000 55.2100000000000 55.1600000000000 55.1600000000000 55.1600000000000 55.1600000000000 55.1600000000000 55.3610000000000 55.5610000000000 55.4600000000000 55.4600000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.5110000000000 55.5610000000000 55.5610000000000 55.7610000000000 55.7100000000000 55.6110000000000 55.4600000000000 55.4100000000000 55.5110000000000 55.7100000000000 55.8110000000000 55.7610000000000 55.7100000000000 56.1110000000000 56.0610000000000 55.8610000000000 55.6600000000000 55.8110000000000 55.9100000000000 56.0110000000000 55.9100000000000 55.7610000000000 55.5610000000000 55.4100000000000 55.4100000000000 55.3110000000000 55.3110000000000 55.3110000000000 55.3110000000000 55.3110000000000 55.3110000000000 55.3110000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.3610000000000 55.3610000000000 55.3610000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.6110000000000 55.6600000000000 55.6110000000000 55.6110000000000 55.5610000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6600000000000 55.6600000000000 55.6110000000000;55.2160000000000 55.1660000000000 55.1660000000000 55.1660000000000 55.1660000000000 55.2160000000000 55.2160000000000 55.1660000000000 55.1660000000000 55.1660000000000 55.1660000000000 55.1660000000000 55.2160000000000 55.2160000000000 55.4160000000000 55.5670000000000 55.5160000000000 55.3670000000000 55.3670000000000 55.4660000000000 55.4160000000000 55.4660000000000 55.4660000000000 55.6660000000000 55.7660000000000 55.7160000000000 55.6660000000000 55.5670000000000 55.5160000000000 55.5670000000000 55.7160000000000 55.8670000000000 55.8670000000000 56.1660000000000 56.1660000000000 56.1660000000000 56.1170000000000 55.9160000000000 55.8170000000000 55.8670000000000 55.9660000000000 55.7660000000000 55.8670000000000 55.6660000000000 55.5160000000000 55.4660000000000 55.3670000000000 55.3670000000000 55.3670000000000 55.3670000000000 55.4160000000000 55.3670000000000 55.3670000000000 55.3670000000000 55.3670000000000 55.3670000000000 55.4660000000000 55.4160000000000 55.4660000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.5160000000000 55.5160000000000 55.5670000000000 55.5670000000000 55.5160000000000 55.5160000000000 55.5160000000000 55.5670000000000 55.6170000000000 55.6660000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6660000000000 55.6170000000000 55.6170000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000;55.2220000000000 55.2220000000000 55.2720000000000 55.2720000000000 55.2220000000000 55.2220000000000 55.2220000000000 55.2220000000000 55.1730000000000 55.2220000000000 55.2220000000000 55.2720000000000 55.2720000000000 55.3730000000000 55.5730000000000 55.6730000000000 55.6730000000000 55.4230000000000 55.3730000000000 55.4230000000000 55.4230000000000 55.4720000000000 55.4720000000000 55.6230000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.6730000000000 55.6730000000000 55.7220000000000 55.8230000000000 55.8730000000000 56.0730000000000 56.0730000000000 56.1230000000000 56.0730000000000 56.0730000000000 56.0220000000000 55.9230000000000 55.8730000000000 55.7220000000000 55.7220000000000 55.6730000000000 55.7220000000000 55.7220000000000 55.5220000000000 55.4720000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4720000000000 55.4230000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.4230000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.5220000000000 55.5220000000000 55.4720000000000 55.4720000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.6230000000000 55.6230000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.6230000000000 55.6230000000000 55.6730000000000 55.6230000000000 55.6230000000000 55.7220000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000;55.2780000000000 55.2780000000000 55.2290000000000 55.2780000000000 55.2290000000000 55.2290000000000 55.2290000000000 55.2780000000000 55.2780000000000 55.2780000000000 55.2780000000000 55.2780000000000 55.3790000000000 55.5780000000000 55.7290000000000 55.7290000000000 55.5780000000000 55.4290000000000 55.4290000000000 55.4290000000000 55.3790000000000 55.4290000000000 55.4790000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.7290000000000 55.6790000000000 55.7290000000000 55.8280000000000 55.8280000000000 55.8790000000000 55.9290000000000 56.0780000000000 56.0280000000000 55.9290000000000 55.8790000000000 55.8280000000000 55.8280000000000 55.7780000000000 55.7290000000000 55.6790000000000 55.7780000000000 55.9290000000000 55.8280000000000 55.7290000000000 55.6290000000000 55.4290000000000 55.3790000000000 55.3790000000000 55.3790000000000 55.4290000000000 55.3790000000000 55.3790000000000 55.4790000000000 55.4790000000000 55.4290000000000 55.4290000000000 55.4290000000000 55.4290000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.4790000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.6290000000000 55.6290000000000 55.6790000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6290000000000 55.6290000000000 55.7290000000000 55.6790000000000 55.6790000000000 55.6790000000000;55.2840000000000 55.2350000000000 55.2350000000000 55.2350000000000 55.2350000000000 55.2840000000000 55.2350000000000 55.2350000000000 55.2350000000000 55.2350000000000 55.3840000000000 55.5340000000000 55.5840000000000 55.7350000000000 55.8340000000000 55.9850000000000 55.8840000000000 55.6340000000000 55.5340000000000 55.4850000000000 55.4350000000000 55.4350000000000 55.4850000000000 55.4850000000000 55.5840000000000 55.6340000000000 55.7350000000000 55.8340000000000 56.2350000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.8840000000000 55.8340000000000 55.8340000000000 55.8840000000000 55.9850000000000 55.9850000000000 55.6340000000000 55.6850000000000 56.0340000000000 55.9850000000000 56.0340000000000 55.8340000000000 55.6340000000000 55.4350000000000 55.4350000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4350000000000 55.4350000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.5340000000000 55.5340000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.4850000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.5840000000000 55.6340000000000 55.5840000000000 55.5840000000000 55.6340000000000 55.5840000000000 55.6340000000000 55.6340000000000 55.6850000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000;55.3400000000000 55.2910000000000 55.2910000000000 55.2410000000000 55.2410000000000 55.2410000000000 55.2410000000000 55.2410000000000 55.2410000000000 55.2910000000000 55.5900000000000 55.7410000000000 55.8400000000000 55.7910000000000 55.8900000000000 55.7410000000000 55.6910000000000 55.6400000000000 55.5900000000000 55.4910000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4910000000000 55.5900000000000 55.6400000000000 55.6910000000000 55.9410000000000 56.3900000000000 55.6400000000000 55.5900000000000 55.5900000000000 55.6400000000000 55.8400000000000 56.0410000000000 55.9410000000000 55.9410000000000 55.8400000000000 55.8400000000000 55.8900000000000 55.9410000000000 55.7410000000000 55.6400000000000 55.6400000000000 55.7410000000000 55.9910000000000 55.9910000000000 55.8400000000000 55.5900000000000 55.4910000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5410000000000 55.5410000000000 55.5410000000000 55.5410000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.6400000000000 55.5900000000000 55.5900000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000;55.3470000000000 55.2470000000000 55.2970000000000 55.2970000000000 55.2470000000000 55.2470000000000 55.2970000000000 55.2470000000000 55.2970000000000 55.3470000000000 55.5970000000000 56.0970000000000 55.6960000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.5970000000000 55.6460000000000 55.7470000000000 55.8470000000000 55.9460000000000 55.6960000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6960000000000 55.8470000000000 55.8470000000000 55.7970000000000 55.8470000000000 55.8960000000000 55.9460000000000 55.7970000000000 55.6960000000000 55.6460000000000 55.6460000000000 55.7470000000000 55.8960000000000 55.8960000000000 55.8470000000000 55.6460000000000 55.4970000000000 55.3960000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4460000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000;55.3030000000000 55.3030000000000 55.2520000000000 55.2520000000000 55.2520000000000 55.3030000000000 55.2520000000000 55.2020000000000 55.2020000000000 55.2520000000000 55.5530000000000 56.1520000000000 55.9020000000000 55.6520000000000 55.5530000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5530000000000 55.5020000000000 55.5020000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.6030000000000 55.7020000000000 55.8030000000000 55.7520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.7520000000000 55.8030000000000 55.8530000000000 55.9020000000000 55.8530000000000 55.8030000000000 55.7020000000000 55.6520000000000 55.6520000000000 55.8030000000000 55.9520000000000 55.7520000000000 55.6520000000000 55.5020000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.5020000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.5020000000000 55.4520000000000 55.4520000000000 55.4520000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.7020000000000 55.7020000000000 55.7020000000000 55.7020000000000 55.7020000000000 55.6520000000000 55.6520000000000 55.7020000000000 55.7020000000000 55.6520000000000 55.7020000000000;55.3080000000000 55.2580000000000 55.2580000000000 55.2580000000000 55.2580000000000 55.2580000000000 55.2580000000000 55.3080000000000 55.3080000000000 55.2580000000000 55.5080000000000 56.1090000000000 55.8590000000000 55.8080000000000 55.6090000000000 55.5580000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.5580000000000 55.5080000000000 55.5080000000000 55.4580000000000 55.5080000000000 55.6590000000000 55.7580000000000 55.9090000000000 55.8080000000000 55.7580000000000 55.7580000000000 55.7080000000000 55.6590000000000 55.6590000000000 55.7580000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.7080000000000 55.6590000000000 55.6590000000000 55.7080000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.5580000000000 55.5080000000000 55.4580000000000 55.4090000000000 55.4090000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6590000000000 55.6590000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000;55.3140000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.3140000000000 55.6650000000000 56.2150000000000 55.9150000000000 55.7640000000000 55.7150000000000 55.5640000000000 55.5140000000000 55.5140000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.6150000000000 55.7640000000000 55.9150000000000 55.9150000000000 55.8650000000000 55.8650000000000 55.7640000000000 55.6650000000000 55.6650000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.5640000000000 55.7150000000000 55.8650000000000 55.8140000000000 55.6150000000000 55.5140000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4150000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000;55.3200000000000 55.2210000000000 55.2210000000000 55.2210000000000 55.2210000000000 55.2210000000000 55.3200000000000 55.4710000000000 55.4210000000000 55.8200000000000 56.2210000000000 56.0200000000000 55.8700000000000 55.7210000000000 55.6200000000000 55.5700000000000 55.5200000000000 55.5200000000000 55.5700000000000 55.5700000000000 55.5700000000000 55.5700000000000 55.5700000000000 55.4710000000000 55.5200000000000 55.5700000000000 55.6200000000000 55.8200000000000 55.8200000000000 55.9710000000000 55.8200000000000 55.7700000000000 55.7700000000000 55.7210000000000 55.7210000000000 55.7700000000000 55.8200000000000 55.7700000000000 55.6710000000000 55.6200000000000 55.5200000000000 55.5200000000000 55.5700000000000 55.6710000000000 55.6710000000000 55.5700000000000 55.5200000000000 55.4710000000000 55.4710000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4710000000000 55.4210000000000 55.4210000000000 55.5200000000000 55.4710000000000 55.4710000000000 55.4710000000000 55.4710000000000 55.4210000000000 55.4710000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5700000000000 55.5700000000000 55.5200000000000 55.5700000000000 55.6200000000000 55.5700000000000 55.5700000000000 55.5700000000000 55.6200000000000 55.6200000000000 55.5700000000000 55.6200000000000 55.6200000000000 55.6200000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.7210000000000 55.7210000000000 55.7210000000000 55.7210000000000;55.3260000000000 55.2770000000000 55.2770000000000 55.2770000000000 55.2770000000000 55.2270000000000 55.2770000000000 55.3760000000000 55.5270000000000 55.7270000000000 55.9770000000000 55.9770000000000 55.8760000000000 55.7770000000000 55.7270000000000 55.6760000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6760000000000 55.7770000000000 56.0270000000000 55.9770000000000 55.7770000000000 55.7270000000000 55.7770000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9770000000000 56.0270000000000 56.0270000000000 55.9770000000000 55.9260000000000 55.9260000000000 55.7770000000000 55.6760000000000 55.5760000000000 55.5760000000000 55.6260000000000 55.7270000000000 55.5760000000000 55.4770000000000 55.5270000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.4770000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5760000000000 55.5760000000000 55.5270000000000 55.5760000000000 55.5760000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6260000000000 55.6760000000000 55.6760000000000 55.6760000000000 55.6760000000000 55.6760000000000 55.6760000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7770000000000 55.7270000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000;55.4320000000000 55.3820000000000 55.3820000000000 55.3330000000000 55.3820000000000 55.3330000000000 55.4320000000000 55.4830000000000 55.6320000000000 55.5830000000000 55.7830000000000 55.9320000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6820000000000 55.6820000000000 55.8330000000000 56.0330000000000 56.1320000000000 56.0830000000000 56.0830000000000 56.0330000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.1320000000000 56.0830000000000 56.1320000000000 56.2830000000000 56.2830000000000 56.2830000000000 56.2330000000000 56.1820000000000 56.0830000000000 55.9320000000000 55.8330000000000 55.7330000000000 55.6320000000000 55.6320000000000 55.6820000000000 55.5330000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.4830000000000 55.4830000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.5830000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.5830000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6320000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.7330000000000 55.7330000000000;55.3390000000000 55.3390000000000 55.3390000000000 55.2890000000000 55.3390000000000 55.3390000000000 55.3390000000000 55.4380000000000 55.7380000000000 55.8390000000000 55.8390000000000 55.7890000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.5390000000000 55.6380000000000 55.6380000000000 55.5890000000000 55.5390000000000 55.6380000000000 55.8390000000000 55.9380000000000 55.9880000000000 55.9880000000000 55.9880000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0890000000000 56.2380000000000 56.3390000000000 56.4380000000000 56.4380000000000 56.4880000000000 56.5890000000000 56.6380000000000 56.3880000000000 56.0890000000000 55.9380000000000 55.7890000000000 55.7380000000000 56.0390000000000 55.8390000000000 55.5390000000000 55.4380000000000 55.4380000000000 55.3880000000000 55.3880000000000 55.4880000000000 55.4880000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4380000000000 55.4380000000000 55.4380000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.5890000000000 55.4880000000000 55.5890000000000 55.5890000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.6380000000000 55.6380000000000 55.6380000000000 55.6380000000000 55.6380000000000 55.6380000000000 55.6880000000000 55.6380000000000 55.6880000000000 55.6380000000000 55.6880000000000 55.6880000000000 55.6880000000000 55.6880000000000 55.6880000000000;55.3450000000000 55.2940000000000 55.3450000000000 55.2940000000000 55.3450000000000 55.2940000000000 55.2940000000000 55.2940000000000 55.4440000000000 55.6940000000000 55.6450000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.4940000000000 55.4940000000000 55.4440000000000 55.6450000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.9440000000000 56.0440000000000 56.1450000000000 56.1940000000000 56.2940000000000 56.4440000000000 56.5440000000000 56.5440000000000 56.7440000000000 56.9940000000000 56.9940000000000 56.6940000000000 56.3450000000000 56.1450000000000 56.3450000000000 55.8450000000000 55.6940000000000 55.5950000000000 55.5440000000000 55.4940000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4940000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4440000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.4940000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.6940000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000;55.4010000000000 55.4010000000000 55.3000000000000 55.3000000000000 55.3000000000000 55.3000000000000 55.3000000000000 55.3000000000000 55.3510000000000 55.5000000000000 55.6510000000000 55.7010000000000 55.6510000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.5500000000000 55.6010000000000 55.6010000000000 55.5500000000000 55.6510000000000 55.6010000000000 55.6010000000000 55.7010000000000 55.7500000000000 55.8510000000000 56 56.1010000000000 56.2500000000000 56.3000000000000 56.4510000000000 56.5500000000000 56.7010000000000 56.8510000000000 57 57.2010000000000 57.2500000000000 56.9510000000000 56.4510000000000 56.2500000000000 56.2500000000000 55.9510000000000 55.7500000000000 55.6010000000000 55.5000000000000 55.4010000000000 55.4010000000000 55.4010000000000 55.4010000000000 55.4510000000000 55.4510000000000 55.4510000000000 55.4510000000000 55.5000000000000 55.5000000000000 55.4510000000000 55.5000000000000 55.4510000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5500000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5500000000000 55.5500000000000 55.5500000000000 55.5500000000000 55.6010000000000 55.6010000000000 55.6510000000000 55.6010000000000 55.6010000000000 55.6510000000000 55.6010000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.7010000000000 55.7010000000000 55.7010000000000 55.7010000000000 55.7010000000000 55.7500000000000 55.7500000000000 55.7010000000000 55.7010000000000 55.7500000000000 55.7010000000000;55.3580000000000 55.2570000000000 55.3070000000000 55.2570000000000 55.2570000000000 55.2570000000000 55.2570000000000 55.2570000000000 55.2570000000000 55.3580000000000 55.4580000000000 55.6580000000000 55.6580000000000 55.6580000000000 55.6580000000000 55.7080000000000 55.6580000000000 55.6080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.6080000000000 55.7080000000000 55.8580000000000 56.1080000000000 56.2080000000000 56.3070000000000 56.4080000000000 56.5570000000000 56.7570000000000 56.8580000000000 57.0570000000000 57.2080000000000 57.3070000000000 57.0570000000000 56.5570000000000 56.4580000000000 56.3580000000000 56.1580000000000 55.8580000000000 55.6580000000000 55.4580000000000 55.4580000000000 55.4080000000000 55.4080000000000 55.4080000000000 55.4080000000000 55.4580000000000 55.4580000000000 55.5570000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.5070000000000 55.5070000000000 55.5070000000000 55.5070000000000 55.4580000000000 55.5070000000000 55.5070000000000 55.5070000000000 55.5070000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.5570000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6080000000000 55.6580000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.6580000000000 55.6580000000000 55.7080000000000 55.7570000000000 55.7570000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000;55.3140000000000 55.2640000000000 55.2640000000000 55.3140000000000 55.3140000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.2640000000000 55.3650000000000 55.4150000000000 55.5640000000000 55.5640000000000 55.6650000000000 55.6150000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.5640000000000 55.5640000000000 55.5140000000000 55.5640000000000 55.6150000000000 55.7150000000000 55.7150000000000 55.9650000000000 56.0640000000000 56.2150000000000 56.3140000000000 56.5140000000000 56.7640000000000 56.9150000000000 57.0640000000000 57.2150000000000 57.2150000000000 57.1650000000000 56.7640000000000 56.5640000000000 56.5140000000000 56.4150000000000 56.1650000000000 55.8650000000000 55.5140000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.6150000000000 55.5640000000000 55.6150000000000 55.5640000000000 55.6150000000000 55.5640000000000 55.6150000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6650000000000 55.6150000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.7150000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.7150000000000 55.7150000000000 55.7150000000000 55.7150000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7150000000000;55.3210000000000 55.3210000000000 55.2710000000000 55.2710000000000 55.2710000000000 55.2710000000000 55.2710000000000 55.3210000000000 55.3210000000000 55.3210000000000 55.4720000000000 55.5210000000000 55.5710000000000 55.6220000000000 55.6720000000000 55.5710000000000 55.5710000000000 55.5210000000000 55.5210000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.5210000000000 55.5710000000000 55.5710000000000 55.6720000000000 55.6720000000000 55.7710000000000 55.8210000000000 55.9720000000000 56.1720000000000 56.3720000000000 56.5710000000000 56.7710000000000 57.0210000000000 57.1720000000000 57.2220000000000 57.1720000000000 56.9220000000000 56.8210000000000 56.6720000000000 56.5710000000000 56.2710000000000 55.9720000000000 55.6220000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.4720000000000 55.4720000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.5710000000000 55.5210000000000 55.5210000000000 55.5210000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.5710000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6220000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.6720000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7710000000000 55.7710000000000 55.8210000000000 55.7710000000000 55.7710000000000 55.7710000000000 55.7710000000000;55.3790000000000 55.3280000000000 55.3280000000000 55.3790000000000 55.3280000000000 55.3280000000000 55.3280000000000 55.3790000000000 55.3280000000000 55.3790000000000 55.4290000000000 55.4290000000000 55.4790000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.5780000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.6790000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.9290000000000 56.0280000000000 56.1290000000000 56.2290000000000 56.5280000000000 56.8280000000000 57.0780000000000 57.1790000000000 57.1790000000000 57.0280000000000 56.9290000000000 56.8280000000000 56.6790000000000 56.4790000000000 56.0280000000000 55.7780000000000 55.6290000000000 55.5780000000000 55.5780000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5780000000000 55.5780000000000 55.5780000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7290000000000 55.7780000000000 55.7780000000000 55.8280000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000;55.3350000000000 55.3860000000000 55.3350000000000 55.3860000000000 55.3350000000000 55.3350000000000 55.3350000000000 55.3350000000000 55.3860000000000 55.3860000000000 55.3860000000000 55.3860000000000 55.3860000000000 55.4360000000000 55.5350000000000 55.5850000000000 55.6860000000000 55.5850000000000 55.5350000000000 55.5350000000000 55.5850000000000 55.6360000000000 55.6360000000000 55.6860000000000 55.6860000000000 55.7850000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.8860000000000 55.9860000000000 56.0850000000000 56.0850000000000 56.2850000000000 56.5350000000000 56.8860000000000 57.0350000000000 57.0850000000000 57.0350000000000 56.9860000000000 56.9860000000000 56.8860000000000 56.5350000000000 56.2360000000000 55.9360000000000 55.7850000000000 55.6360000000000 55.5850000000000 55.5850000000000 55.5350000000000 55.5350000000000 55.5350000000000 55.5350000000000 55.5850000000000 55.5850000000000 55.5850000000000 55.5850000000000 55.5350000000000 55.5850000000000 55.5850000000000 55.5850000000000 55.5850000000000 55.5850000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6360000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.6860000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7850000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7850000000000 55.7850000000000 55.7850000000000 55.7850000000000 55.7850000000000 55.7850000000000 55.8860000000000 55.8350000000000 55.8350000000000 55.8350000000000 55.8350000000000;55.4430000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3420000000000 55.3420000000000 55.3420000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.4430000000000 55.5420000000000 55.5920000000000 55.6430000000000 55.6430000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.6930000000000 55.7430000000000 55.6930000000000 55.8420000000000 55.8930000000000 55.8420000000000 55.7920000000000 55.9430000000000 56.1430000000000 56.1930000000000 55.9430000000000 56.0920000000000 56.2920000000000 56.6930000000000 56.7920000000000 56.9430000000000 56.9430000000000 57.1430000000000 57.1930000000000 57.0420000000000 56.7430000000000 56.4430000000000 56.0920000000000 55.8420000000000 55.6930000000000 55.5920000000000 55.5420000000000 55.5420000000000 55.5920000000000 55.5420000000000 55.5920000000000 55.5920000000000 55.5420000000000 55.5420000000000 55.5420000000000 55.6430000000000 55.5920000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.7430000000000 55.6930000000000 55.6930000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7920000000000 55.7430000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000;55.4500000000000 55.4500000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.4000000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.3490000000000 55.4000000000000 55.4000000000000 55.3490000000000 55.3490000000000 55.5000000000000 55.5990000000000 55.7500000000000 55.7000000000000 55.6500000000000 55.5990000000000 55.5990000000000 55.6500000000000 55.5990000000000 55.6500000000000 55.9500000000000 55.9000000000000 55.9000000000000 55.9500000000000 55.9500000000000 56.0990000000000 56.2500000000000 55.9000000000000 55.9000000000000 56.0490000000000 56.2990000000000 56.5490000000000 56.5990000000000 56.7990000000000 57 57.1500000000000 57 56.7990000000000 56.5990000000000 56.2990000000000 55.9000000000000 55.7000000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5990000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5990000000000 55.5990000000000 55.5990000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5490000000000 55.5990000000000 55.6500000000000 55.5990000000000 55.6500000000000 55.5990000000000 55.5990000000000 55.5990000000000 55.5990000000000 55.6500000000000 55.6500000000000 55.6500000000000 55.6500000000000 55.6500000000000 55.7000000000000 55.6500000000000 55.6500000000000 55.7000000000000 55.7000000000000 55.7000000000000 55.7500000000000 55.7000000000000 55.7000000000000 55.7000000000000 55.7000000000000 55.7000000000000 55.7500000000000 55.7500000000000 55.7000000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7990000000000 55.7990000000000 55.7990000000000 55.7990000000000 55.7990000000000 55.7990000000000;55.3560000000000 55.3560000000000 55.3560000000000 55.3060000000000 55.3060000000000 55.3060000000000 55.3560000000000 55.3560000000000 55.3060000000000 55.3060000000000 55.3060000000000 55.3060000000000 55.4070000000000 55.3560000000000 55.3560000000000 55.4070000000000 55.5560000000000 55.7560000000000 55.7560000000000 55.6060000000000 55.5560000000000 55.6060000000000 55.6570000000000 55.6060000000000 55.6570000000000 55.6570000000000 55.7070000000000 55.7070000000000 55.8060000000000 55.7560000000000 55.8560000000000 55.8560000000000 55.8060000000000 55.8060000000000 55.8560000000000 55.9570000000000 56.1060000000000 56.2560000000000 56.4070000000000 56.6060000000000 56.8560000000000 56.9070000000000 56.8060000000000 56.6570000000000 56.4070000000000 56.0560000000000 55.7070000000000 55.5560000000000 55.5060000000000 55.5060000000000 55.5060000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5060000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.6570000000000 55.6060000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.8060000000000 55.8060000000000 55.8560000000000 55.8560000000000 55.8060000000000 55.8060000000000 55.8060000000000;55.4120000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.3620000000000 55.4120000000000 55.4120000000000 55.4120000000000 55.4120000000000 55.5130000000000 55.8620000000000 55.8120000000000 55.6620000000000 55.6120000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.6620000000000 55.6620000000000 55.6120000000000 55.6120000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.7630000000000 55.8120000000000 55.9120000000000 56.1120000000000 56.2130000000000 56.3620000000000 56.6120000000000 56.8620000000000 56.8120000000000 56.7630000000000 56.4630000000000 56.1120000000000 55.8620000000000 55.6620000000000 55.6120000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.6120000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6120000000000 55.6620000000000 55.6620000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.6620000000000 55.6620000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000;55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.4180000000000 55.4180000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.3680000000000 55.4180000000000 55.4180000000000 55.4180000000000 55.7690000000000 55.8680000000000 55.7690000000000 55.6180000000000 55.7190000000000 55.7690000000000 55.7190000000000 55.6680000000000 55.6680000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.7190000000000 55.7690000000000 55.7690000000000 55.9690000000000 56.1680000000000 56.3680000000000 56.5190000000000 56.6680000000000 56.7690000000000 56.6180000000000 56.4180000000000 56.2690000000000 56.0690000000000 55.7690000000000 55.7190000000000 55.6680000000000 55.6180000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.6180000000000 55.5690000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7690000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.8190000000000 55.8190000000000 55.8680000000000 55.8680000000000 55.8680000000000;55.4240000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.3750000000000 55.4240000000000 55.6740000000000 55.6250000000000 55.6250000000000 55.7240000000000 55.7750000000000 55.7750000000000 55.7240000000000 55.6740000000000 55.6740000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6740000000000 55.6740000000000 55.6250000000000 55.7240000000000 55.7750000000000 55.8250000000000 55.8250000000000 56.0250000000000 56.1740000000000 56.3750000000000 56.4740000000000 56.5250000000000 56.4740000000000 56.3750000000000 56.2240000000000 56.0250000000000 55.8750000000000 55.7240000000000 55.7750000000000 55.7240000000000 55.6740000000000 55.6250000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.6740000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7750000000000 55.7750000000000 55.7750000000000 55.7750000000000 55.7750000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8750000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.9240000000000 55.9240000000000;55.5300000000000 55.4800000000000 55.4800000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.3810000000000 55.4300000000000 55.4800000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.4300000000000 55.3810000000000 55.4300000000000 55.4800000000000 55.4800000000000 55.5300000000000 55.5300000000000 55.6800000000000 55.6310000000000 55.7300000000000 55.7800000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7800000000000 55.8310000000000 55.9300000000000 56.0300000000000 56.1800000000000 56.3310000000000 56.3810000000000 56.3810000000000 56.3810000000000 56.2800000000000 56.1310000000000 55.9800000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7300000000000 55.5810000000000 55.5810000000000 55.6800000000000 55.6310000000000 55.6310000000000 55.6310000000000 55.6310000000000 55.6310000000000 55.6310000000000 55.6310000000000 55.6800000000000 55.6800000000000 55.6800000000000 55.6310000000000 55.6310000000000 55.6800000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.6800000000000 55.7300000000000 55.7300000000000 55.7300000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.9300000000000 55.9300000000000;55.4860000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4860000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4370000000000 55.4860000000000 55.4370000000000 55.4860000000000 55.4860000000000 55.4860000000000 55.5360000000000 55.5360000000000 55.5870000000000 56.2360000000000 55.7860000000000 55.7360000000000 55.7860000000000 55.7360000000000 55.8370000000000 55.7860000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.8370000000000 55.8370000000000 55.9370000000000 55.9860000000000 56.2360000000000 56.3370000000000 56.3370000000000 56.3370000000000 56.3370000000000 56.3370000000000 56.1870000000000 55.9860000000000 55.8370000000000 55.8370000000000 55.6870000000000 55.6370000000000 55.6370000000000 55.5870000000000 55.5870000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6870000000000 55.6870000000000 55.6370000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.7360000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.6870000000000 55.7860000000000 55.7860000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.8370000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.9370000000000;55.4430000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.4430000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.3930000000000 55.4430000000000 55.5920000000000 56.0420000000000 56.2430000000000 55.8930000000000 55.5420000000000 55.5920000000000 55.5920000000000 55.6930000000000 55.6930000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8930000000000 55.8930000000000 56.1930000000000 56.1930000000000 56.2920000000000 56.3930000000000 56.3420000000000 56.3420000000000 56.1430000000000 55.8930000000000 55.7430000000000 55.6430000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.6430000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.6930000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000;55.4990000000000 55.4490000000000 55.4490000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.3980000000000 55.4490000000000 55.4490000000000 55.4490000000000 55.5480000000000 56.0480000000000 56.3480000000000 55.8480000000000 55.4990000000000 55.4990000000000 55.5480000000000 55.5480000000000 55.6480000000000 55.6480000000000 55.5980000000000 55.5980000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.8480000000000 55.7490000000000 55.8480000000000 56.0480000000000 56.1990000000000 56.1990000000000 56.2490000000000 56.3980000000000 56.4990000000000 56.4490000000000 55.9490000000000 55.7490000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5480000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6990000000000 55.6990000000000 55.6480000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.7490000000000 55.7980000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7980000000000 55.7980000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.8480000000000 55.7980000000000 55.8480000000000 55.8980000000000;55.4550000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.3540000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.4040000000000 55.5550000000000 55.7050000000000 55.7550000000000 55.5550000000000 55.5050000000000 55.4550000000000 55.4550000000000 55.4550000000000 55.5550000000000 55.5050000000000 55.5050000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.6540000000000 55.7050000000000 55.8050000000000 55.8050000000000 55.7550000000000 55.7550000000000 55.8050000000000 55.8050000000000 55.8540000000000 55.9550000000000 56.0550000000000 56.0550000000000 56.1540000000000 56.3050000000000 56.5050000000000 56.4550000000000 56.2550000000000 55.8540000000000 55.6540000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6540000000000 55.6540000000000 55.6540000000000 55.6540000000000 55.6040000000000 55.6540000000000 55.6540000000000 55.6540000000000 55.6540000000000 55.7050000000000 55.6540000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7050000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.9550000000000;55.4600000000000 55.4100000000000 55.4600000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4100000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.4600000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.5110000000000 55.6110000000000 55.7610000000000 55.8110000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.8110000000000 55.8610000000000 55.9100000000000 55.9100000000000 56.0110000000000 56.0610000000000 56.0610000000000 56.2100000000000 56.3610000000000 56.3610000000000 56.2100000000000 55.9100000000000 55.8110000000000 55.7100000000000 55.6600000000000 55.6110000000000 55.6110000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.6110000000000 55.6110000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.7100000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.6600000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.8110000000000 55.8110000000000 55.8110000000000 55.8110000000000 55.8110000000000 55.8610000000000 55.9100000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.9100000000000 55.9100000000000 55.9100000000000;55.5160000000000 55.4660000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4660000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4160000000000 55.4660000000000 55.4660000000000 55.4660000000000 55.5160000000000 55.4660000000000 55.5160000000000 55.5160000000000 55.5160000000000 55.4660000000000 55.5160000000000 55.5160000000000 55.5160000000000 55.6660000000000 55.8170000000000 55.8670000000000 55.7660000000000 55.7660000000000 55.8670000000000 55.8670000000000 55.9160000000000 55.9160000000000 55.9160000000000 56.0670000000000 56.1170000000000 56.2160000000000 56.3670000000000 56.3170000000000 56.2160000000000 56.2160000000000 56.0670000000000 55.9160000000000 55.7160000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6170000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.7160000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.7160000000000 55.7160000000000 55.7160000000000 55.7160000000000 55.7160000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8670000000000 55.8670000000000 55.8670000000000 55.8670000000000 55.8670000000000 55.9660000000000 55.9160000000000 56.0160000000000;55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4230000000000 55.4720000000000 55.4720000000000 55.4230000000000 55.4230000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.5220000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.4720000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5220000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.5730000000000 55.5220000000000 55.5220000000000 55.6230000000000 55.8230000000000 55.8730000000000 55.8230000000000 55.8730000000000 55.9720000000000 55.9230000000000 55.9720000000000 56.0220000000000 55.9720000000000 56.0220000000000 56.0220000000000 56.1730000000000 56.4230000000000 56.4720000000000 56.2720000000000 56.2720000000000 56.2220000000000 56.0730000000000 55.9230000000000 55.8230000000000 55.8230000000000 55.7720000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.6730000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.8230000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.8230000000000 55.7720000000000 55.7720000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.9230000000000 55.9230000000000 55.9230000000000 55.9230000000000 55.9720000000000;55.5280000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4290000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4290000000000 55.4290000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.4790000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.4790000000000 55.5280000000000 55.5280000000000 55.4790000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5280000000000 55.5780000000000 55.5280000000000 55.5780000000000 55.6790000000000 55.7780000000000 55.9290000000000 55.9290000000000 55.9290000000000 55.9290000000000 56.0280000000000 56.0780000000000 55.8790000000000 55.7290000000000 55.8790000000000 56.0280000000000 56.3280000000000 56.4290000000000 56.3790000000000 56.2290000000000 56.2780000000000 56.2290000000000 56.1790000000000 56.0280000000000 55.9790000000000 55.9790000000000 55.9790000000000 55.8790000000000 55.7780000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.8280000000000 55.7780000000000 55.7780000000000 55.8280000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.9290000000000 55.8790000000000 55.9290000000000 55.9290000000000 55.9290000000000 55.9290000000000 55.9290000000000;55.5340000000000 55.4850000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4350000000000 55.4850000000000 55.5340000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.5340000000000 55.4850000000000 55.5340000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.4850000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5340000000000 55.5840000000000 55.6850000000000 55.8840000000000 55.9350000000000 55.8840000000000 55.9350000000000 56.0840000000000 55.9350000000000 55.6850000000000 55.6340000000000 55.6340000000000 55.7840000000000 56.0340000000000 56.1850000000000 56.1850000000000 56.1850000000000 56.1850000000000 56.2350000000000 56.1850000000000 55.9850000000000 55.8840000000000 55.8840000000000 55.9850000000000 55.9850000000000 55.9350000000000 55.8340000000000 55.7840000000000 55.7350000000000 55.7350000000000 55.7840000000000 55.7350000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.8340000000000 55.8340000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8840000000000 55.8840000000000;55.3900000000000 55.4410000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.3900000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4410000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.4910000000000 55.5410000000000 55.5410000000000 55.5900000000000 55.7410000000000 55.8400000000000 55.8400000000000 55.8900000000000 55.8400000000000 55.7910000000000 55.6400000000000 55.5900000000000 55.5410000000000 55.5900000000000 55.6400000000000 55.7910000000000 55.9410000000000 56.0900000000000 56.1910000000000 56.2410000000000 56.2410000000000 56.1400000000000 55.9410000000000 55.8400000000000 55.8900000000000 55.9410000000000 55.9410000000000 55.9410000000000 55.8400000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7410000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.7410000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.7910000000000 55.7410000000000 55.7410000000000 55.7910000000000 55.7910000000000 55.7410000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8900000000000 55.8900000000000 55.8900000000000 55.8900000000000 55.8900000000000;55.4970000000000 55.4460000000000 55.4460000000000 55.4970000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4460000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.4970000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5470000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.6460000000000 55.7470000000000 55.8960000000000 55.9460000000000 55.8960000000000 55.9460000000000 55.8960000000000 55.7470000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6960000000000 55.7470000000000 55.8960000000000 56.0970000000000 56.2470000000000 56.3470000000000 56.3470000000000 56.2470000000000 56.0970000000000 56.0470000000000 55.9970000000000 56.0470000000000 56.0470000000000 55.9970000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9970000000000 55.9460000000000 55.8470000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.9460000000000 55.9460000000000 55.8960000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000;55.5530000000000 55.5530000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5530000000000 55.5530000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5020000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.5530000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.7020000000000 55.9020000000000 55.9520000000000 55.9520000000000 56.0020000000000 56.0020000000000 55.7020000000000 55.6520000000000 55.6520000000000 55.7020000000000 55.7020000000000 55.7020000000000 55.8530000000000 56.0020000000000 56.2520000000000 56.3530000000000 56.3530000000000 56.3530000000000 56.2020000000000 56.1520000000000 56.0530000000000 56.0530000000000 56.0020000000000 56.0020000000000 55.9520000000000 55.9020000000000 55.9020000000000 55.9020000000000 56.0020000000000 55.9520000000000 55.8530000000000 55.8030000000000 55.8530000000000 55.8530000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8530000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.9020000000000 55.9020000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.9020000000000 55.9020000000000 55.9520000000000 55.9520000000000 55.9020000000000 55.9520000000000;55.5080000000000 55.5080000000000 55.4580000000000 55.5080000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.5080000000000 55.5080000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.4580000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5580000000000 55.5080000000000 55.5080000000000 55.5580000000000 55.5580000000000 55.5080000000000 55.5080000000000 55.5080000000000 55.5580000000000 55.5580000000000 55.6090000000000 55.7080000000000 55.8590000000000 55.9580000000000 55.9580000000000 55.9580000000000 55.9580000000000 55.6590000000000 55.6590000000000 55.6590000000000 55.7580000000000 55.8080000000000 55.9580000000000 56.0580000000000 56.1590000000000 56.2080000000000 56.2580000000000 56.3080000000000 56.4090000000000 56.3590000000000 56.2580000000000 56.2580000000000 56.2080000000000 56.1090000000000 56.0080000000000 55.9580000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.9090000000000 56.0080000000000 55.9580000000000 55.9090000000000 55.9090000000000 55.9090000000000 55.8590000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.8590000000000 55.9090000000000 55.8590000000000 55.8590000000000 55.9090000000000;55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4150000000000 55.4150000000000 55.4650000000000 55.4150000000000 55.4150000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.4650000000000 55.4650000000000 55.5140000000000 55.5640000000000 55.5640000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5140000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.5640000000000 55.7640000000000 55.9150000000000 55.9650000000000 55.9650000000000 55.9150000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.6650000000000 55.7640000000000 55.7640000000000 55.7640000000000 56.0140000000000 56.0640000000000 56.0640000000000 56.2150000000000 56.3650000000000 56.3650000000000 56.4650000000000 56.4150000000000 56.3140000000000 56.2640000000000 56.0140000000000 55.9650000000000 55.9150000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.9650000000000 55.9650000000000 55.9650000000000 55.9650000000000 55.9650000000000 55.9150000000000 55.8650000000000 55.8140000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.8140000000000 55.8650000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.8650000000000 55.9150000000000 55.9150000000000 55.9150000000000;55.4710000000000 55.4710000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4710000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4210000000000 55.4710000000000 55.4710000000000 55.5200000000000 55.4710000000000 55.4710000000000 55.4710000000000 55.5200000000000 55.4710000000000 55.4710000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5200000000000 55.5700000000000 55.6710000000000 55.9210000000000 55.9710000000000 55.9710000000000 55.9210000000000 55.7210000000000 55.6200000000000 55.6200000000000 55.6710000000000 55.7210000000000 55.7210000000000 55.8200000000000 55.9210000000000 55.9710000000000 55.9710000000000 56.1200000000000 56.2210000000000 56.4710000000000 56.6200000000000 56.5700000000000 56.4710000000000 56.3700000000000 56.1710000000000 56.0200000000000 55.9710000000000 55.9710000000000 55.8700000000000 55.8700000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 56.0200000000000 56.0700000000000 55.9210000000000 55.8700000000000 55.7700000000000 55.7700000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.7700000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8200000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000;55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.5270000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.5270000000000 55.4770000000000 55.4770000000000 55.4770000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5760000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5270000000000 55.5760000000000 55.5760000000000 55.6260000000000 55.6260000000000 55.5760000000000 55.6760000000000 55.9260000000000 55.9770000000000 55.9770000000000 55.9260000000000 55.6760000000000 55.6260000000000 55.6260000000000 55.6760000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8760000000000 55.9770000000000 55.9770000000000 56.0270000000000 56.1260000000000 56.3260000000000 56.5760000000000 56.6760000000000 56.6260000000000 56.4770000000000 56.3760000000000 56.2270000000000 56.1260000000000 56.0760000000000 55.9770000000000 55.9260000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.9770000000000 56.0270000000000 56.0760000000000 55.9770000000000 55.8760000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8760000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9770000000000 55.9770000000000 55.9770000000000 55.9260000000000 55.9770000000000 55.9770000000000;55.5330000000000 55.5330000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.5330000000000 55.5330000000000 55.4830000000000 55.4830000000000 55.4830000000000 55.5330000000000 55.5830000000000 55.5330000000000 55.5330000000000 55.5830000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5330000000000 55.5830000000000 55.6820000000000 55.6320000000000 55.5830000000000 55.5830000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6320000000000 55.6820000000000 55.6320000000000 55.6820000000000 55.6820000000000 55.6820000000000 55.6320000000000 55.6820000000000 55.7830000000000 55.9320000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.7830000000000 55.6820000000000 55.6820000000000 56.0330000000000 55.9830000000000 55.9320000000000 55.8820000000000 55.8820000000000 55.9830000000000 55.9830000000000 55.9320000000000 55.9830000000000 56.2330000000000 56.6820000000000 56.8330000000000 56.7830000000000 56.6820000000000 56.5330000000000 56.3820000000000 56.2830000000000 56.2330000000000 56.1820000000000 56.1820000000000 56.0830000000000 55.9830000000000 55.9320000000000 55.9320000000000 56.0330000000000 56.0330000000000 56.1820000000000 56.0330000000000 55.8820000000000 55.8330000000000 55.8820000000000 55.8330000000000 55.8330000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.9320000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000;55.5390000000000 55.5890000000000 55.5390000000000 55.5390000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.4880000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5390000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.5890000000000 55.6380000000000 55.6380000000000 55.7380000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8880000000000 55.8390000000000 55.7380000000000 55.6880000000000 55.7380000000000 55.8390000000000 55.9380000000000 55.8390000000000 55.8390000000000 55.9380000000000 55.9380000000000 55.8880000000000 55.8880000000000 56.0890000000000 56.5390000000000 56.8390000000000 56.8390000000000 56.7890000000000 56.6380000000000 56.4880000000000 56.3390000000000 56.2890000000000 56.3390000000000 56.2380000000000 56.1380000000000 55.9880000000000 55.9880000000000 55.9380000000000 55.9380000000000 56.0390000000000 56.1380000000000 56.0890000000000 55.8880000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.9880000000000 55.9380000000000;55.5440000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4440000000000 55.4940000000000 55.4440000000000 55.5440000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.4940000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5440000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.5950000000000 55.6450000000000 55.7440000000000 55.8450000000000 55.7940000000000 55.7940000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.7440000000000 55.7440000000000 55.7940000000000 55.8950000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 56.0440000000000 56.3450000000000 56.8450000000000 56.9940000000000 56.8450000000000 56.7440000000000 56.5440000000000 56.4940000000000 56.4440000000000 56.4440000000000 56.2440000000000 56.1940000000000 56.0950000000000 56.0950000000000 56.0440000000000 56.0440000000000 55.9940000000000 55.9940000000000 55.9940000000000 55.8950000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.7940000000000 55.7940000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8450000000000 55.8450000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.8950000000000 55.9440000000000 55.9440000000000 55.9940000000000 55.9440000000000 55.9940000000000;55.5500000000000 55.5500000000000 55.5500000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5500000000000 55.5500000000000 55.5500000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5000000000000 55.5500000000000 55.5500000000000 55.5500000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6010000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.7500000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 56 55.9010000000000 55.8510000000000 55.8510000000000 55.9510000000000 55.9010000000000 55.8510000000000 55.8510000000000 56.0500000000000 55.9510000000000 56 56.1010000000000 56.2010000000000 56.5000000000000 56.9010000000000 56.9010000000000 56.8000000000000 56.7500000000000 56.6010000000000 56.6510000000000 56.6510000000000 56.4010000000000 56.2500000000000 56.1010000000000 56.1010000000000 56.1010000000000 56.1010000000000 56.0500000000000 56.0500000000000 56.1010000000000 56 55.9010000000000 55.9010000000000 55.8510000000000 55.9010000000000 55.8510000000000 55.8510000000000 55.9010000000000 55.9010000000000 55.9510000000000 55.9510000000000 55.9510000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9510000000000 55.9510000000000 55.9510000000000 55.9510000000000 55.9510000000000 56 56 56 56;55.6060000000000 55.5060000000000 55.5060000000000 55.5560000000000 55.5560000000000 55.5060000000000 55.5060000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.5560000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.5560000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.6060000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6060000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.6570000000000 55.7070000000000 55.8060000000000 55.9070000000000 55.9070000000000 55.8560000000000 55.8560000000000 55.8060000000000 55.8560000000000 55.9070000000000 56.0060000000000 56.1060000000000 56.0560000000000 56.0560000000000 56.0560000000000 55.9070000000000 55.8560000000000 56.1570000000000 56.2070000000000 56.0560000000000 56.1570000000000 56.1060000000000 56.1060000000000 56.1570000000000 56.3060000000000 56.5560000000000 56.7070000000000 56.7070000000000 56.6060000000000 56.5560000000000 56.6060000000000 56.5060000000000 56.3560000000000 56.2070000000000 56.0560000000000 56.1060000000000 56.1570000000000 56.2070000000000 56.0560000000000 56.1060000000000 56.1060000000000 56.0060000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9070000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 55.9570000000000 56.0060000000000 56.0060000000000 56.0060000000000 56.0060000000000;55.5620000000000 55.5620000000000 55.5620000000000 55.6120000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.5620000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6120000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.7630000000000 55.8120000000000 55.9120000000000 55.8620000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.9120000000000 55.9630000000000 56.0130000000000 56.1120000000000 56.2130000000000 56.3120000000000 56.2130000000000 56.0130000000000 55.9630000000000 55.9630000000000 56.1120000000000 56.1120000000000 56.1620000000000 56.1120000000000 56.0620000000000 56.1120000000000 56.1620000000000 56.3120000000000 56.3120000000000 56.5130000000000 56.5130000000000 56.5130000000000 56.5130000000000 56.5130000000000 56.5130000000000 56.4120000000000 56.2130000000000 56.1120000000000 56.1120000000000 56.2130000000000 56.2130000000000 56.1620000000000 56.1120000000000 56.0620000000000 56.0130000000000 55.9630000000000 55.9120000000000 55.9120000000000 55.9120000000000 55.9120000000000 55.9120000000000 55.9630000000000 56.0130000000000 55.9630000000000 55.9630000000000 55.9630000000000 55.9630000000000 55.9630000000000 55.9630000000000 55.9630000000000 56.0130000000000 55.9630000000000 55.9630000000000 55.9630000000000 56.0130000000000 56.1120000000000 56.0620000000000 56.0620000000000;55.6180000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.6180000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.5690000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6680000000000 55.6180000000000 55.6180000000000 55.6180000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.7190000000000 55.6680000000000 55.7190000000000 55.7690000000000 55.8680000000000 55.8190000000000 55.8190000000000 55.9180000000000 55.8680000000000 55.8190000000000 55.8680000000000 55.9180000000000 55.9690000000000 56.1180000000000 56.1180000000000 56.2690000000000 56.1680000000000 56.0190000000000 55.9690000000000 55.9690000000000 56.0190000000000 56.0690000000000 56.1180000000000 56.0690000000000 56.0190000000000 56.0190000000000 56.0190000000000 55.9690000000000 56.0190000000000 56.0190000000000 56.2690000000000 56.4180000000000 56.5190000000000 56.5190000000000 56.5690000000000 56.5190000000000 56.4690000000000 56.0190000000000 56.0690000000000 56.1680000000000 56.1680000000000 56.1680000000000 56.1180000000000 56.0190000000000 55.9690000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 56.0190000000000 56.0190000000000 56.0190000000000;55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5250000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.6250000000000 55.5750000000000 55.5750000000000 55.6250000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.5750000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6250000000000 55.6740000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8750000000000 55.8750000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.9240000000000 55.9240000000000 55.9740000000000 56.0250000000000 56.0750000000000 55.9740000000000 55.9240000000000 55.8750000000000 55.9240000000000 56.0250000000000 55.9740000000000 55.9240000000000 55.9240000000000 56.0750000000000 55.9740000000000 55.9240000000000 55.8250000000000 55.7750000000000 55.8250000000000 56.0750000000000 56.4240000000000 56.5250000000000 56.5250000000000 56.5250000000000 56.4240000000000 56.1250000000000 55.9740000000000 56.0250000000000 56.1250000000000 56.1740000000000 56.0750000000000 56.0250000000000 56.0250000000000 55.9740000000000 55.9740000000000 55.9240000000000 55.9240000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.9240000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.9740000000000 55.9240000000000 55.9240000000000 55.9740000000000 55.9740000000000 55.9740000000000 55.9740000000000 56.0250000000000;55.5810000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.4800000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5810000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5300000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.5810000000000 55.6800000000000 55.7300000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.8810000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.9300000000000 55.8810000000000 55.8810000000000 55.9300000000000 55.9800000000000 55.9800000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7300000000000 55.7800000000000 55.8310000000000 56.2800000000000 56.4300000000000 56.4800000000000 56.4800000000000 56.4300000000000 56.2300000000000 56.0300000000000 56.0300000000000 56.0810000000000 56.1800000000000 56.1800000000000 56.0810000000000 56.0300000000000 56.0300000000000 55.9800000000000 55.9300000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.9800000000000 55.9300000000000 55.9800000000000 55.9300000000000 55.9300000000000 55.9800000000000 55.9800000000000 55.9800000000000 55.9800000000000 55.9300000000000 55.9800000000000 55.9800000000000 56.0300000000000;55.5870000000000 55.5360000000000 55.5360000000000 55.5360000000000 55.5360000000000 55.5870000000000 55.5870000000000 55.5360000000000 55.5360000000000 55.5870000000000 55.5360000000000 55.5360000000000 55.5360000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.5870000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6370000000000 55.6870000000000 55.7860000000000 55.8370000000000 55.9370000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.9860000000000 56.0360000000000 56.0360000000000 56.0360000000000 55.8870000000000 55.8370000000000 55.7860000000000 55.8370000000000 55.7860000000000 55.7860000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 56.3870000000000 56.4860000000000 56.4860000000000 56.4370000000000 56.4370000000000 56.2860000000000 56.0870000000000 56.0360000000000 56.0870000000000 56.1870000000000 56.2860000000000 56.1370000000000 56.0360000000000 55.9860000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.8870000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9860000000000 55.9860000000000 55.9860000000000 55.9370000000000 55.9860000000000 56.0360000000000 56.0360000000000 55.9860000000000 56.0360000000000 56.0360000000000 56.0360000000000;55.6430000000000 55.5920000000000 55.5920000000000 55.5420000000000 55.5420000000000 55.5420000000000 55.5420000000000 55.5420000000000 55.5420000000000 55.5920000000000 55.5420000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.5920000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6430000000000 55.6930000000000 55.7920000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8420000000000 55.8930000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8930000000000 55.9930000000000 56.0420000000000 55.9430000000000 55.8420000000000 55.7920000000000 55.7920000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.8420000000000 55.9430000000000 56.3420000000000 56.4430000000000 56.4430000000000 56.4430000000000 56.4430000000000 56.2430000000000 56.0420000000000 56.0420000000000 56.0420000000000 56.3420000000000 56.4930000000000 56.0420000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.8930000000000 55.8930000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9930000000000 55.9430000000000 55.9430000000000 55.9930000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9930000000000 55.9930000000000 55.9930000000000 55.9930000000000 55.9930000000000;55.6480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5980000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5480000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5480000000000 55.5480000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.5980000000000 55.6480000000000 55.5980000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.6480000000000 55.7490000000000 55.7980000000000 55.9990000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8480000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8480000000000 55.7980000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7490000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 56.2490000000000 56.4490000000000 56.4490000000000 56.3980000000000 56.3480000000000 56.1480000000000 55.9990000000000 56.0480000000000 56.1480000000000 56.2980000000000 56.3980000000000 56.0980000000000 55.9490000000000 55.9490000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9990000000000 55.9990000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9990000000000 55.9990000000000 55.9990000000000 55.9990000000000 55.9990000000000;55.6040000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5050000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.5550000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.6040000000000 55.7050000000000 55.9040000000000 56.0550000000000 56.0050000000000 56.0050000000000 56.0050000000000 55.9550000000000 55.9550000000000 55.9040000000000 55.9040000000000 55.9550000000000 55.9040000000000 55.8540000000000 55.8540000000000 55.8050000000000 55.8050000000000 55.7550000000000 55.8050000000000 55.8050000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8540000000000 55.9550000000000 56.4040000000000 56.4040000000000 56.3540000000000 56.2050000000000 56.0050000000000 56.0050000000000 56.0550000000000 56.1540000000000 56.1540000000000 56.2550000000000 56.1040000000000 55.9040000000000 55.8540000000000 55.8540000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 56.0050000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 56.0050000000000 56.0550000000000;55.6600000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5110000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5110000000000 55.5110000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.5610000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.5610000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6110000000000 55.6600000000000 55.6600000000000 55.6110000000000 55.6600000000000 55.7100000000000 55.9600000000000 56.0110000000000 55.9600000000000 56.0110000000000 56.2100000000000 55.9600000000000 55.8110000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7100000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.8110000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.7610000000000 55.8110000000000 56.1600000000000 56.4100000000000 56.3610000000000 56.1600000000000 56.0110000000000 55.9600000000000 56.0110000000000 56.0110000000000 56.1110000000000 56.1110000000000 56.0110000000000 55.9600000000000 55.8610000000000 55.8610000000000 55.9100000000000 55.8610000000000 55.8610000000000 55.9600000000000 55.9100000000000 55.9600000000000 55.9100000000000 55.9100000000000 55.9600000000000 56.0110000000000 56.0110000000000 56.0110000000000 55.9600000000000 55.9600000000000 55.9600000000000 55.9600000000000 55.9600000000000 56.0110000000000 56.0110000000000;55.6170000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.6170000000000 55.6170000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.5670000000000 55.6170000000000 55.6660000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6170000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.6660000000000 55.7160000000000 55.7160000000000 55.7160000000000 55.8170000000000 55.8670000000000 55.8670000000000 55.9160000000000 55.8670000000000 55.8170000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.7660000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8170000000000 55.8670000000000 55.8170000000000 55.8170000000000 55.8670000000000 55.8670000000000 55.8670000000000 55.8670000000000 55.9160000000000 56.4160000000000 56.4660000000000 56.3170000000000 56.1170000000000 56.0160000000000 56.0160000000000 56.0160000000000 56.1170000000000 56.1660000000000 56.1170000000000 56.0670000000000 55.9660000000000 55.9660000000000 55.9660000000000 55.9660000000000 55.9660000000000 55.9660000000000 55.9660000000000 56.0160000000000 56.0160000000000 56.0160000000000 56.0160000000000 56.0160000000000 56.0670000000000 56.0670000000000 56.0670000000000 56.0670000000000 56.0670000000000 56.0670000000000 56.0670000000000 56.1660000000000 56.1170000000000;55.7220000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6230000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6230000000000 55.6730000000000 55.6230000000000 55.6230000000000 55.6230000000000 55.6230000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.7220000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.6730000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7220000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.7720000000000 55.8230000000000 55.8230000000000 55.8230000000000 55.7720000000000 55.7720000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8230000000000 55.8230000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.8730000000000 55.9230000000000 56.3230000000000 56.5220000000000 56.4720000000000 56.3230000000000 56.0730000000000 56.0730000000000 56.0730000000000 56.0730000000000 56.1230000000000 56.1230000000000 56.0730000000000 56.0220000000000 55.9720000000000 55.9720000000000 55.9720000000000 55.9720000000000 55.9720000000000 55.9720000000000 55.9720000000000 56.0220000000000 56.0220000000000 56.0730000000000 56.0730000000000 56.0730000000000 56.0730000000000 56.1230000000000 56.0730000000000 56.1230000000000 56.1230000000000 56.1230000000000 56.1230000000000 56.0730000000000;55.6790000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6290000000000 55.6290000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6290000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.6790000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7290000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.7780000000000 55.8280000000000 55.7780000000000 55.7780000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8280000000000 55.8790000000000 55.8790000000000 55.8280000000000 55.8790000000000 55.8280000000000 55.8280000000000 55.8790000000000 55.8790000000000 55.8790000000000 55.8790000000000 55.8280000000000 55.8790000000000 55.8790000000000 55.8790000000000 55.8790000000000 55.9290000000000 55.8790000000000 55.9290000000000 56.0780000000000 56.4790000000000 56.5280000000000 56.7780000000000 56.2290000000000 56.1290000000000 56.0780000000000 56.1290000000000 56.1290000000000 56.1290000000000 56.0780000000000 56.0780000000000 56.0280000000000 55.9790000000000 56.0280000000000 56.0280000000000 56.0780000000000 56.0280000000000 56.0280000000000 56.0280000000000 56.0280000000000 56.0280000000000 56.0280000000000 56.0780000000000 56.0780000000000 56.0780000000000 56.0780000000000 56.1290000000000 56.1290000000000 56.0780000000000 56.0780000000000 56.1290000000000;55.7350000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6850000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6340000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.7350000000000 55.6850000000000 55.7350000000000 55.7350000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.6850000000000 55.7840000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7350000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.8340000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.7840000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.8340000000000 55.9850000000000 56.3340000000000 56.6850000000000 56.8840000000000 56.3840000000000 56.1850000000000 56.1340000000000 56.1340000000000 56.0840000000000 56.1340000000000 56.0840000000000 56.0340000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 56.0340000000000 56.0340000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 55.9850000000000 56.0340000000000 56.0340000000000 56.0340000000000 56.0340000000000 56.0340000000000;55.6910000000000 55.6400000000000 55.6400000000000 55.5900000000000 55.6400000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.5900000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.5900000000000 55.5900000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6910000000000 55.6910000000000 55.6400000000000 55.6400000000000 55.6400000000000 55.6910000000000 55.6910000000000 55.6400000000000 55.6400000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.6910000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7410000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.7910000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8900000000000 55.8900000000000 55.9410000000000 56.0410000000000 56.2410000000000 56.5410000000000 56.5900000000000 56.4910000000000 56.2910000000000 56.1400000000000 56.1400000000000 56.0900000000000 56.0900000000000 56.0410000000000 56.0410000000000 56.0410000000000 55.9910000000000 55.9410000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 55.9910000000000 56.0410000000000 56.0410000000000 56.0410000000000 56.0410000000000 56.0900000000000 56.0900000000000 56.0900000000000 56.0410000000000;55.7470000000000 55.6460000000000 55.6460000000000 55.5970000000000 55.6460000000000 55.5970000000000 55.5970000000000 55.5970000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6460000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.6960000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.6960000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7970000000000 55.7970000000000 55.7470000000000 55.7970000000000 55.7470000000000 55.7470000000000 55.7970000000000 55.7470000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8470000000000 55.8960000000000 55.9460000000000 56.0470000000000 56.1460000000000 56.4460000000000 56.5970000000000 56.5970000000000 56.4970000000000 56.2970000000000 56.1460000000000 56.0970000000000 56.0970000000000 56.0470000000000 56.0970000000000 56.0970000000000 56.0970000000000 56.0970000000000 56.0470000000000 56.0470000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0970000000000 56.0970000000000 56.0970000000000 56.0970000000000;55.6030000000000 55.6520000000000 55.6030000000000 55.6030000000000 55.6520000000000 55.6520000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6030000000000 55.6520000000000 55.6030000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.7020000000000 55.7520000000000 55.7020000000000 55.7020000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.6520000000000 55.7020000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.7520000000000 55.8030000000000 55.8030000000000 55.7520000000000 55.8030000000000 55.8030000000000 55.8030000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8530000000000 55.8030000000000 55.8530000000000 55.8530000000000 55.9020000000000 55.9020000000000 56.0530000000000 56.1030000000000 56.3030000000000 56.5530000000000 56.6030000000000 56.5530000000000 56.4020000000000 56.1520000000000 56.1030000000000 56.0020000000000 56.0020000000000 56.0530000000000 56.1030000000000 56.0530000000000 56.0530000000000 56.0530000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0020000000000 56.0530000000000 56.0530000000000 56.0530000000000 56.0530000000000 56.0530000000000 56.0530000000000 56.0530000000000;55.7080000000000 55.6590000000000 55.6590000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6590000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6090000000000 55.6590000000000 55.6090000000000 55.6090000000000 55.6590000000000 55.6090000000000 55.6090000000000 55.6590000000000 55.6590000000000 55.6590000000000 55.6590000000000 55.6590000000000 55.7080000000000 55.6590000000000 55.6590000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.6590000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7080000000000 55.7580000000000 55.7580000000000 55.7080000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.7580000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.8080000000000 55.9090000000000 55.8590000000000 55.8590000000000 55.9090000000000 55.9090000000000 55.9090000000000 55.9090000000000 55.9090000000000 56.0080000000000 56.0580000000000 56.1090000000000 56.2080000000000 56.4580000000000 56.5580000000000 56.6090000000000 56.5580000000000 56.5080000000000 56.2080000000000 56.1090000000000 56.0580000000000 56.0580000000000 56.0580000000000 56.1090000000000 56.1090000000000 56.0580000000000 56.0580000000000 56.0580000000000 56.0080000000000 56.0080000000000 56.0080000000000 56.0080000000000 56.0080000000000 56.0580000000000 56.0580000000000 56.0580000000000 56.0580000000000 56.0580000000000 56.1090000000000 56.0580000000000 56.1090000000000 56.1090000000000;55.7150000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6150000000000 55.6650000000000 55.7150000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.6650000000000 55.7640000000000 55.7150000000000 55.7150000000000 55.7150000000000 55.7150000000000 55.7640000000000 55.7150000000000 55.7640000000000 55.7150000000000 55.7150000000000 55.7150000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.7640000000000 55.8140000000000 55.8140000000000 55.7640000000000 55.7640000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.7640000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8140000000000 55.8650000000000 55.8650000000000 55.9150000000000 55.8650000000000 55.9150000000000 55.9150000000000 55.9150000000000 55.9150000000000 56.0140000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.1150000000000 56.2640000000000 56.4150000000000 56.5640000000000 56.6150000000000 56.6150000000000 56.5640000000000 56.3650000000000 56.2150000000000 56.1650000000000 56.1150000000000 56.1150000000000 56.0640000000000 56.0640000000000 56.0140000000000 56.0140000000000 56.0140000000000 56.0140000000000 56.0140000000000 56.0140000000000 56.0140000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.0640000000000 56.1150000000000 56.1150000000000;55.7210000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6200000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.6710000000000 55.7210000000000 55.7210000000000 55.7210000000000 55.7210000000000 55.7210000000000 55.7210000000000 55.6710000000000 55.7210000000000 55.7210000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.7700000000000 55.8200000000000 55.8200000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.8700000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 55.9210000000000 56.0200000000000 56.0700000000000 56.1710000000000 56.1200000000000 56.1710000000000 56.1710000000000 56.2700000000000 56.3700000000000 56.4710000000000 56.6200000000000 56.7210000000000 56.7210000000000 56.6710000000000 56.5200000000000 56.3200000000000 56.2210000000000 56.1710000000000 56.1200000000000 56.0700000000000 56.0700000000000 56.1200000000000 56.1200000000000 56.1200000000000 56.0700000000000 56.1200000000000 56.1200000000000 56.1200000000000 56.1200000000000 56.1200000000000 56.1710000000000 56.1710000000000 56.1710000000000 56.1710000000000 56.2210000000000 56.2210000000000;55.7270000000000 55.7270000000000 55.6760000000000 55.6760000000000 55.6760000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.7270000000000 55.8260000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.7770000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8260000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.8760000000000 55.9770000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9260000000000 55.9770000000000 55.9770000000000 55.9770000000000 55.9770000000000 55.9770000000000 55.9770000000000 55.9770000000000 56.0760000000000 56.0760000000000 56.1260000000000 56.1260000000000 56.1760000000000 56.1760000000000 56.1760000000000 56.2270000000000 56.3760000000000 56.5760000000000 56.6760000000000 56.7770000000000 56.7770000000000 56.7270000000000 56.6260000000000 56.3260000000000 56.1760000000000 56.0760000000000 56.0760000000000 56.0760000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1260000000000 56.1760000000000 56.1760000000000 56.1760000000000 56.1760000000000 56.1760000000000 56.1760000000000 56.1760000000000;55.8330000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.8330000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.8330000000000 55.7830000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8330000000000 55.8820000000000 55.8820000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8820000000000 55.9320000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9830000000000 55.9320000000000 55.9830000000000 55.9830000000000 55.9320000000000 55.9830000000000 56.0330000000000 56.0830000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.2830000000000 56.4320000000000 56.5830000000000 56.7330000000000 56.7330000000000 56.7330000000000 56.5830000000000 56.3820000000000 56.1320000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.0830000000000 56.1320000000000 56.1320000000000 56.1320000000000 56.1320000000000 56.0830000000000 56.1320000000000 56.1320000000000 56.1320000000000 56.1320000000000 56.1820000000000 56.1820000000000;55.7380000000000 55.7890000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.7890000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.6880000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7890000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7380000000000 55.7890000000000 55.7380000000000 55.7380000000000 55.7890000000000 55.7890000000000 55.7890000000000 55.8390000000000 55.7890000000000 55.8880000000000 55.8880000000000 55.7890000000000 55.7890000000000 55.7890000000000 55.7890000000000 55.7890000000000 55.8390000000000 55.7890000000000 55.7890000000000 55.7890000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8390000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.8880000000000 55.9380000000000 55.8880000000000 55.9380000000000 55.9880000000000 55.9380000000000 55.9380000000000 55.9380000000000 55.8880000000000 55.9380000000000 55.9380000000000 55.9380000000000 56.0390000000000 56.1380000000000 56.1380000000000 56.1380000000000 56.1380000000000 56.0890000000000 56.0890000000000 56.1880000000000 56.3390000000000 56.5390000000000 56.6880000000000 56.6380000000000 56.6380000000000 56.5890000000000 56.4380000000000 56.1380000000000 56.0890000000000 56.0390000000000 56.0390000000000 56.0890000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0390000000000 56.0890000000000 56.0890000000000 56.0890000000000 56.0890000000000 56.0890000000000 56.0890000000000;55.8450000000000 55.8450000000000 55.8950000000000 55.8950000000000 55.8450000000000 55.7940000000000 55.7440000000000 55.6940000000000 55.6940000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6450000000000 55.6940000000000 55.7440000000000 55.6940000000000 55.6940000000000 55.6940000000000 55.6940000000000 55.6940000000000 55.6940000000000 55.6940000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.6940000000000 55.7940000000000 55.7440000000000 55.7440000000000 55.7940000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7440000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.7940000000000 55.8450000000000 55.8450000000000 55.8950000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.8450000000000 55.9440000000000 55.9440000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.1940000000000 56.5440000000000 56.5440000000000 56.5440000000000 56.5440000000000 56.5440000000000 56.5440000000000 56.3450000000000 56.0950000000000 55.9940000000000 55.9940000000000 55.9940000000000 56.0440000000000 55.9940000000000 55.9940000000000 55.9940000000000 56.0440000000000 56.0440000000000 55.9940000000000 56.0440000000000 56.0950000000000 56.0950000000000 56.0950000000000 56.0440000000000 56.0440000000000 56.0950000000000;55.8000000000000 55.8000000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.7500000000000 55.7010000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6010000000000 55.6510000000000 55.6010000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.6510000000000 55.7500000000000 55.7500000000000 55.7010000000000 55.7010000000000 55.7010000000000 55.7500000000000 55.7010000000000 55.7010000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7010000000000 55.7010000000000 55.7500000000000 55.7500000000000 55.8000000000000 55.8000000000000 55.8000000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.8000000000000 55.7500000000000 55.7500000000000 55.7500000000000 55.8000000000000 55.8000000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.8510000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9010000000000 55.9510000000000 56.1010000000000 56.2010000000000 56.0500000000000 56.0500000000000 56.0500000000000 56.0500000000000 56.1010000000000 56.1510000000000 56.2500000000000 56.4010000000000 56.5000000000000 56.5500000000000 56.6510000000000 56.6510000000000 56.6010000000000 56.3000000000000 56.1010000000000 56.0500000000000 56.1010000000000 56.1510000000000 56.1510000000000 56.1510000000000 56.1510000000000 56.1510000000000 56.2010000000000 56.2500000000000 56.2500000000000 56.2500000000000 56.2500000000000 56.2500000000000 56.2010000000000 56.1510000000000 56.1510000000000;55.7560000000000 55.8060000000000 55.8060000000000 55.8560000000000 55.8560000000000 55.8060000000000 55.8060000000000 55.7560000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7560000000000 55.7560000000000 55.7070000000000 55.7070000000000 55.7560000000000 55.7560000000000 55.8060000000000 55.8060000000000 55.7560000000000 55.7560000000000 55.7070000000000 55.7070000000000 55.7070000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.7560000000000 55.8060000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8060000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.8560000000000 55.9070000000000 55.9070000000000 55.9570000000000 55.9070000000000 55.9070000000000 55.9570000000000 55.9570000000000 55.9070000000000 55.9570000000000 55.9570000000000 55.9570000000000 56.1060000000000 56.2070000000000 56.2070000000000 56.1570000000000 56.1060000000000 56.1060000000000 56.1570000000000 56.1060000000000 56.1570000000000 56.1570000000000 56.1570000000000 56.2560000000000 56.4570000000000 56.6060000000000 56.7070000000000 56.6570000000000 56.4570000000000 56.2560000000000 56.1570000000000 56.1570000000000 56.2560000000000 56.2560000000000 56.2560000000000 56.2560000000000 56.3060000000000 56.3060000000000 56.3060000000000 56.2560000000000 56.2560000000000 56.2560000000000 56.2070000000000 56.3060000000000 56.2560000000000 56.1570000000000;55.7130000000000 55.6620000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7630000000000 55.7630000000000 55.7130000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.6620000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7130000000000 55.7630000000000 55.7630000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8120000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.8120000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.7630000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8620000000000 55.8620000000000 56.0130000000000 56.1120000000000 56.1620000000000 56.1120000000000 56.1120000000000 56.1120000000000 56.0620000000000 56.0620000000000 56.0620000000000 56.0620000000000 56.1120000000000 56.1120000000000 56.2630000000000 56.5130000000000 56.6620000000000 56.6620000000000 56.5620000000000 56.3620000000000 56.2630000000000 56.1620000000000 56.2130000000000 56.2130000000000 56.2130000000000 56.1620000000000 56.1620000000000 56.2630000000000 56.2130000000000 56.2130000000000 56.1620000000000 56.2130000000000 56.2130000000000 56.2630000000000 56.2630000000000 56.2130000000000;55.6680000000000 55.6180000000000 55.6180000000000 55.5690000000000 55.6180000000000 55.6180000000000 55.6680000000000 55.7190000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.6680000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.6680000000000 55.7690000000000 55.8190000000000 55.8680000000000 55.8680000000000 55.8190000000000 55.7690000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7690000000000 55.7690000000000 55.7190000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8680000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.9180000000000 56.0190000000000 56.0190000000000 56.0190000000000 56.0190000000000 56.0190000000000 56.0190000000000 56.0690000000000 56.0690000000000 56.0690000000000 56.0690000000000 56.1180000000000 56.2690000000000 56.4690000000000 56.6180000000000 56.7190000000000 56.6680000000000 56.4690000000000 56.3190000000000 56.2190000000000 56.2190000000000 56.2190000000000 56.2690000000000 56.2690000000000 56.2190000000000 56.2190000000000 56.2690000000000 56.2190000000000 56.1680000000000 56.1680000000000 56.2190000000000 56.2690000000000 56.2690000000000 56.2190000000000;55.7240000000000 55.6250000000000 55.6250000000000 55.6740000000000 55.6250000000000 55.6250000000000 55.6740000000000 55.6740000000000 55.7240000000000 55.7240000000000 55.6740000000000 55.6740000000000 55.6740000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.6740000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7240000000000 55.7750000000000 55.8250000000000 55.9240000000000 55.9240000000000 55.8750000000000 55.8750000000000 55.7750000000000 55.7750000000000 55.7240000000000 55.7750000000000 55.8250000000000 55.7750000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8250000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.9740000000000 55.9240000000000 55.9240000000000 55.9240000000000 55.9240000000000 55.9240000000000 55.9740000000000 55.9740000000000 55.9740000000000 56.0250000000000 56.0250000000000 56.1250000000000 56.1250000000000 56.1250000000000 56.1250000000000 56.1250000000000 56.2240000000000 56.1740000000000 56.1250000000000 56.2240000000000 56.4240000000000 56.6740000000000 56.7750000000000 56.7750000000000 56.6250000000000 56.4240000000000 56.2750000000000 56.1740000000000 56.2750000000000 56.2750000000000 56.2750000000000 56.2240000000000 56.3250000000000 56.4240000000000 56.3750000000000 56.2750000000000 56.3250000000000 56.2750000000000 56.2750000000000 56.2750000000000 56.2240000000000;55.7800000000000 55.7300000000000 55.6800000000000 55.6800000000000 55.6800000000000 55.6800000000000 55.6800000000000 55.7300000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.7800000000000 55.8310000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7300000000000 55.7300000000000 55.7800000000000 55.8310000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7300000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.7800000000000 55.8310000000000 55.9300000000000 55.9800000000000 55.9800000000000 55.9300000000000 55.8810000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8310000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.8810000000000 55.9800000000000 55.9300000000000 55.9300000000000 55.9300000000000 55.9300000000000 55.9300000000000 55.9300000000000 55.9800000000000 55.9800000000000 55.9800000000000 55.9800000000000 55.9800000000000 56.0300000000000 56.0810000000000 56.1800000000000 56.1800000000000 56.2300000000000 56.2800000000000 56.2800000000000 56.2300000000000 56.1800000000000 56.1800000000000 56.3310000000000 56.6310000000000 56.7800000000000 56.8310000000000 56.7300000000000 56.5300000000000 56.3310000000000 56.1800000000000 56.1800000000000 56.2300000000000 56.2800000000000 56.2800000000000 56.3810000000000 56.4800000000000 56.4800000000000 56.4300000000000 56.2800000000000 56.2800000000000 56.2800000000000 56.2800000000000 56.2800000000000;55.7360000000000 55.6870000000000 55.7360000000000 55.7360000000000 55.6870000000000 55.6870000000000 55.7360000000000 55.7360000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.7860000000000 55.7860000000000 55.7360000000000 55.7360000000000 55.7360000000000 55.7860000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.8370000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.7860000000000 55.8870000000000 55.9860000000000 56.0870000000000 55.9860000000000 55.9370000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8370000000000 55.8370000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.8870000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9370000000000 55.9860000000000 55.9370000000000 55.9860000000000 55.9860000000000 55.9860000000000 55.9860000000000 55.9860000000000 55.9860000000000 56.0360000000000 56.0870000000000 56.0870000000000 56.0870000000000 56.1870000000000 56.2360000000000 56.2360000000000 56.2360000000000 56.2360000000000 56.2360000000000 56.2360000000000 56.3870000000000 56.6370000000000 56.7860000000000 56.7860000000000 56.8370000000000 56.6870000000000 56.4860000000000 56.2860000000000 56.2360000000000 56.2360000000000 56.3370000000000 56.3370000000000 56.4370000000000 56.5360000000000 56.5360000000000 56.4860000000000 56.4370000000000 56.2860000000000 56.2860000000000 56.2360000000000 56.2360000000000;55.7920000000000 55.7430000000000 55.7920000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8930000000000 55.8420000000000 55.8420000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7430000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.8420000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8930000000000 55.9430000000000 55.9430000000000 55.8930000000000 55.8420000000000 55.8420000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.7920000000000 55.8420000000000 55.7920000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.8420000000000 55.9430000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.8930000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9430000000000 55.9930000000000 56.0420000000000 56.0420000000000 56.1430000000000 56.1430000000000 56.1430000000000 56.0920000000000 56.0920000000000 56.1430000000000 56.1930000000000 56.2920000000000 56.4430000000000 56.6430000000000 56.6930000000000 56.7920000000000 56.7920000000000 56.5920000000000 56.3930000000000 56.1930000000000 56.1930000000000 56.3420000000000 56.6430000000000 56.6430000000000 56.5920000000000 56.5920000000000 56.7920000000000 56.6930000000000 56.4930000000000 56.3930000000000 56.3930000000000 56.3420000000000;55.6990000000000 55.6990000000000 55.6480000000000 55.6990000000000 55.6480000000000 55.6480000000000 55.6990000000000 55.7490000000000 55.7490000000000 55.7980000000000 55.7980000000000 55.7490000000000 55.7490000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6990000000000 55.6480000000000 55.6480000000000 55.7980000000000 55.8480000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.8480000000000 55.8480000000000 55.7980000000000 55.7490000000000 55.7980000000000 55.8480000000000 55.8480000000000 55.8480000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.7980000000000 55.8480000000000 55.8980000000000 55.8980000000000 55.8480000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.8980000000000 55.9490000000000 55.8980000000000 55.8980000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.8980000000000 55.9990000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9490000000000 55.9990000000000 55.9990000000000 55.9990000000000 56.0980000000000 56.0980000000000 56.0980000000000 56.0980000000000 56.1990000000000 56.1990000000000 56.2490000000000 56.2490000000000 56.3980000000000 56.5980000000000 56.6990000000000 56.8480000000000 56.8980000000000 56.8480000000000 56.5480000000000 56.2980000000000 56.2490000000000 56.4490000000000 56.7980000000000 56.8980000000000 56.8480000000000 56.7980000000000 56.6990000000000 56.5980000000000 56.3480000000000 56.2980000000000 56.2980000000000 56.2490000000000;55.7550000000000 55.7050000000000 55.7050000000000 55.7550000000000 55.7050000000000 55.7550000000000 55.7550000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.8050000000000 55.7550000000000 55.7550000000000 55.7050000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.7550000000000 55.8540000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8050000000000 55.8050000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8050000000000 55.8050000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.8540000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9550000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9040000000000 55.9550000000000 55.9550000000000 55.9550000000000 56.0050000000000 55.9550000000000 55.9550000000000 55.9550000000000 55.9550000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0050000000000 56.0550000000000 56.0550000000000 56.0550000000000 56.1040000000000 56.1540000000000 56.2050000000000 56.2550000000000 56.2550000000000 56.3050000000000 56.3050000000000 56.4550000000000 56.6540000000000 56.8540000000000 56.9550000000000 56.9550000000000 56.8540000000000 56.5050000000000 56.3050000000000 56.4040000000000 56.8050000000000 56.9040000000000 57.0050000000000 56.9550000000000 56.8540000000000 56.7550000000000 56.4040000000000 56.3540000000000 56.3540000000000 56.3050000000000;55.8610000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8610000000000 55.9110000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.8120000000000 55.7620000000000 55.7620000000000 55.7620000000000 55.8120000000000 55.8610000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9110000000000 55.9110000000000 55.9110000000000 55.9110000000000 55.9110000000000 55.8610000000000 55.9110000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.8610000000000 55.9110000000000 55.9110000000000 55.8610000000000 55.9110000000000 55.9110000000000 55.9110000000000 55.9620000000000 55.9110000000000 55.9110000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9620000000000 55.9620000000000 56.0120000000000 55.9620000000000 56.0120000000000 56.0620000000000 56.0120000000000 56.0120000000000 56.0120000000000 56.0620000000000 56.0120000000000 56.0120000000000 56.1110000000000 56.0620000000000 56.0120000000000 56.0620000000000 56.0620000000000 56.0620000000000 56.0620000000000 56.0620000000000 56.1110000000000 56.0620000000000 56.1110000000000 56.1110000000000 56.1110000000000 56.2120000000000 56.2120000000000 56.2120000000000 56.3610000000000 56.5120000000000 56.7620000000000 56.9620000000000 56.9620000000000 57.0120000000000 56.9620000000000 56.6110000000000 56.5620000000000 56.7120000000000 56.8610000000000 57.0120000000000 56.9110000000000 56.7620000000000 56.5620000000000 56.4110000000000 56.3610000000000 56.3120000000000 56.3610000000000;55.7690000000000 55.7690000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.7190000000000 55.8190000000000 55.8680000000000 55.8680000000000 55.8190000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7190000000000 55.7190000000000 55.7690000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.7690000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8190000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.8680000000000 55.9180000000000 55.9180000000000 55.9180000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 56.0190000000000 56.0190000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 55.9690000000000 56.0190000000000 56.0690000000000 56.1180000000000 56.1680000000000 56.2690000000000 56.4690000000000 56.7190000000000 57.0690000000000 57.3680000000000 57.1180000000000 56.6180000000000 56.4690000000000 56.3680000000000 56.4690000000000 56.5190000000000 56.5690000000000 56.5190000000000 56.5690000000000 56.3190000000000 56.2690000000000 56.2690000000000 56.2690000000000;55.7760000000000 55.7260000000000 55.8260000000000 55.7760000000000 55.7260000000000 55.7260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.7760000000000 55.7760000000000 55.7260000000000 55.7260000000000 55.7260000000000 55.7260000000000 55.7260000000000 55.7260000000000 55.7260000000000 55.7760000000000 55.7760000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8750000000000 55.8260000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.7760000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8260000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.8750000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9250000000000 55.9250000000000 55.9250000000000 55.9250000000000 55.9250000000000 55.9250000000000 55.9760000000000 55.9760000000000 56.0260000000000 56.0260000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9760000000000 55.9760000000000 56.0260000000000 56.0260000000000 56.0760000000000 56.1750000000000 56.1750000000000 56.1750000000000 56.1250000000000 56.1750000000000 56.3750000000000 56.7260000000000 57.0260000000000 57.5760000000000 57.6250000000000 57.1250000000000 56.7760000000000 56.5260000000000 56.4250000000000 56.3750000000000 56.3750000000000 56.4250000000000 56.3750000000000 56.3750000000000 56.3750000000000 56.3750000000000 56.3260000000000;55.7830000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7830000000000 55.7330000000000 55.8330000000000 55.8330000000000 55.8820000000000 55.8330000000000 55.7830000000000 55.7830000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7330000000000 55.7830000000000 55.7830000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.7830000000000 55.7830000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8330000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.8820000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9320000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 55.9830000000000 56.0330000000000 56.0330000000000 56.0330000000000 56.0330000000000 56.0330000000000 56.0830000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1820000000000 56.1320000000000 56.3820000000000 56.6320000000000 57.0330000000000 57.5830000000000 57.5330000000000 56.9320000000000 56.8330000000000 56.6820000000000 56.4830000000000 56.3330000000000 56.3330000000000 56.3330000000000 56.3820000000000 56.4320000000000 56.3820000000000 56.4320000000000 56.3820000000000;55.7400000000000 55.7400000000000 55.7900000000000 55.7900000000000 55.8400000000000 55.7900000000000 55.8890000000000 55.8890000000000 55.8890000000000 55.8400000000000 55.7900000000000 55.7900000000000 55.7400000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.8400000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.8890000000000 55.8890000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.8400000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.7900000000000 55.8890000000000 55.8400000000000 55.8890000000000 55.8890000000000 55.8890000000000 55.8890000000000 55.8890000000000 55.8890000000000 55.9390000000000 55.9390000000000 55.9390000000000 55.9390000000000 55.9390000000000 55.9390000000000 55.8890000000000 55.8890000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 55.9900000000000 56.0400000000000 56.0400000000000 55.9900000000000 56.0400000000000 56.0400000000000 56.0400000000000 56.0400000000000 56.0400000000000 56.0400000000000 56.0900000000000 56.1390000000000 56.1390000000000 56.2400000000000 56.2400000000000 56.2400000000000 56.2400000000000 56.1890000000000 56.3890000000000 56.5900000000000 56.9390000000000 57.3400000000000 57.5400000000000 57.1890000000000 56.9900000000000 56.6890000000000 56.5900000000000 56.3890000000000 56.2900000000000 56.2900000000000 56.2900000000000 56.2900000000000 56.3890000000000 56.3890000000000 56.3400000000000;55.7470000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8960000000000 55.8960000000000 55.8470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7470000000000 55.7970000000000 55.7970000000000 55.8960000000000 55.9970000000000 56.0470000000000 56.0470000000000 55.9460000000000 55.8960000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.7970000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8470000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.8960000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9460000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 55.9970000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.0470000000000 56.1460000000000 56.1960000000000 56.2970000000000 56.2470000000000 56.2470000000000 56.2470000000000 56.4460000000000 56.5970000000000 56.9460000000000 57.1960000000000 57.1960000000000 57.1460000000000 57.1460000000000 57.0470000000000 56.7470000000000 56.5470000000000 56.4460000000000 56.3470000000000 56.2970000000000 56.3470000000000 56.3470000000000 56.3960000000000 56.3960000000000];

o = SICM.SICMScan.FromZDataGrid(z);
o.setXSize(50);
o.setYSize(50);

o.setClean();

function varargout = flatten(self, method, varargin)
# Flattening of the data using different methods
#
#    Examples: 
#      
#      obj.flatten(method)
#        
#        Flattens the data using `method` (see below).
#
#      newobj = obj.flatten(method)
#
#        As above, but returns a new SICMScan object with the flattend
#        data.
#
#  
# The methods available are listed below. Some have additional arguments
# that can or have to be passed to the function. The meaning is explained
# in the corresponding description:
#
# Methods available:
# ==================
#
#  'plane': 
#     Subtracts a plane from the data. 
#     If no additional arguments are provided, tries to fit a plane to the
#     data and subtract it.
#     An optional second argument might be provided that contains three
#     data points (in indices to the pixels in zdata_grid) that define the
#     the plane. The format should be:
#              [1 1; 1 2; 2 1]
#     which would use the pixels at indices (1,1), (1,2) and (2,1) for the 
#     plane definition. (Use of additional arguments is not yet
#     implemented) 
#
# 'paraboloid':
#    Subtracts a paraboloid fitted to the data. Useful for small sections
#    of a cell.
#
# 'linewise':
#    First subtracts a plane, then fits a line to every data line along the
#    x-axis.
# 'polyXX':
#    Subtracts a 2D polynomial, the degree of the polynomial should be
#    passed as optional parameter.


    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.flatten(method, varargin{:})
        varargout{1} = o;
        return
    end
    
    # Known methods...
    
    methods = struct(...
        'plane', @local_flattenPlane,...
        'paraboloid', @local_flattenParaboloid,...
        'linewise', @local_flattenLinewise,...
        'linewisemean', @local_flattenLinewiseMean,...
        'linewiseY', @local_flattenLinewiseY,...
        'polyXX', @local_flattenPoly,...
        'manual', @local_flatten_manual ...
    );

    data = feval(methods.(method), self, varargin{:});
    self.zdata_grid = data;
    self.upd_zlin_();
    
end

function data = local_flattenPlane(obj, varargin)
    
    if nargin == 1
        x = obj.xdata_lin;
        y = obj.ydata_lin;
        z = obj.zdata_lin;
        [fo, go] = fit([x,y],z,'poly11');
        d = obj.zdata_grid - feval(fo, obj.xdata_grid, obj.ydata_grid);
        p25 = prctile(d(:), 25);
        excludeIdx = find(d(:) > p25);
        [fo, go] = fit([x,y],d(:),'poly11','Exclude',excludeIdx);
        data = d - feval(fo, obj.xdata_grid, obj.ydata_grid);
    end
end

function data = local_flattenParaboloid(obj, varargin)
    if nargin == 1
        x = obj.xdata_lin;
        y = obj.ydata_lin;
        z = obj.zdata_lin;
        [fo, go] = fit([x,y],z,'poly22');
        data = obj.zdata_grid - feval(fo, obj.xdata_grid, obj.ydata_grid);
    end
end

function data = local_flattenLinewise(obj, varargin)
    omit = [];
    if nargin == 1
        p = 25;
    else
        p = varargin{1};
        if nargin == 4
            omit = varargin{3};
        end
    end
    data = obj.zdata_grid'; #local_flattenPlane(obj);
    sz = size(data);
    ndata = zeros(sz(1), sz(2));
    for y = 1:sz(1)
        l = data(y,:);
        if any(omit==y)
            ndata(y,:) = l;
            continue
        end

        p25 = prctile(l, p);
        eIdx = find(l > p25);
        fo = fit((0:length(l)-1)', l', 'poly1', 'Exclude', eIdx);
        ndata(y,:) = l - (feval(fo,  0: length(l)-1))';
    end
    data = ndata';
end

function data = local_flattenLinewiseMean(obj, varargin)
    data = obj.zdata_grid;
    sz = size(data);
    
    ndata = zeros(sz(1), sz(2));
    for y = 1:sz(1)
        l = data(y,:);
        fo = fit((0:length(l)-1)', l', 'poly1');
        fdata = feval(fo,  0: length(l)-1)';
        
        
        #size(l)
        #size(fdata)
        ndata(y,:) = l - fdata;
        
        if y == 1
            figure;
            plot(l,'Color',[.5 .5 .5]);
            hold on;
            plot(fdata','r');
            plot(ndata(y,:), 'k');
        end
            
    end
    data = ndata;
end

function data = local_flattenLinewiseY(obj, varargin)
    data = obj.zdata_grid;
    sz = size(data);
    
    ndata = zeros(sz(1), sz(2));
    for x = 1:sz(2)
        l = data(:,x);
        fo = fit((0:length(l)-1)', l, 'poly1');
        fdata = feval(fo,  0: length(l)-1);
        
        
        #size(l)
        #size(fdata)
        ndata(:,x) = l - fdata;
        
        if x == 1
            figure;
            plot(l,'Color',[.5 .5 .5]);
            hold on;
            plot(fdata','r');
            plot(ndata(:,x), 'k');
        end
            
    end
    data = ndata;
end

function data = local_flattenPoly(obj, varargin)
    if nargin >= 2
        x = obj.xdata_lin;
        y = obj.ydata_lin;
        z = obj.zdata_lin;
        if nargin == 2
            [fo, ~] = fit([x,y],z,sprintf('poly#g#g',varargin{1}, varargin{1}));
        else
            [fo, ~] = fit([x,y],z,sprintf('poly#g#g',varargin{1}, varargin{1}), varargin{2:end});
        end
        try
            data = obj.zdata_grid - feval(fo, obj.xdata_grid, obj.ydata_grid);
        catch
            data = obj.zdata_grid - feval(fo, obj.xdata_grid', obj.ydata_grid');
        end
    end
end

function data = local_flatten_manual(obj)
    app = SICM.SICMScanFlattenApp(obj);
    function local_assign_result(scan)
        data = scan.zdata_grid;
    end
    app.CloseCallback = @local_assign_result;
    waitfor(app.Figure);
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: {'Plane','Paraboloid','Linewise','Linewise (mean)', 'Linewise Y', 'polyXX'}
#+GMD FixedArgs: {'plane','paraboloid', 'linewise', 'linewisemean', 'linewiseY', 'polyXX'}
#+GMD VarArgs: {struct(), struct(), struct('type','int','desc','Which percentile to use (in percent)'), struct(), struct(), struct('type','int','desc','Degree of polynomial (1 to 5)')}
#+GMD Depends: {}
#+GMD Changes: {'z'}
#+GMD Immediate: 0
#+GMD Menu: 'Flatten'
#+END GUIMETADATA

function varargout = filter(self, method, varargin)
# Filtering of the data using different methods
#
#    Examples: 
#      
#      obj.filter(method)
#        
#        Filters the data using `method` (see below).
#
#      newobj = obj.filter(method)
#
#        As above, but returns a new SICMScan object with the filtered
#        data.
#
#  
# The methods available are listed below. Some have additional arguments
# that can or have to be passed to the function. The meaning is explained
# in the corresponding description:
#
# Methods available:
# ==================
#
#  'median': 
#     Sets the pixel value to the median of the surroundings. Filter width
#     must be applied as second argument:
#
#     obj.filter('median', 5)
#
#  'outliers':
#     Looks for outliers that differ by more than a threshold from the
#     mean of its eight neighbours and replaces them by the mean of the
#     neighbours. For example: 
#  
#       obj.filter('outliers', 30)
# 
#     will filter all pixels that differ by 30 z-units. Thus, the z-scaling
#     is important. To be independent from the scaling, the option
#     'std' can be given as third argument. Thus, every pixel
#     exceeding the x-fold of the standard deviation of its neighbours will 
#     be filtered: 
#
#       obj.filter('outliers', 2, 'std')

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.filter(method, varargin{:})
        varargout{1} = o;
        return
    end
    
    # Known methods...
    
    methods = struct(...
        'median', @local_filterMedian,...
        'average', @local_filterAverage,...
        'outliers', @local_filterNeighbours...
    );

    data = feval(methods.(method), self, varargin{:});
    self.zdata_grid = data;
    self.upd_zlin_();
    
end

function data = local_filterMedian(obj, varargin)
    data = medfilt2(obj.zdata_grid, [varargin{1} varargin{1}],'symmetric');
end
function data = local_filterAverage(obj, varargin)
    h = fspecial('average', [varargin{1} varargin{1}]);
    data = filter2(h, obj.zdata_grid);
end
function data = local_filterNeighbours(obj, varargin)

    deviation = nargin > 2 && strcmp('std', varargin{2});
    data = obj.zdata_grid;
    sz = size(data);
    n=zeros(1,8);
    plot(obj); hold on
    for row = 2 : sz(1) - 1
        for col = 2: sz(2) - 1
            n(1) = obj.zdata_grid(row-1, col-1);
            n(2) = obj.zdata_grid(row-1, col  );
            n(3) = obj.zdata_grid(row-1, col-1);
            n(4) = obj.zdata_grid(row-1, col);
            n(5) = obj.zdata_grid(row+1, col);
            n(6) = obj.zdata_grid(row-1, col+1);
            n(7) = obj.zdata_grid(row  , col+1);
            n(8) = obj.zdata_grid(row+1, col+1);
            m = mean(n);
            if deviation 
                thresh = varargin{1} * std(n);
            else
                thresh = varargin{1};
            end
            if abs(obj.zdata_grid(row, col)-m) > thresh 
                data(row, col) = m;
                
            end
        end
    end
end
#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: {'Median','Average'}
#+GMD FixedArgs: {'median','average'}
#+GMD VarArgs: {struct('type','int','desc','Width of the filter window'), struct('type','int','desc','Width of the filter window')}
#+GMD Depends: {}
#+GMD Changes: {'z'}
#+GMD Immediate: 0
#+GMD Menu: 'Filter'
#+END GUIMETADATA

function t = fduration(self, varargin)
# Returns a formatted string of the duration of the scan.
# 
#    Examples: 
#    
#      obj.fduration(format_string)
#        
#        Returns a string representation of the duration of the scan
#        according to format_string. Within this format string, the
#        following values are replaced with their respective counterparts:
#      
#        #n: The duration in milliseconds (as in the durattion-property)
#        #s: The duration in seconds, rounded
#        #m: The duration in minutes, rounded
#        #h: The duration in hours, rounded
#  
#        The next replacements express the duration as HH:MM:SS:NNN, where
#        HH is the amount of hours, MM the amount of minutes, SS the amount
#        of seconds and NNN the amount of milliseconds. 
#
#        #N: NNN of the above
#        #S: SS of the above
#        #M: MM of the above
#        #H: HH of the above
#
#      obj.fduration()
#        
#        Uses the default format string '#H:#M:#S.#N'
#
#   Note the following:
#
#      # Generate an empty SICMScan object:
#      foo = SICM.SICMScan();
#      # Set its duration to 4h, 35m, 21s and 123ms:
#      foo.duration = 60*60*1e3 * 4  ... # Hours
#                   + 60*1e3    * 35 ... # Minutes
#                   + 1e3       * 21 ... # Seconds     
#                   +             123   # Millisecodns
#
#   
#
#     foo.fduration('#m')
#     ans =   
#     275
# 
#     # This is the duration in minutes
#
#     foo.fduration('#M')
#     ans = 
#     35
#
#     # The minutes-part of the total duration 

    if isnan (self.duration) 
        t = '';
        return;    
    end
    duration = struct();
    duration.n = self.duration;
    duration.s = round(self.duration/1000);
    duration.m = round(duration.s/60);
    duration.h = round(duration.m/60);
    
    
    duration.H = floor(self.duration / ( 60*60*1000));
    tmp_d = self.duration - duration.H * 60*60*1000;
    duration.M = floor(tmp_d / (60*1000));
    tmp_d = tmp_d - duration.M * 60*1000;
    duration.S = floor(tmp_d/1000);
    duration.N = mod(self.duration, 1000);
    
    if nargin > 1
        format = varargin{1};
    else
        format = '#H:#M:#S.#N';
    end
    #
    # Alas, the follwing does not wark as I would expect
    #
    #t = strrep(format, ...
    #    { '#n', '#s', '#m', '#h', '#H', '#M', '#S', '#N'}, ...
    #    { ...
    #        num2str(duration.n), ...
    #        num2str(duration.s), num2str(duration.m), num2str(duration.h), ...
    #        num2str(duration.H), num2str(duration.M), num2str(duration.S), ...
    #        num2str(duration.N) ...
    #    });
    #
    # So I have to call strrep manually for every field:
    
    t = format;
    fnames = fieldnames(duration);
    for needle = fnames'
        t = strrep(t, ['#', needle{1}], num2str(duration.(needle{1})) );
    end
    
end

function varargout = eachAppCurve(self, fhandle)
# This function applies the function handle provided by handle to each of
# the approach curves. For example, to fit all approach curves, use:
#
#   obj.eachAppCurve(@fit)
#
# This function is quite similar to the build-in cellfun function. However,
# the first arguments that is passed to the function is the SICMAppCurve
# object.
#
# See also CELLFUN

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.eachAppCurve(fhandle);
        varargout{1} = o;
        return
    end
    #for i = 1:length(self.approachcurves)
    #    feval(fhandle, self.approachcurves{i}, varargin{:});
    #end
    
    cellfun(fhandle, self.approachcurves);

function h = distance (self)
# Determination of the distance between two points (in pixel). 
#
# Uses the imdistline function of matlab.
#
    figure; 
    self.imagesc();
    h = imdistline(gca);
end

#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meas'
#+GMD Name: 'Measure Distance'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {}
#+GMD Immediate: 0
#+GMD Menu: 'Measurements'
#+END GUIMETADATA

function varargout = crop(self, varargin)
# allows to crop a piece from the scan data
#
# One can either provide a set of x, y, width, height values to crop the
# data:
#
#   scan.crop(0,0,50,50)
#
# or omit the values. In the latter case, a picture of the data is shown
# (via imagesc) and one can select a rectangular area.
#
# As always, if an output variable is specified, a new scan object is
# returned.

    if nargout == 1
        o = SICM.SICMScan.fromSICMScan_(self);
        o.crop(varargin{:})
        varargout{1} = o;
        return
    end
    
    if nargin > 1
        r= [varargin{1},...
            varargin{2},...
            varargin{3},...
            varargin{4}];
        r = round(r);
    else
        f = figure;
        imagesc(self.zdata_grid);
        r = getrect;
        close(f);
        r = round(r);
        r(1:2) = r(1:2) +1;
        if r(1) > self.xpx || r(2) > self.ypx 
            warning('SICMScan:DataOutsideRange', ...
                'Data cannot be cropped.');
            return
        end
    end
    self.zdata_grid = self.zdata_grid(r(2):r(2)+r(4), r(1):r(1)+r(3));
    self.ydata_grid = self.ydata_grid(r(2):r(2)+r(4), r(1):r(1)+r(3));
    self.xdata_grid = self.xdata_grid(r(2):r(2)+r(4), r(1):r(1)+r(3));
        
    self.zdata_lin = self.zdata_grid(:);
    self.xdata_lin = self.xdata_grid(:);
    self.ydata_lin = self.ydata_grid(:);
        
    self.xpx = r(4)+1;
    self.ypx = r(3)+1;
        
    self.xsize = self.xpx * self.stepx;
    self.ysize = self.ypx * self.stepy;
   
    
    
#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'meth'
#+GMD Name: 'Crop'
#+GMD FixedArgs: {}
#+GMD VarArgs: {}
#+GMD Depends: {}
#+GMD Changes: {'x','y','z'}
#+GMD Immediate: 0
#+GMD Menu: 'Simple Manipulations'
#+END GUIMETADATA

function varargout = changeXY(self)
def changeXY(self):
# Changes x and y values
    if newObject==False:
        tmp_y = self.xdata_grid
        self.xdata_grid = self.ydata_grid
        self.ydata_grid = tmp_y
        self.xdata_lin = self.xdata_grid(:)
        self.ydata_lin = self.ydata_grid(:)
        return None
    else:
        o = SICM.SICMScan.fromSICMScan_(self);
        o.changeXY();
        return o

function c = centroid(self, threshold)
# Compute the centroid of a projection of the data equal or exceeding
# threshold to the z=0 plane. 
#
#    Example 
#      c = obj.centroid(2)
#
#        Computes the centroid of the projection of the data points equal
#        or larger than 2.
#
#        c is in the form [x-coordinate, y-coordinate]

    # Compute the projection
    proj = self.zdata_grid > threshold;
    
    props = regionprops(proj);
    
    areas = [props.Area];
    midx = find(areas == max(areas));
    
    c = [props(midx).Centroid(2) * self.stepx ...
         props(midx).Centroid(1) * self.stepy];



## This is the old version of the computation
#     
#     # Number of points in the projection
#     n = sum(proj(:));
#     
#     # If the projection does not contain any values, return NaN
#     if n == 0
#         c = [NaN, NaN];
#         return
#     end
#     
#     x_tmp = self.xdata_grid .* proj;
#     y_tmp = self.ydata_grid .* proj;
#     
#     x_coord = sum(x_tmp(:)) / n;
#     y_coord = sum(y_tmp(:)) / n;
#     
#     c = [x_coord, y_coord];
# end
    
#TODO: Everything
def area(self):
# Computes the area of the scan.
#
# Example: 
#   a = scan.area()

    # If the data does not contain NaNs, use this method, it is fast
    if sum(isnan(self.zdata_grid(:))) == 0:

        [m, n] = size(self.zdata_grid)

        dx = self.stepx
        dy = self.stepy
        Z = self.zdata_grid

        areas = ...
            0.5*sqrt((dx*dy)^2 + (dy*(Z(1:m-1,2:n) - Z(1:m-1,1:n-1))).^2 + ...
            (dx*(Z(2:m,1:n-1) - Z(1:m-1,1:n-1))).^2)...
            +...
            0.5*sqrt((dx*dy)^2 + (dx*(Z(1:m-1,2:n) - Z(2:m,2:n))).^2 + ...
            (dy*(Z(2:m,1:n-1) - Z(2:m,2:n))).^2);

        a = sum(areas(:));
        
    else:
        if sum(isnan(self.zdata_grid(:))) == length(self.zdata_grid(:)):
            a = 0
            return a
        end
        fprintf('NaNs detected in surface data. Calculation may take long.\n');
        a = 0;
        X = self.xdata_grid;
        Y = self.ydata_grid;
        Z = self.zdata_grid;
        lX = length(X);
        lY = length(Y);
        for nx = 1:lX-1
            for ny = 1:lY-1

                eX = [X(ny,nx)   X(ny,nx+1) 
                    X(ny+1,nx) X(ny+1,nx+1)]
                eY = [Y(ny,nx)   Y(ny,nx+1) 
                    Y(ny+1,nx) Y(ny+1,nx+1)]
                eZ = [Z(ny,nx)   Z(ny,nx+1) 
                    Z(ny+1,nx) Z(ny+1,nx+1)]

                # take two triangles, calculate the cross product to get the surface area
                # and sum them.
                v1 = [eX(1,1) eY(1,1) eZ(1,1)]
                v2 = [eX(1,2) eY(1,2) eZ(1,2)]
                v3 = [eX(2,1) eY(2,1) eZ(2,1)]
                v4 = [eX(2,2) eY(2,2) eZ(2,2)]
                if ~(isnan(eZ(1,1)) or isnan(eZ(1,2)) or isnan(eZ(2,1)))
                    a  = a + norm(cross(v2-v1,v3-v1))/2
                end
                if ~(isnan(eZ(2,2)) or isnan(eZ(1,2)) or isnan(eZ(2,1)))
                    a  = a + norm(cross(v2-v4,v3-v4))/2
    return a


#+BEGIN GUIMETADATA: Do not delete
#+GMD Type: 'prop'
#+GMD Name: 'Area'
#+GMD Depends: {'x','y','z'}
#+GMD Changes: {}
#+GMD Immediate: 0
#+GMD Unit: 'sqrt([x]×[y])×[z]'
#+END GUIMETADATA

def applyMask(self, mask,newObject=False):
# Applies a binary mask to the data.
#
#    A binary mask is a two dimensional vector of zeros and ones that has
#    the same size as the zdata_grid. Applying this mask multiplies the
#    zdata_grid and the mask element by element, hence setting the zdata to
#    zero where the mask contains zero and leaving the zdata unaltered
#    where the mask is  one.
#
#    Assume the follwing mask:
#      mask = [0 1 0;...
#              1 1 1;...
#              0 1 0]
#
#    and a SICMScan object `obj` with the following zdata_grid:
#      obj.zdata_grid = [.1 .2 .3;
#                        .4 .5 .6;
#                        .7 .8 .9]
#
#    Examples:
#
#       obj.applyMask(mask);
#
#         The zdata_grid will look like this:
#           obj.zdata_grid = [ 0 .2  0;
#                             .4 .5 .6;
#                              0 .8  0]
#
#       newobj = obj.applyMask(mask)
#        
#         As above, but retruns a new object instead of modifying `obj`

    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.applyMask(mask)
        return o
    
    self.zdata_grid = self.zdata_grid * mask
    self.upd_zlin_()
    return None

def addYOffset(self, yoffset, newObject=False):
# Shifts the data by `yoffset` in y-direction
#
#    Examples:
#
#      obj.addYOffset(2)
#
#        Shifts the data in `obj` by 2 length units.
#
#      newobj = obj.addYOffset(2)
#
#        As above, but reutrns a new object instead of modifying `obj`.

    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self);
        o.addYOffset(yoffset);
        return o
    end
    
    self.ydata_grid = self.ydata_grid + yoffset;
    self.ydata_lin = self.ydata_grid(:);
    
    self.IsDirty = true;
    return None

def addXOffset(self, xoffset, newObject=False):
# Shifts the data by `xoffset` in x-direction
#
#    Examples:
#
#      obj.addXOffset(2)
#
#        Shifts the data in `obj` by 2 length units.
#
#      newobj = obj.addXOffset(2)
#
#        As above, but reutrns a new object instead of modifying `obj`.

    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.addXOffset(xoffset)
        return o    
    self.xdata_grid = self.xdata_grid + xoffset
    self.xdata_lin = self.xdata_grid[:]
    return None
    
    