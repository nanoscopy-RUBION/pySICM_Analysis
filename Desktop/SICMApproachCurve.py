import math
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

function [h, f , g, repeats] =fitApproachCurve(z,U,t,varargin)
def fit_approach_curve(z,U,t,difference=0,varargin):

    # The equation 
    appCurve = fittype('U0*(1+C/(z-h))','independent',{'z'},'Coefficients',{'C','h','U0'});
    
    # Start points and other helpers for the fit funtion
    
    uh = z[-1]
    lh = z[-1]-2
    sh = z[-1]-.5
    
    # These values might be only valid for pipettes used so far... Sharper
    # pipettes might require an adaption
    
    lC = 0.00001
    uC = 0.1
    sC = 0.001
           
    sU0 = np.mean(U[:100]) #Is indexing in MATLAB inclusive? If so, 100. IF not, 99
    lU0 = np.min(U[:100])/2
    uU0 = np.max(U[:100])*2
    
    # Some temporary variables
    
    h_old=math.inf
    h=0
    counter=1
    all_h = np.array([])
    
    # The first fit
    
    [fitres, gfitg]= fit(z, U, appCurve, 'StartPoint',[sC, sh, sU0], 'Lower',[lC, lh, lU0], 'Upper',[uC, uh, uU0]);
    
    while abs(h-h_old) > difference and isempty(find(all_h==h,1))
        h_old = h
        counter=counter+1
            
        h = fitres.C/(t-1) + fitres.h;
        ind = find(z >= h);
        if(h_old ~=h)
            all_h = [all_h h_old];
        [fitres, gfitg]= fit(z(ind), U(ind), appCurve, 'StartPoint',[sC, sh, sU0], 'Lower',[lC, lh, lU0], 'Upper',[uC, uh, uU0]);

    while abs(h-h_old) > difference && isempty(find(all_h==h,1))
        h_old = h;
        counter=counter+1
            
        h = fitres.C/(t-1) + fitres.h;
        ind = find(z >= h);
        if(h_old ~=h)
            all_h = [all_h h_old];
        end
        [fitres, gfitg]= fit(z(ind), U(ind), appCurve, 'StartPoint',[sC, sh, sU0], 'Lower',[lC, lh, lU0], 'Upper',[uC, uh, uU0]);
        #https://www.mathworks.com/help/curvefit/fit.html

    end
    
    f=fitres
    g=gfitg
    if np.sum(np.equal(all_h,h)) == 0:
        repeats = -counter
    else:
        repeats = +counter

    return [h, f, g, repeats]


'''    
    # fitApproachCurve
    #
    # [h, f, g, repeats] = fitApproachCurve(z,U,t)
    # fits the equation U0*(1+C/(z-h)) to the data provided in z and U up
    # to a threshold of U/U0 = t.
    #
    # First, the entire data in z and U is considered. The fit is computed
    # and h, the sample height, is determined. Then only valus of z (and
    # their corresponding U-values) below this value are considered and the
    # fit is computed. Again, h is determined from this data, and the
    # fitting procedure is applied again.
    #
    # This is repeated until two successive determinations yield only a
    # difference in h below 0.0001 (that is .1 nm if data is given in
    # micrometers). Alternatively, the difference can be provided as the
    # optional argument. If a loop occrus, the procedure is halted.
    #
    # The retrun valus are 
    #   h: height of the sample
    #   f: the fit object
    #   g: the goodness of the fit
    #   repeats: the number of iterations. If negative, a loop occured.
    #
    # See also fit
    
    if nargin == 4
        difference = varargin{1};
    else
        difference = 0.0001;
    end
    
    # The equation 
    appCurve = fittype('U0*(1+C/(z-h))','independent',{'z'},'Coefficients',{'C','h','U0'});
    
    # Start points and other helpers for the fit funtion
    
    uh = z(end);
    lh = z(end)-2;
    sh = z(end)-.5;
    
    # These values might be only valid for pipettes used so far... Sharper
    # pipettes might require an adaption
    
    lC = 0.00001;
    uC = 0.1;
    sC = 0.001;
           
    #
    sU0 = mean(U(1:100));
    lU0 = min(U(1:100))/2;
    uU0 = max(U(1:100))*2;
    
    # Some temporary variables
    
    h_old=inf; h=0; counter=1; all_h = [];
    
    # The first fit
    
    [fitres, gfitg]= fit(z, U, appCurve, 'StartPoint',[sC, sh, sU0], 'Lower',[lC, lh, lU0], 'Upper',[uC, uh, uU0]);
    
    while abs(h-h_old) > difference && isempty(find(all_h==h,1))
        h_old = h;
        counter=counter+1;
            
        h = fitres.C/(t-1) + fitres.h;
        ind = find(z >= h);
        if(h_old ~=h)
            all_h = [all_h h_old];
        end
        [fitres, gfitg]= fit(z(ind), U(ind), appCurve, 'StartPoint',[sC, sh, sU0], 'Lower',[lC, lh, lU0], 'Upper',[uC, uh, uU0]);
    end
    
    f=fitres;
    g=gfitg;
    if ~isempty(find(all_h==h,1))
        repeats = -counter;
    else
        repeats = +counter;
    end
    
'''

def appCurveG(z, C, H, G0):
    #Assumes G is a numpy array so this operation is performed elementwise
    #Consider casting to np array for safety?
    return G0*(1 + (C/(z-H))**-1)

'''function g = appCurveG(z, C, H, G0)
#
# SICM.appCurve
#
# Calculates G0.*(1 + (C./(z-H))^-1)
#
# G = SICM.appCurveG(z, C, H, G0)
#
# Calculates the conductances for all values in the vector z and
# the corresponding constants C, H and G0.

g = G0.*(1 + (C./(z-H))^-1);'''

def appCurve(z, h0, d0, U0):
    #Assumes G is a numpy array so this operation is performed elementwise
    #Consider casting to np array for safety?
    return U0*(1 + h0/(z-d0))

'''function u = appCurve(z, h0, d0, U0)
#
# SICM.appCurve
#
# Calculates U0.*(1 + h0./(z-d0))
#
# R = SICM.appCurve(z, h0, d0, U0)
#
# Calculates the voltages for all values in the vector z and
# the corresponding constants h0, d0 and U0.

u = U0.*(1 + h0./(z-d0));'''

def averageFilter(d, l=1):
    y = np.zeros(d.size()[0]-2*l,)
    for i in np.range(l+1,d.size()[0]):
        y[i] = np.mean(d[i-l:i+1]) #May need to be i+2. Test this!


'''function y = averageFilter(d, varargin)
# SICM.averageFilter
#
# Smoothes data by calculating the avarage of adjacent data points for 
# one-dimensional vectors. 
# 
#
# y = SICM.averageFilter(data)
# 
# Substitutes every data point n with the average of n-1, n and n+1. The 
# returned vector has a sized reduced by 2.
# 
# y = SICM.averageFilter(data, l)
#
# Substitutes every data point n with the average of n-l, n-l+1, .., n,
# n+l-1, n+l. The returned vector has a sized reduced by 2l.
#
# See also FSPECIAL, FILTER

l = 1;
if nargin == 2
    l = varargin{1};
end;
y = zeros(length(d)-2*l, 1);
for i = l+1:length(d)-l
    y(i-l) = mean(d(i-l:i+l));
end'''

def appCurveRel(z, h0, d0):
    #Assumes G is a numpy array so this operation is performed elementwise
    #Consider casting to np array for safety?
    return 1 + h0/(z-d0)


'''function R = appCurveRel(z, h0, d0)
# SICM.appCurve
#
# Calculates 1 + h0/(z-d0)
#
# R = SICM.appCurve(z, h0, d0)
#
# Calculates the relative resistance R for all values in the vector z and
# the corresponding constants h0 and d0.

R = 1 + h0./(z-d0);'''

function [r, varargout] = roughness(data, varargin);
#ROUGHNESS - Compute the roughness of the data
#
#    Currently, the following method is used:
#
#    1) Subtract a paraboloid from the data
#    2) Remove outliers
#    3) Compute the RMSE of the data
#
#
#
#    Examples:
#  
#    r = roughness(data)
#    
#      Computes and returns the roughness
#
#
#    [r, outliers_removed] = roughness(data)
#     
#      Computes the roughness and returns the data without outliers.
#      Instead of the outlieres, NaN is inserted
#
#
#    [r, outliers_removed, fo] = roughness(data)
#
#      As above, but additionally returns the  fitobject.
#
#    [r, outliers_removed, fo, go] = roughness(data)
#
#      As above, but additionally returns the goodness of the fit.
#
#    SEE ALSO: SUBTRACTPARABOLOID, MEDIAN, BOXPLOT
def get_roughness(data,pxsz = 1):

[flat, fo, go] = subtractParaboloid(data, pxsz); #Not a standard function. Determine what it is in original code

p75 = np.perctile(flat, 75)
p25 = np.perctile(flat, 25)

upperlimit = p75 + 1.5 * (p75 - p25)
lowerlimit = p25 - 1.5 * (p75 - p25)

no_outliers = flat(flat >= lowerlimit and flat <= upperlimit) #Determine how Matlab performs implicit indexing
#Need numpy arrays for above
r = rmse(no_outliers([:]); #Consider whether to use least squares instead
#r =sqrt(mean_squared_error(y_actual, y_predicted))
tmp = flat
tmp[tmp<lowerlimit or tmp > upperlimit] = np.NaN
return [r,tmp,fo,go]


'''function [r, varargout] = roughness(data, varargin);
#ROUGHNESS - Compute the roughness of the data
#
#    Currently, the following method is used:
#
#    1) Subtract a paraboloid from the data
#    2) Remove outliers
#    3) Compute the RMSE of the data
#
#
#
#    Examples:
#  
#    r = roughness(data)
#    
#      Computes and returns the roughness
#
#
#    [r, outliers_removed] = roughness(data)
#     
#      Computes the roughness and returns the data without outliers.
#      Instead of the outlieres, NaN is inserted
#
#
#    [r, outliers_removed, fo] = roughness(data)
#
#      As above, but additionally returns the  fitobject.
#
#    [r, outliers_removed, fo, go] = roughness(data)
#
#      As above, but additionally returns the goodness of the fit.
#
#    SEE ALSO: SUBTRACTPARABOLOID, MEDIAN, BOXPLOT
pxsz = 1;
if nargin > 1
    pxsz = varargin{1};
end

[flat, fo, go] = subtractParaboloid(data, pxsz);

p75 = prctile(flat(:), 75);
p25 = prctile(flat(:), 25);

# Every data point beyond 1.5 IQRs is an outlier
upperlimit = p75 + 1.5 * (p75 - p25);
lowerlimit = p25 - 1.5 * (p75 - p25);

no_outliers = flat(flat >= lowerlimit & flat <= upperlimit);
r = rmse(no_outliers(:));
if nargout > 1
    tmp = flat;
    tmp(tmp<lowerlimit | tmp > upperlimit) = NaN;
    varargout{1} = tmp;
end
if nargout > 2
    varargout{2} = fo;
end
if nargout > 3
    varargout{3} = go;
end'''




