classdef SICMAppCurve < SICM.importer & matlab.mixin.Copyable
# This class provides tools to analyse and process SICM approach curves.


    #properties (SetAccess = protected, SetObservable)
    xdata = None # holds the x-data, that is the piezo extension
    ydata = None # holds the voltage data
    mode = None # VC or CC mode
    direction = None # Was the piezo increasing or decreasing...
    fitobject = []; # Holds thh fit object, once the method `fit`has been called.
    filename = None
    FallRate = None
    Threshold = None
    info = struct;
    SamplingRate = None
    
    #properties (Hidden)
    importers = {...
        struct(...
            'name'   , 'AscII importer, PH', ...
            'exts'   , '*.sic;',...
            'expl'   , 'Two-column ASCII data files (*.sic)',...
            'extlist', {'.sic'},...
            'handle' , @local_ImportAscii_sic...
        ),...
        struct(...
            'name'   , 'AscII importer for ac files, PH', ...
            'exts'   , '*.ac;',...
            'expl'   , 'Three-column ASCII data files (*.ac)',...
            'extlist', {'.ac'},...
            'handle' , @local_ImportAscii_ac...
        ),...
        struct(...
            'name'   , 'Binary Importer, AG', ...
            'exts'   , '*.sicm;',...
            'expl'   , 'Binary Data (*.sicm)',...
            'extlist', {'.sicm'},...
            'handle' , @local_ImportBinary_sicm...
        ),...
    }
    fitfunc = []; #holds the fit function...
    inversefitfunc = []; # holds the inversed fit function
    fitproblems = 0;
    
    #properties (Constant)
    modes = struct(...
        'VC', 0, ...# Voltage Clamp mode
        'CC', 1  ...# Current Clamp mode
    )
    directions = struct(...
        'INC', 0, ...
        'DEC', 1 ...
    )

    methods (Static)
       o = FromFile(varargin)
       o = FromXYData(x,y)
       o = FromXYData_info(x,y,FallRate,Threshold)
       
       # internal functions...
       o = fromSICMAppCurve_(obj)
    end
    methods (Access = public)
        # Constructor
        function self = SICMAppCurve()
        # Generates an empty SICMAppCurve object. Rarely used. The static
        # methods FROMFILE and FROMXYDATA generate a SICMAppCurve object
        # that contains data.
        #
        # See also FROMFILE, FROMXYDATA
        end
        
        # Methods to describe the data:
        
        varargout = setMode(self, mode)
        varargout = setDirection(self, direction)
        varargout = setFitFunc(self, handle)
        
        # Methods to manipulate the data
        
        varargout = normalize(self, varargin)
        varargout = inverse(self)
        varargout = reverse(self)
        varargout = autoDetectSamplingRate( self, varargin )
        scaleX (self, factor, varargin);
        scaleY (self, factor, varargin);
        
        varargout = shiftX( self, offset );
        varargout = shiftY( self, offset );
        
        varargout = addInfo( self, info, value);
        # Methods to analyse the data automaticlly
        
        varargout = guessCurveType(self, varargin);
        varargout = guessMode(self, varargin);
        varargout = guessDirection(self, varargin);
        varargout = guessFitFunc(self, varargin);
        varargout = setSamplingRate(self, rate);
        # Methods to visualize the data
        varargout = plot(self, varargin);
        varargout = filter(self, varargin);
        varargout = frequencyPlot(self);
        # fitting
        
        varargout = fit(self, varargin);
        varargout = fitToThreshold(self, T);
        fitIsOk(self);
    end
    methods (Access = protected)
        [I0, C, D] = guessStartPoint(self);
        b = returnValIfVarArgEmpty_(self, val, varargin);
    end
end


# Importer functions

function o = local_ImportAscii_sic(filename)
	fid = fopen(filename);
    res = textscan(fid, '#s #s','headerLines',1);
    # text import is always a bit ugly...
    o = SICM.SICMAppCurve.FromXYData(...
        str2double(strrep(res{2}(:,1),',','.')),...
        str2double(strrep(res{1}(:,1),',','.')));
end

function o = local_ImportAscii_ac(filename)
	fid = fopen(filename);
    
    res = textscan(fid, '#s #s #s','headerLines',1);
    # This import throws away the resistance data
    o = SICM.SICMAppCurve.FromXYData(...
        str2double(strrep(res{1}(:,1),',','.')),...
        str2double(strrep(res{3}(:,1),',','.')));
end

function o = local_ImportBinary_sicm(filename)
    [~,purefilename,~] = fileparts(filename);    
    tempdirname = tempname;
    gunzip(filename, tempdirname);
    untar([tempdirname filesep purefilename], tempdirname);
    
    filelist = dir(tempdirname);
    
    # information about the size etc. are stored in json format in a file
    # called settings.json
    fid = fopen([tempdirname filesep 'settings.json']);
    cjson = textscan(fid,'#s');
    fclose(fid);
    sjson = cjson{1}{1};
    info = jsondecode(sjson);
    
    for i=1:size(filelist,1)
        [~,purefilename2,ext] = fileparts(filelist(i).name);
        if isempty(ext) && ~strcmp(purefilename2, purefilename)
            datafile = purefilename2;
        end
    end
    
    fid = fopen([tempdirname filesep datafile]);
    data = fread(fid,'uint16');
    try
        rmdir(tempdirname, 's');
    catch ME
        warning('SICMAppCurve:CleanupPropblem', ...
            'Was not able to delete\n  #s\nYou can safely remove this directory and its contents.', ...
            tempdirname);
    end
    o = SICM.SICMAppCurve.FromXYData(...
        (1:length(data))', ...
        double(data));
    o.info = info;
    o.filename = filename;
    try  ##ok<TRYNC>
        o.FallRate = str2double(info.FallRate);
    end
    try ##ok<TRYNC>
        o.Threshold = str2double(info.Threshold)/100;
    end
end

'''
classdef SICMAppCurve < SICM.importer & matlab.mixin.Copyable
# This class provides tools to analyse and process SICM approach curves.


    properties (SetAccess = protected, SetObservable)
        xdata = NaN; # holds the x-data, that is the piezo extension
        ydata = NaN; # holds the voltage data
        mode = NaN; # VC or CC mode
        direction = NaN; # Was the piezo increasing or decreasing...
        fitobject = []; # Holds thh fit object, once the method `fit`has been called.
        filename = NaN;
        FallRate = NaN;
        Threshold = NaN;
        info = struct;
        SamplingRate = NaN;
    end
    
    properties (Hidden)
        importers = {...
            struct(...
                'name'   , 'AscII importer, PH', ...
                'exts'   , '*.sic;',...
                'expl'   , 'Two-column ASCII data files (*.sic)',...
                'extlist', {'.sic'},...
                'handle' , @local_ImportAscii_sic...
            ),...
            struct(...
                'name'   , 'AscII importer for ac files, PH', ...
                'exts'   , '*.ac;',...
                'expl'   , 'Three-column ASCII data files (*.ac)',...
                'extlist', {'.ac'},...
                'handle' , @local_ImportAscii_ac...
            ),...
            struct(...
                'name'   , 'Binary Importer, AG', ...
                'exts'   , '*.sicm;',...
                'expl'   , 'Binary Data (*.sicm)',...
                'extlist', {'.sicm'},...
                'handle' , @local_ImportBinary_sicm...
            ),...
        }
        fitfunc = []; #holds the fit function...
        inversefitfunc = []; # holds the inversed fit function
        fitproblems = 0;
    end
    
    properties (Constant)
        modes = struct(...
            'VC', 0, ...# Voltage Clamp mode
            'CC', 1  ...# Current Clamp mode
        ); 
        directions = struct(...
            'INC', 0, ...
            'DEC', 1 ...
        );
    end

    methods (Static)
       o = FromFile(varargin)
       o = FromXYData(x,y)
       o = FromXYData_info(x,y,FallRate,Threshold)
       
       # internal functions...
       o = fromSICMAppCurve_(obj)
    end
    methods (Access = public)
        # Constructor
        function self = SICMAppCurve()
        # Generates an empty SICMAppCurve object. Rarely used. The static
        # methods FROMFILE and FROMXYDATA generate a SICMAppCurve object
        # that contains data.
        #
        # See also FROMFILE, FROMXYDATA
        end
        
        # Methods to describe the data:
        
        varargout = setMode(self, mode)
        varargout = setDirection(self, direction)
        varargout = setFitFunc(self, handle)
        
        # Methods to manipulate the data
        
        varargout = normalize(self, varargin)
        varargout = inverse(self)
        varargout = reverse(self)
        varargout = autoDetectSamplingRate( self, varargin )
        scaleX (self, factor, varargin);
        scaleY (self, factor, varargin);
        
        varargout = shiftX( self, offset );
        varargout = shiftY( self, offset );
        
        varargout = addInfo( self, info, value);
        # Methods to analyse the data automaticlly
        
        varargout = guessCurveType(self, varargin);
        varargout = guessMode(self, varargin);
        varargout = guessDirection(self, varargin);
        varargout = guessFitFunc(self, varargin);
        varargout = setSamplingRate(self, rate);
        # Methods to visualize the data
        varargout = plot(self, varargin);
        varargout = filter(self, varargin);
        varargout = frequencyPlot(self);
        # fitting
        
        varargout = fit(self, varargin);
        varargout = fitToThreshold(self, T);
        fitIsOk(self);
    end
    methods (Access = protected)
        [I0, C, D] = guessStartPoint(self);
        b = returnValIfVarArgEmpty_(self, val, varargin);
    end
end


# Importer functions

function o = local_ImportAscii_sic(filename)
	fid = fopen(filename);
    res = textscan(fid, '#s #s','headerLines',1);
    # text import is always a bit ugly...
    o = SICM.SICMAppCurve.FromXYData(...
        str2double(strrep(res{2}(:,1),',','.')),...
        str2double(strrep(res{1}(:,1),',','.')));
end

function o = local_ImportAscii_ac(filename)
	fid = fopen(filename);
    
    res = textscan(fid, '#s #s #s','headerLines',1);
    # This import throws away the resistance data
    o = SICM.SICMAppCurve.FromXYData(...
        str2double(strrep(res{1}(:,1),',','.')),...
        str2double(strrep(res{3}(:,1),',','.')));
end

function o = local_ImportBinary_sicm(filename)
    [~,purefilename,~] = fileparts(filename);    
    tempdirname = tempname;
    gunzip(filename, tempdirname);
    untar([tempdirname filesep purefilename], tempdirname);
    
    filelist = dir(tempdirname);
    
    # information about the size etc. are stored in json format in a file
    # called settings.json
    fid = fopen([tempdirname filesep 'settings.json']);
    cjson = textscan(fid,'#s');
    fclose(fid);
    sjson = cjson{1}{1};
    info = jsondecode(sjson);
    
    for i=1:size(filelist,1)
        [~,purefilename2,ext] = fileparts(filelist(i).name);
        if isempty(ext) && ~strcmp(purefilename2, purefilename)
            datafile = purefilename2;
        end
    end
    
    fid = fopen([tempdirname filesep datafile]);
    data = fread(fid,'uint16');
    try
        rmdir(tempdirname, 's');
    catch ME
        warning('SICMAppCurve:CleanupPropblem', ...
            'Was not able to delete\n  #s\nYou can safely remove this directory and its contents.', ...
            tempdirname);
    end
    o = SICM.SICMAppCurve.FromXYData(...
        (1:length(data))', ...
        double(data));
    o.info = info;
    o.filename = filename;
    try  ##ok<TRYNC>
        o.FallRate = str2double(info.FallRate);
    end
    try ##ok<TRYNC>
        o.Threshold = str2double(info.Threshold)/100;
    end
end
'''

def shiftX(self, offset, newObject=False):
# Shifts the xdata by /offset/
#
#    Examples:
#      
#      obj.shiftX(100)
#
#        Shifts the xdata by 100.
#
#      newobj = obj.shiftX(100)
#
#        returns a new SICMAppCurve object with shifted xdata.

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.shiftX(offset)
        return o
    self.xdata = self.xdata + offset
    return None

def shiftY(self, offset, newObject=False):
# Shifts the xdata by /offset/
#
#    Examples:
#      
#      obj.shiftY(100)
#
#        Shifts the ydata by 100.
#
#      newobj = obj.shiftY(100)
#
#        returns a new SICMAppCurve object with shifted ydata.
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.shiftY(offset)
        return o
    self.ydata = self.ydata + offset
    return None

def setSamplingRate(self, rate, newObject=False): 

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.setSamplingRate(rate)
        return o    
    self.SamplingRate = rate
    return None


def setMode(self, mode, newObject=False):
# Sets the mode (CC or VC) of an approach curve
#
#    Examples:
#      
#      obj.setMode(SICM.SICMAppCurve.modes.VC)
#
#        Sets the mode of `obj` to VC.
#
#      newobj = obj.setMode(SICM.SICMAppCurve.modes.VC)
#
#        returns a new SICMAppCurve object with mode VC.

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.setMode(mode);
        return o
    self.mode = mode;
    return None

def setInverseFitFunc(self, fhandle):
# Sets the inverse fit function. Requires a function handle as input.
    self.inversefitfunc = fhandle


def setFitObject(self, fitobject, newObject=False):
# Set's the fitobject of the approach Curve
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.setFitobject(fitobject)
        return o
    self.fitobject = fitobject
    self.fitproblems = 0
    return None

def setFitFunc(self, handle, newObject=False):
# Sets the fit function handle used for the object.
#
# Examples:
#    ffunc = @(U0, C, d, x) (U0*(1+C/(x-d))
#
#    obj.setFitFunc(ffunc);
#
#      Sets the fit function to the function ffunc
#
#   newobj = obj.setFitFunc(ffunc);
#
#      Returns a new object with fit function ffunc

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.setFitFunc(handle)
        return o
    self.fitfunc = handle;
    return None

def setDirection(self, direction, newObject=False):
# Sets the direction (INC or DEC) of an approach curve
#
#    Examples:
#      
#      obj.setDirection(SICM.SICMAppCurve.directions.INC)
#
#        Sets the direction of `obj` to INCC.
#
#      newobj = obj.setDirection(SICM.SICMAppCurve.directions.INC)
#
#        returns a new SICMAppCurve object with direction INC.

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.setDirection(direction);
        return o
    self.direction = direction;
    return None

def scaleY(self, factor, offset=0):
    data = self.ydata
    data = data - offset
    data = data * factor
    self.ydata = data

def scaleX(self, factor, offset=0):
    data = self.xdata
    data = data - offset
    data = data * factor
    self.xdata = data

def reverseData(self):
# Reverse the y-data
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.reverseData();
        return o    
    self.ydata = self.ydata(end:-1:1); #Determine how to do this, based on data structure of ydata
    return None

def returnValIfVargArgEmpty_(self, val, b = -1):
    # Internal function
    #
    # Returns `val`if varargin is empty, varargin{1} otherwise.
    if b != -1:
        b = val
    return b

function varargout = readAllAppCurves(self, fhandle)
def readAllAppCurves(self, fhandle, newObject=False):
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
    if newObject:
        o = SICM.SICMScan.fromSICMScan_(self)
        o.readAllAppCurves(fhandle)
        return o
    self.approachcurves = zeros(...
        size(self.zdata_grid,1),...
        size(self.zdata_grid,2)); 
    
    #Commented out to make IDE happy
    # Loop through all data points
    #for i = 1:length(self.zdata_lin)
       # [y,x] = ind2sub(size(self.zdata_grid), i);
        #fname = fhandle(x,y,i);
        #self.approachcurves(y,x) = SICM.SICMAppCurve.FromFile(fname);
    return None

def plotAll(self):
    # Plots the data and the fit, if available
    #Determine how to implement in matplotlib
    #TODO
    plot(self.xdata, self.ydata);
    if ~isempty(self.fitobject)
        hold on;
        m = max([self.fitobject.D+0.001 min(self.xdata)]);
        x = linspace(m, max(self.xdata), 200);
        plot(x,feval(self.fitobject,x),'r--');
        hold off;

function varargout = plot(self, varargin)
def plot(self, returnPlot):
# Plots the data in appCurve
    a = plot(self.xdata, self.ydata, varargin{:});
    if nargout > 1
        varargout{1} = a;
    #TODO determine how best to plot
    end
    

function varargout = normalizeData(self, varargin)
def normalizeData(self,normalize, newObject=False, n=None):
# Normalize the y-data
#
# If no argument is specified, the mean of last 10# of the data points is
# used to normalize the data. Note that since this class assumes that the
# change in conductance occurs at smaller x-values, the mena is calcultaed
# at the end of the y-data

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.normalizeData(varargin{:}); #Determine best way to communicate
        return o
    if n == None:
        n = np.round(self.ydata.size()/10)
    m = np.mean(self.ydata[end-n:end])
    self.ydata = self.ydata/m #Should be element-wise with numpy

def isVCMode(self):
# returns whether the mode of the approach curve is VC
    return self.mode == SICM.SICMAppCurve.modes.VC

def isINC(self):
# returns whether the direction of the approach curve is INC

    return self.direction == SICM.SICMAppCurve.directions.INC

def isDEC(self):
# returns whether the direction of the approach curve is DEC

    return self.direction == SICM.SICMAppCurve.directions.DEC

def isCCMode(self):
# returns whether the mode of the approach curve is CC

    return self.mode == SICM.SICMAppCurve.modes.CC

def inverseData(self, newObject=False):
# Inverse the y-data: Data becomes 1/data
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.inverseData();
        return 0    
    self.ydata = 1/self.ydata
    return None

def gui(self, newObject=False):
# Opens the ApproachCurve GUI
#
# Examples:
#    obj.gui();
#
#      Opens the GUI
#
#   handle = obj.gui();
#
#      Returns a handle to the GUI
    h = SICMApps.AppCurveApp.AppCurveApp(self);
    if newObject:
        return h
    return None

function [I0, C, D] = guessStartPoint(self)
def guessStartPoint(self):
# This function guesses the start points for a fit and returns them. Note
# that this function only guesses the start points for the functions
# provided by guessFitFunc(), for fit functions set manually you should
# provide the start points etc by passing them to the function fit.
#
# See also FIT, GUESSFITFUNC

    if self.direction == SICM.SICMAppCurve.directions.DEC:
        D = min(self.xdata) - .1;
        if self.xdata[-1] > self.xdata[-1]:
            I0 = mean(self.ydata[0:10])
        else:
            I0 = mean(self.ydata[-11:-1])#Potentially -10, check
        end
    else:
        D = max(self.xdata) + .1
        if self.xdata[-1] > self.xdata[-1]:
            I0 = mean(self.xdata[-11:-1]) #Potentially -10, see above
        else:
            I0 = mean(self.xdata[1:10])
    C = 0.01
    return [IO, C, D]

function varargout = guessMode(self, varargin)
def guessMode(self, newObject=False):
# This function tries to guess whether the AppCurve was recorded in VC or
# CC mode.
    
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.guessMode(varargin{:})
        return o
    force_overwrite = self.returnValIfVarArgEmpty_(0, varargin{:});

    if force_overwrite == 0 and not isnan(self.mode):
        warning('SICMAppCurve:ModeNotEmpty',...
            'This AppCurve object already has a mode. I will keep that.');
        return None
    
    avg = mean(self.ydata);
    if abs(min(self.ydata)-avg) > abs(max(self.ydata) - avg):
        self.setMode(SICM.SICMAppCurve.modes.VC);
    else:
        self.setMode(SICM.SICMAppCurve.modes.CC);
    return None
    ## old check, not very reliable    
    #     p25 = prctile(self.ydata, 25);
    #     p75 = prctile(self.ydata, 75);
    #     
    #     iqr = p75-p25;
    #     outl_low = self.ydata(self.ydata < p25-1.5*iqr);
    #     outl_high = self.ydata(self.ydata > p75+1.5*iqr);
    #     
    #     if length(outl_low) == length(outl_high)
    #         warning('SICMAppCurve:CannotGuessMode',...
    #             'I cannot find a proper mode for this curve');
    #     elseif length(outl_low) > length(outl_high)
    #         # Looks like the curve values decrease, hence ydata contains
    #         # the current. 
    #         self.setMode(SICM.SICMAppCurve.modes.VC);
    #     else
    #         self.setMode(SICM.SICMAppCurve.modes.CC);
    #     end


function varargout = guessFitFunc(self, varargin)
def guessFitFunc(self, newObject=False):
# This function tries to guess whether the AppCurve was recorded with
# increasing or decreasing x-values.
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self)
        o.guessFitFunc(varargin{:})
        return o    
    force_overwrite = self.returnValIfVarArgEmpty_(0, varargin{:});
    if force_overwrite == 0 and not isempty(self.fitfunc):
        warning('SICMAppCurve:FitFuncNotEmpty',...
            'This AppCurve object already has a fit function. I will keep that.');
        return None
    end
    
    if isnan(self.direction):
        self.guessDirection();
    
    # For VC and DEC
    if self.mode == SICM.SICMAppCurve.modes.VC ...
            && self.direction == SICM.SICMAppCurve.directions.DEC
        self.setFitFunc(@(I0,C,D,x)(...
            I0 .* (1 + C ./ (x - D) ).^-1 ...
            ));
        self.setInverseFitFunc(@(I0,C,D,I)(...
            D - C ./ ((I./I0) - 1)...
            ));
    end
    # For VC and INC
    if self.mode == SICM.SICMAppCurve.modes.VC ...
            && self.direction == SICM.SICMAppCurve.directions.INC
        self.setFitFunc(@(I0,C,D,x)(...
            I0 .* (1 + C ./ (D - x) ).^-1 ...
            ));
    end
    # For CC and DEC
    if self.mode == SICM.SICMAppCurve.modes.CC ...
            && self.direction == SICM.SICMAppCurve.directions.INC
        self.setFitFunc(@(U0,C,D,x)(...
            U0 .* (1 + C ./ (x - D) ) ...
            ));
    end
    # For CC and INC
    if self.mode == SICM.SICMAppCurve.modes.CC ...
            && self.direction == SICM.SICMAppCurve.directions.INC
        self.setFitFunc(@(U0,C,D,x)(...
            U0 .* (1 + C ./ (D - x) ) ...
            ));
    end
end

function varargout = guessDirection(self, varargin)
# This function tries to guess whether the AppCurve was recorded with
# increasing or decreasing x-values.
    if nargout == 1
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.guessDirection(varargin{:});
        varargout{1} = o;
        return;
    end
    
    force_overwrite = self.returnValIfVarArgEmpty_(0, varargin{:});
    
    if force_overwrite == 0 && ~isnan(self.direction)
        warning('SICMAppCurve:DirectionNotEmpty',...
            'This AppCurve object already has a direction. I will keep that.');
        return
    end
    
    if isnan(self.mode)
        warning('SICMAppCurve:MissingInformation',...
            'This AppCurve object has not yet a mode. Trying to guess it.');
        self.guessMode();
    end
    if isnan(self.mode)
        error('SICMAppCurve:MissingInformation',...
            'This AppCurve object has no mode. Giving up.');
    end
    
    if self.mode == SICM.SICMAppCurve.modes.VC
        local_guessDirectionForVC(self)
    else
        local_guessDirectionForCC(self)
    end
end

# These functions are still quite ugly...

def local_guessDirectionForVC(obj):
    [mlow, mhigh, x0, xend] = local_getMeansAndExtremes(obj);
    if mlow < mhigh:
        if x0 < xend:
            obj.setDirection(SICM.SICMAppCurve.directions.DEC);
        else:
            obj.setDirection(SICM.SICMAppCurve.directions.INC);
        end
    else:
        if x0 < xend:
            obj.setDirection(SICM.SICMAppCurve.directions.INC);
        else:
            obj.setDirection(SICM.SICMAppCurve.directions.DEC);

def local_guessDirectionForCC(obj):
    [mlow, mhigh, x0, xend] = local_getMeansAndExtremes(obj);
    if mlow > mhigh:
        if x0 < xend:
            obj.setDirection(SICM.SICMAppCurve.directions.DEC);
        else:
            obj.setDirection(SICM.SICMAppCurve.directions.INC);
    else:
        if x0 < xend:
            obj.setDirection(SICM.SICMAppCurve.directions.INC);
        else:
            obj.setDirection(SICM.SICMAppCurve.directions.DEC);


def local_getMeansAndExtremes(obj):
    mlow = mean(obj.ydata[:10])
    mhigh = mean(obj.ydata[-11:-1])
    x0 = obj.xdata(1)
    xend = obj.xdata(end)
    return [mlow, mhigh, x0,xend]


#TODO determine what the varargin are for these
def guessCurveType(self, varargin, newObject=False):
# 
#
# This function tries to ananlyze the data and to find out whether the
# curve was recorded in CC or VC mode and whether the chnage in conductance
# occurs at smaller x-values or larger x-values.
    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.guessCurveType(varargin{:});
        return o
    self.guessMode(varargin{:});
    self.guessDirection(varargin{:});
    self.guessFitFunc(varargin{:});
    return None


def FromXYData(self, x,y):
# Returns a SCIMAppCurve object with the x and y data as provided by the
# two input arguments.

    o = SICM.SICMAppCurve;
    o.xdata = x;
    o.ydata = y;
    return o
    #NOT ORIGINALLY PART OF CLASS


def fromSICMAppCurve_(self, obj):
# internal static function used to copy an SICMAppCurve object
    o = obj.copy();
    return o
    #Consider more traditional copy method
    #def __copy__(self):
    #clone = copy.deepcopy(self)
    #clone._b = some_op(clone._b)
    #return clone
    

def FromFile(varargin, filename = None): 

# Reads data from a file into a SICMAppCurve object
#
#    To allow importing different types of data, this functions
#    uses different importer functions. They are stored in the
#    constant importer property of the SICMScan class.
#
#    Examples:
#      obj = SICMAppCurve.FromFile
#
#      Opens a file dialog and reads the selected file in an
#      SICMSAppCurve object.
#
#      obj = SICMAppCurve.Fromfile(filename)
#      Reads the file `filename` into a SICMScan object
#
#    See also IMPORTER

    tmp = SICM.SICMAppCurve();
    if filename == None:
        [finame, pname] = tmp.getFilename_()
        if finame == 0:
            return o
        filename = fullfile(pname, finame)
    o = tmp.getObjectFromFilename_(filename);
    delete(tmp);
    return o

def frequencyPlot(self):
    if self.SamplingRate: #Better way to check for NaN/default values?
        dFrq = self.SamplingRate / length(self.ydata)
        #freq = 0 : dFrq : self.SamplingRate/2;
        freq = np.arange(0,dFrq,by=self.SamplingRate/2)
    else:
        #freq = 0 : floor(length(self.ydata)/2)+1;
        freq = np.arange(0,floor(length(self.ydata)/2)+1)
    #TODO
    Y = fft(self.ydata) #Determine equivalent python function
    p = semilogx(freq, abs(Y(1:length(freq)))); #Determine equivalent for matplotlib
    return p

def fitToThreshold(self, T, newObject=False):
# Performs an fit optimized to find a z.value at a certain threshold.

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.fitToThreshold(T);
        return o
    
    if isempty(self.fitfunc): #Determine what fitfunc is and most appropriate function to check this
        self.guessFitFunc()
    if isempty(self.fitobject): #See above
        self.fit();
    C = self.fitobject.C;
    I0 = self.fitobject.I0;
    D = self.fitobject.D;
    
    # To detect infinite loops, we need to keep all old values of zT:
    
    l_old = []; # It will grow inside a loop since I do not know how many attempts will be made
    I0_old = []; # It will grow inside a loop since I do not know how many attempts will be made
    C_old = []; # It will grow inside a loop since I do not know how many attempts will be made
    D_old = []; # It will grow inside a loop since I do not know how many attempts will be made
    
    zT = self.inversefitfunc(I0, C, D, T*I0);
    #xstep = min(abs(diff(self.xdata)));
    zT_old = [];
    errors = 0;

    while isempty(zT_old) ...
            || abs(zT_old(end)-zT) > 0.001
        
        [x,y]= local_getXandYuntilThreshold(self, zT);
        
        # Check whether we might enter an infinite loop...
        l = length(x);
        idx = find (l_old == l);
        if ~isempty(find(abs(I0_old(idx) - I0)<.99*I0,1))...
            && ~isempty(find(abs(C_old(idx) - C)<.99*C,1))...
            && ~isempty(find(abs(D_old(idx) - D)<.99*D,1))
            warning('SICMAppCurve:InfiniteLoopDetected',...
                'Fitting is likely to enter an infinite loop. Stopping after #g attempts.', length(l_old));
            self.fitproblems=1;
            
            break;
        
        if length(x) < 3:
            if errors == 0:
                if self.isVCMode():
                    idx = find(self.ydata > T * I0_old(end));
                else:
                    idx = find(self.ydata < T * I0_old(end));
                end
                x = self.xdata(idx);
                y = self.ydata(idx);
                l = length(x);
                plot(x,y);
                errors = 1; 
            else:
                self.fitproblems=1;
                error('SICMAppCurve:NotEnoughDataPointsForFit',...
                    'Sorry, I cannot fit this data automatically.');
            end
        end
        l_old(end+1) = l;##ok<AGROW>
        if self.isDEC()
            w = abs(y - T * I0);
            w = 1 - (w / max(w));
            fo = fit(x,y,self.fitfunc, 'Start', [I0, C, D], 'Lower',[I0*.5 1e-6 D-5], 'Upper', [I0*2, 1, min(x)+1e-6;],'Weights', w);
        else
            fo = fit(x,y,self.fitfunc, 'Start', [I0, C, D], 'Upper',[I0*2 1 D+5], 'Lower', [I0*.5, 1e-6, max(x)+1e-6], 'Weights', w);
        end
        
        I0_old(end+1) = I0; ##ok<AGROW>
        I0 = fo.I0;
        C_old(end+1) = C; ##ok<AGROW>
        C = fo.C;
        
        D_old(end+1) = D; ##ok<AGROW>
        D = fo.D;
        zT_old = zT;  
        zT = self.inversefitfunc(I0, C, D, T*I0);
    
    self.fitobject = fo;  
    return None
    
def local_getXandYuntilThreshold(obj, zT):
    if obj.isDEC():
        ind = find(obj.xdata >= zT);
        x = obj.xdata(ind);
        y = obj.ydata(ind);
        return [x,y]
    end
    if obj.isINC()
        ind = find(obj.xdata <= zT);
        x = obj.xdata(ind);
        y = obj.ydata(ind);
        return [x,y]
    end
    error('SICMAPPCurve:DirectionNotSet',...
        'The direction of the approach curve is not known.');
    return [x,y]
end
    

def fittool(self):
# Opens the approach curve in the fit tool
    cftool(self.xdata, self.ydata)

def fitIsOk(self):
# This function can be used to manually say that a fit is ok, setting the
# fitporblems property to 0
    self.fitproblems = 0;

def fit(self, newObject=False,argArr=False):
# Fit the function provided by setFitFunc to the data
#
# See also SETFITFUNC

    if newObject:
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.fit(argArr) #As else, implement change
        return o

    others = {}; 
    
    [I0, C, D] = self.guessStartPoint();
    start = [I0, C, D];
    lower = [I0 - .5 * I0 , 0, D/100];
    upper = [I0 * 2, Inf D*100];
    if self.direction == SICM.SICMAppCurve.directions.DEC:
        upper(3) = min(self.xdata) - 10 *eps;
        lower(3) = D - 3;
    else:
        upper(3) = D + 3;
        lower(3) = max(self.xdata) + 10 *eps;
    while len(argArr)>0: #Change to dictionary?
        switch varargin{1}
            case 'Start'
                start = varargin{2};
                varargin(1:2)=[];

            case 'Upper'
                upper = varargin{2};
                varargin(1:2)=[];

            case 'Lower'
                lower = varargin{2};
                varargin(1:2)=[];

            otherwise
                others{end+1} = varargin{1}; ##ok<AGROW> # I do not know better...
            if argArr[0] == 'Start':
            
            else if argArr[0] == 'Upper':

            else if argArr[0] == 'Lower':

            else:



    self.fitobject = fit(self.xdata, self.ydata, self.fitfunc,
        'Start', start,
        'Lower', lower,
        'Upper', upper,
        others{:})
    return None

function varargout = filter(self, method, varargin)
# This function applies a filter to the Approach curve data. The syntax is:
# 
#   obj.filter(methods, params);
#
# which applies the filter in `method` with parameters `params` to the
# data. To receive a new object instead of modyfying the origina lone, use 
#
#   newobj = obj.filter(methods, params);
#
# The following filter methods and params are available:
#
#   method       params     description 
#
#   'median'  :   /width/    Applies a median filter to the data with the 
#                            speecified /width/
#   'mean'    :   /width/    Applies a mean filter to the data with the 
#                            specified /width/
#   'highpass':   /freq/     Applies a sharp highpass filter cutting
#                            frequencies below /freq/
#   'lowpass':    /freq/     Applies a sharp lowpass filter cutting
#                            frequencies above /freq/
#   'bandpass':   /freq/, /freq2/     
#                            Applies a sharp bandpass filter cutting
#                            frequencies below /freq/ and above /freq2/
    if nargout == 1
        o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
        o.filter(method, varargin{:});
        varargout{1} = o;
        return;
    end
    
    switch method
        case 'median'
            [self.xdata, ...
             self.ydata] = local_filterMedian(self, varargin{:});
        case 'mean'
            [self.xdata, ...
             self.ydata] = local_filterMean(self, varargin{:});
        case 'lowpass'
            [self.xdata, ...
             self.ydata] = local_filter_bandpass(self, varargin{:});
        case 'highpass'
            [self.xdata, ...
             self.ydata] = local_filter_bandpass(self, 0, varargin{:}); 
        case 'bandpass'
            [self.xdata, ...
             self.ydata] = local_filter_bandpass(self, varargin{:});
        otherwise
            error('SICMAPPCurve:UnknownFilterMethod',...
                'The filter method #s is not implemeted', method);
    end
end

function [x,y] = local_filterMedian(obj, varargin)
    width = round(varargin{1});
    if mod(width, 2) ~= 1
        width = width + 1;
        warning('SICMAppCurve:filterWidthAdjusted',...
            'Filter width must be odd, adjusted to #s', width);
    end
    offset = floor(width/2);
    x = obj.xdata(offset+1:end-offset);
    y = zeros(length(obj.ydata) - 2* offset, 1);
    for i = 1:length(obj.ydata) - width
        y(i) = median(obj.ydata(i:i+width));
    end
    
end
function [x,y] = local_filterMean(obj, varargin)
    width = round(varargin{1});
    if mod(width, 2) ~= 1
        width = width + 1;
        warning('SICMAppCurve:filterWidthAdjusted',...
            'Filter width must be odd, adjusted to #s', width);
    end
    offset = floor(width/2);
    x = obj.xdata(offset+1:end-offset);
    y = zeros(length(obj.ydata) - 2* offset, 1);
    
    for i = 1:length(obj.ydata) - width
        y(i) = mean(obj.ydata(i:i+width));
    end
end

function [x,y] = local_filter_bandpass(obj, varargin)
    try
        sr = obj.SamplingRate;
    catch
        error('SICMAppCurve:filter',...
            'To apply a (high|low|band)pass filter, the object requires a samling rate');
    end
    if isnan(sr)
        error('SICMAppCurve:filter',...
            'To apply a (high|low|band)pass filter, the object requires a samling rate');
    end
    high = inf;
    low = varargin{1};
    if nargin > 2
        high = varargin{2};
    end
    
    if high < low 
        tmp = low;
        low = high;
        high = tmp;
    end
    
    Y = fft(obj.ydata);
    
    
    #real_part = Y(1:floor(length(obj.ydata)/2)+1);
    dFrq = sr / length(obj.ydata);
    freq = 0 : dFrq :sr/2;

    # semilogx(freq, abs(real_part));

    fl_half = freq < low | freq > high;
    
    if low > 0 && high < Inf
        fl_half = ~fl_half;
    end
    fl = zeros(size(Y));
    off = 0
    if length(Y) < 2*length(fl_half)
        off = 1
    end
    fl(1:length(fl_half)) = fl_half;
    size(fl(length(fl_half)+1:end))
    size((fl_half(end-off:-1:1))')
    fl(length(fl_half)+1:end,1) = (fl_half(end-off:-1:1))'; #Make sure to transpose
    #figure;
    #plot(fl);
    #title('Filter')
    #figure;
    #plot(abs(Y(2:end-1)).*fl(2:end-1) );
    #title('Filtered spektrum');
    ny = real(ifft(Y.*fl));
    #figure;
    #plot(obj.xdata, ny);
    #title('Filtered data');
    x = obj.xdata;
    y = ny;
end


function varargout = autoDetectSamplingRate( self, varargin )
    if nargout == 1
       o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
       o.autoDetectSamplingRate( varargin{:} );
       varargout{1} = o;
       return;
    end
     
    Y = fft(self.ydata);
    
    real_part = abs(Y(1:floor(length(self.ydata)/2)+1));
    idx = find(real_part == max(real_part(2:end)))-1;
    f = 50;
    if nargin > 1
        f = varargin{1};
    end
    # fprintf('The maximum peak in frequency is in bin #g, maybe the sampling frequency was #g\n', idx, 2*f*(length(real_part)-1)/idx);
    self.setSamplingRate(2*f*(length(real_part)-1)/idx);
    
end

function varargout = addInfo( self, info, value)
    if nargout == 1
       o = SICM.SICMAppCurve.fromSICMAppCurve_(self);
       o.addInfo( info, value );
       varargout{1} = o;
       return;
    end
    
    self.info.(info) = value;
    
end