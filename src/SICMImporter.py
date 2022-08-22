import tarfile as tf
import numpy as np
import tkinter as tk
from tkinter import filedialog

#class importer:
# Helper class that provides a simple data import interface. Inherit your
# classes from this class.
#
class importer:
        importers = {}
        def getFilename():
            filter = {}
            l = len(SICM.SICMScan.importers)
            for i in np.arange(1,l):
                filter = [filter[:], SICM.SICMScan.importers[i].exts, SICM.SICMScan.importers[i].expl]
                #[fname, pname] = uigetfile(filter,...
                #'Pick a file');
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
            return [fname, pname]

        # Internal function
        #    This function displays a file selector according to
        #    the filetypes that can be imported
        #
        #    See also IMPORTERS

'''
classdef importer
# Helper class that provides a simple data import interface. Inherit your
# classes from this class.
#
     properties (Constant, Hidden)
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
        #   A fundtion handle pointing to a funtion that reads the data.
        #   The function should have one input argument, the filename, and
        #   return an SICMScan object
        #
        # See also UIGETFILE, STRCMP, FUNCTIONS
        importers = {};
     end
     methods (Static)
         function [fname, pname] = getFilename_()
         # Internal function
         #    This function displays a file selector according to
         #    the filetypes that can be imported
         #
         #    See also IMPORTERS
            filter = {};
            l = length(SICM.SICMScan.importers);
            for i = 1:l
                filter = {filter{:}; SICM.SICMScan.importers{i}.exts, ...
                SICM.SICMScan.importers{i}.expl};
            end
                [fname, pname] = uigetfile(filter,...
                'Pick a file');
         end
    end
end'''

class importer:
# Helper class that provides a simple data import interface. Inherit your
# classes from this class.
#
     properties (Constant, Hidden)
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
        #   A fundtion handle pointing to a funtion that reads the data.
        #   The function should have one input argument, the filename, and
        #   return an SICMScan object
        #
        # See also UIGETFILE, STRCMP, FUNCTIONS
        #importers = {};
     end
     methods 
         function self = importer()
         end
         function [fname, pname] = getFilename_(self) 
         # Internal function
         #    This function displays a file selector according to
         #    the filetypes that can be imported
         #
         #    See also IMPORTERS
            filter = {};
            l = length(self.importers);
            
            for i = 1:l
                filter{i,1} = self.importers{i}.exts;
                filter{i,2} = self.importers{i}.expl;
            end
                [fname, pname] = uigetfile(filter,...
                'Pick a file');
         end
         
         function o = getObjectFromFilename_(self, filename)
            [~, ~, e] = fileparts(filename);
            for i = 1:length(self.importers)
                if sum(strcmp(e, self.importers{i}.extlist)) > 0
                    o = self.importers{i}.handle(filename);
                    return
                end
            end
         end
         def getObjectFromFilename(self, filename):

            return self.importers{}.handle
    end
end

'''
classdef importer < matlab.mixin.Copyable
# Helper class that provides a simple data import interface. Inherit your
# classes from this class.
#
     properties (Constant, Hidden)
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
        #   A fundtion handle pointing to a funtion that reads the data.
        #   The function should have one input argument, the filename, and
        #   return an SICMScan object
        #
        # See also UIGETFILE, STRCMP, FUNCTIONS
        #importers = {};
     end
     methods 
         function self = importer()
         end
         function [fname, pname] = getFilename_(self) 
         # Internal function
         #    This function displays a file selector according to
         #    the filetypes that can be imported
         #
         #    See also IMPORTERS
            filter = {};
            l = length(self.importers);
            
            for i = 1:l
                filter{i,1} = self.importers{i}.exts;
                filter{i,2} = self.importers{i}.expl;
            end
                [fname, pname] = uigetfile(filter,...
                'Pick a file');
         end
         
         function o = getObjectFromFilename_(self, filename)
            [~, ~, e] = fileparts(filename);
            for i = 1:length(self.importers)
                if sum(strcmp(e, self.importers{i}.extlist)) > 0
                    o = self.importers{i}.handle(filename);
                    return
                end
            end
         end
    end
end'''

def readBinarySICMData(fname):
    # Generate temporary dircetory and unpack the data.
    # A sicm-file is a gzipped tar archive. It will be unpacked into a
    # temporary directory.
    [ ~, purefilename, ext ] = fileparts(fname)
    tempdirname = tempname
    gunzip(fname, tempdirname) #Figure out how to best implement in python
    tf.extract()
    untar([tempdirname filesep purefilename], tempdirname)
    #TarFile.extract(member, path='', set_attrs=True, *, numeric_owner=False)
    # information about the size etc. are stored in json format in a file
    # called settings.json
    fid = fopen([tempdirname filesep 'settings.json'])
    cjson = textscan(fid,'#s')
    fclose(fid)
    sjson = cjson{1}{1}
    info = jsondecode(sjson)
    xsize = str2double(info.x_px)
    ysize = str2double(info.y_px)
    
    filelist = dir(tempdirname)
    
    for i=1:size(filelist,1):
        [ ~, purefilename2, ext ] = fileparts(filelist(i).name);
        # HL: measurement data is stored in a Byte file without fileextension
        if isempty(ext) && ~strcmp(purefilename2, purefilename):
            datafile = purefilename2
    fid = fopen([tempdirname filesep datafile])
    img = fread(fid,[ysize,xsize],'uint16')
    fclose(fid)
    # Read additional info, if available
    fid = fopen([tempdirname filesep datafile '.info'])
    cinfo2 = textscan(fid, '#s')
    fclose(fid)
    sinfo2 = [cinfo2[1,:]]
    rmdir(tempdirname, 's')
    
    o = SICM.SICMScan.FromZDataGrid(img);
    o.setXSize(str2double(info.x_Size));
    o.setYSize(str2double(info.y_Size));
    try
        info2 = parse_json(sinfo2);
        o.duration = info2.client_scan_duration;  
    catch
    return o
'''
function o = readBinarySICMData(fname)
   # Generate temporary dircetory and unpack the data.
    # A sicm-file is a gzipped tar archive. It will be unpacked into a
    # temporary directory.
    [ ~, purefilename, ext ] = fileparts(fname);
    tempdirname = tempname;
    gunzip(fname, tempdirname);
    untar([tempdirname filesep purefilename], tempdirname);
    
    # information about the size etc. are stored in json format in a file
    # called settings.json
    fid = fopen([tempdirname filesep 'settings.json']);
    cjson = textscan(fid,'#s');
    fclose(fid);
    sjson = cjson{1}{1};
    info = jsondecode(sjson);
    xsize = str2double(info.x_px);
    ysize = str2double(info.y_px);
    
    filelist = dir(tempdirname);
    
    for i=1:size(filelist,1)
        [ ~, purefilename2, ext ] = fileparts(filelist(i).name);
        # HL: measurement data is stored in a Byte file without fileextension
        if isempty(ext) && ~strcmp(purefilename2, purefilename)
            datafile = purefilename2;
        end
    end
    fid = fopen([tempdirname filesep datafile]);
    img = fread(fid,[ysize,xsize],'uint16');
    fclose(fid);
    # Read additional info, if available
    fid = fopen([tempdirname filesep datafile '.info']);
    cinfo2 = textscan(fid, '#s');
    fclose(fid);
    sinfo2 = [cinfo2{1}{:}];
    rmdir(tempdirname, 's');
    
    o = SICM.SICMScan.FromZDataGrid(img);
    o.setXSize(str2double(info.x_Size));
    o.setYSize(str2double(info.y_Size));
    try
        info2 = parse_json(sinfo2);
        o.duration = info2.client_scan_duration;  
    catch
        
    end
'''