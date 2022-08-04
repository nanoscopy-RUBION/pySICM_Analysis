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

def local_flattenPlane(obj):
    x = obj.xdata_lin
    y = obj.ydata_lin
    z = obj.zdata_lin
    [fo, go] = fit([x,y],z,'poly11')
    d = obj.zdata_grid - feval(fo, obj.xdata_grid, obj.ydata_grid)
    p25 = prctile(d(:), 25)
    excludeIdx = find(d(:) > p25)
    [fo, go] = fit([x,y],d(:),'poly11','Exclude',excludeIdx)
    data = d - feval(fo, obj.xdata_grid, obj.ydata_grid)
    return data

function data = local_flattenParaboloid(obj, varargin)
    if nargin == 1
        x = obj.xdata_lin
        y = obj.ydata_lin
        z = obj.zdata_lin
        [fo, go] = fit([x,y],z,'poly22')
        data = obj.zdata_grid - feval(fo, obj.xdata_grid, obj.ydata_grid)

function data = local_flattenLinewise(obj, varargin)
    omit = []
    if nargin == 1
        p = 25
    else
        p = varargin{1}
        if nargin == 4
            omit = varargin{3}

    data = obj.zdata_grid'; #local_flattenPlane(obj);
    sz = size(data)
    ndata = zeros(sz(1), sz(2))
    for y = 1:sz(1)
        l = data(y,:);
        if any(omit==y)
            ndata(y,:) = l;
            continue

        p25 = prctile(l, p);
        eIdx = find(l > p25);
        fo = fit((0:length(l)-1)', l', 'poly1', 'Exclude', eIdx);
        ndata(y,:) = l - (feval(fo,  0: length(l)-1))';
    data = ndata';

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
    data = ndata;

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
    data = ndata;

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

function data = local_flatten_manual(obj)
    app = SICM.SICMScanFlattenApp(obj);
    function local_assign_result(scan)
        data = scan.zdata_grid;
    app.CloseCallback = @local_assign_result;
    waitfor(app.Figure);