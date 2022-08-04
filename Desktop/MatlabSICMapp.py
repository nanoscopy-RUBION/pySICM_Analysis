% Finally, the x-est attempt to have a GUI for SICM data processing
%
% Requires Matlab 2020b due to the use of the
% matlab.ui.componentcontainer.ComponentContainer in the single display
% components.

classdef SICMapp < phutils.gui.R2020b.App
    properties
        % This is the data structure for the app

        % The app can hold multiple scans
        Scans = {}

        % One or more might be currently selected (index)
        SelectedIndex = []
        
        
    end
    properties % (Hidden)
        ImportMenu matlab.ui.container.Menu
        ImportMenuImport matlab.ui.container.Menu
        ImportMenuImportMultiple matlab.ui.container.Menu
        
        AboutMenu matlab.ui.container.Menu
        
        Selector sicmapp.gui.SICMDataSelector
        Display sicmapp.gui.SICMDataDisplay
        MainGrid matlab.ui.container.GridLayout
        
        
    end
    properties (Constant)
        AppName = 'SICM Data Analysis'
        AppVersionMajor = 0
        AppVersionMinor = 1
        
    end
    properties (Constant, Hidden)
        DefaultFileName = 'New File'
        FileExtension = '.sicmapp.mat'
        AboutMessage = 'App: %s\nVersion%g.%g\n\nLicense: GPL 3.0 (see https://github.com/RUBION-Nanoscopy/SICM-toolbox/blob/master/LICENSE)\nSome icons taken from Bootstrap, licensed under a MIT license (https://github.com/twbs/icons/blob/main/LICENSE.md)';
    end
    methods
        function self = SICMapp(varargin)
            SICMapp.version_check();
            self.setup();
            
            self.Figure.Visible = 'on';
        end
    end
    
    methods (Static)
        function version_check()
            % Check for Matlab R2020b (or later)
            v = version('-release');
            vnumber = str2double(v(1:4));
            vletter = v(5);
            if vnumber < 2020 || (vnumber == 2020 && ~strcmp(vletter, 'b'))
                error('SICMapp:VersionMismatch', ...
                    'The SICMapp requires Matlab R2020b or later.');
            end
        end
    end
    methods (Access = protected)
        function setup(self)
            setup@phutils.gui.R2020b.App(self);
            self.Grid.ColumnWidth = {'1x'};
            self.Grid.RowHeight = {'1x', 32}; % last row is the status bar
            self.Grid.Padding = 0;
            self.Grid.RowSpacing = 3;

            % Split upper part into two columns with ratio 1:3
            self.MainGrid = uigridlayout(self.Grid, [1,2], ...
                'ColumnWidth', {'1x','3x'});
            
            self.Selector = sicmapp.gui.SICMDataSelector(self.MainGrid, ...
                'ValueChangedFcn', @(~,~)self.update(), ...
                'ScansChangedFcn', @self.scans_changed ...
            );
            self.Display = sicmapp.gui.SICMDataDisplay(self.MainGrid, ...
                'MenuChangedFcn', @self.on_menu_changed, ...
                'SICMScanInterface', SICM.SICMScan().getInterfaceInformation());
            
            
            self.ImportMenu = uimenu(self.Figure, 'Text', 'Import');
            self.ImportMenuImport = uimenu(self.ImportMenu, 'Text', 'Import single file', ...
                'MenuSelectedFcn', @self.importmenu_on_import);
            self.ImportMenuImportMultiple = uimenu(self.ImportMenu, 'Text', 'Import multiple files', ...
                'MenuSelectedFcn', @self.importmenu_on_importmult);
            
            % Menu functionality (functions are at the end)
            
            self.FileMenuOpen.MenuSelectedFcn = @self.filemenu_on_open;
            self.FileMenuNew.MenuSelectedFcn = @self.filemenu_on_new;
            self.FileMenuClose.MenuSelectedFcn = @self.filemneu_on_close;
            self.FileMenuSave.MenuSelectedFcn = @self.filemenu_on_save;
            self.FileMenuSaveAs.MenuSelectedFcn = @self.filemenu_on_save_as;
            
            self.AboutMenu = uimenu(self.Figure, 'Text', 'About', ...
                'MenuSelectedFcn', @self.show_alert);
            % Make a new file
            self.new();
        end
        
        function update(self, varargin)
            self.Selector.Scans = self.Scans;
            if ~isempty(self.Selector.Value)
                self.Display.Value = self.Selector.Value;
            end
        end
        
        function close(self)
            % closes the app
            close@phutils.gui.R2020b.App(self);
            self.delete();  
        end
        
        function new(self)
            % starts a new file 
            self.Scans = {};
            self.SelectedIndex = [];
            self.FileName = sprintf('%s%s', self.DefaultFileName, self.FileExtension);
            % An empty file is not dirty
            self.IsDirty = false;
            % But it has a default file name
            self.IsAutomaticFilename = true;
        end
        
        function save(self)
            % Saves to the current filename
            scans = self.Scans;
            selectedIndex = self.SelectedIndex;
            save(self.FileName, 'scans', 'selectedIndex');
            self.IsDirty = false;
            % Even if the file name has not been changed, it is not the
            % automatic one anymore
            self.IsAutomaticFilename = false;
        end
        function open(self)
            % opens the file from self.FileName
            loaded = load(self.FileName);
            self.Scans = loaded.scans;
            self.SelectedIndex = loaded.selectedIndex;
            self.IsDirty = false;
            self.IsAutomaticFilename = false;
            self.update();
        end
        
        function import(self, fname)
            imported = SICM.SICMScan.FromFile(fname);
            self.Scans{end+1} = imported;
            self.IsDirty = true;
            self.update();
        end
        
        function closeFile(self)
            % closes a file (not the App)
            if self.IsDirty
                
            end
                
        end
        
        
        function fname = getFilename(self, mustExist, title, varargin)
            % gets a filename from a dialog
            directory = self.getSetting('LastDirectory', pwd());
            if mustExist
                [f,p] = uigetfile(...
                    {sprintf('*%s', self.FileExtension), sprintf("%s-Files", self.AppName)}, ...
                    title, directory ...
                );
            else
                if numel(varargin) > 0
                    directory = [directory filesep varargin{1}];
                end
                [f,p] = uiputfile(...
                    {sprintf('*%s', self.FileExtension), sprintf("%s-Files", self.AppName)}, ...
                    title, directory ...
                );
            end
            if ~isequal(f, 0)
                self.setSetting('LastDirectory', p);
                % @TODO: check for correct file ext, sometimes a bit strange in
                % linux systems, maybe due to the two dots
                
                fname = [p filesep f];
            else
                fname = false;
            end
            figure(self.Figure);
        end
        
        % GUI callbacks
        function scans_changed(self, source, data)
            self.IsDirty = true;
            if data.NeedsRedraw
                self.update();
            end
            
        end
        
        function on_menu_changed(self, obj, varargin)
            % re-order the menu
            % This is ugly, but works
            self.AboutMenu.Parent = self.FileMenu;
            self.AboutMenu.Parent = self.Figure;
        end
        % Menu callbacks
        function filemenu_on_close(self, menu, data)
        end
        function filemenu_on_new(self, menu, data)
            self.new();
        end
        function filemenu_on_open(self, menu, data) 
            f = self.getFilename(true, 'Select a File name');
            if f
                self.FileName = f;
                self.open();
            end
        end
        function filemenu_on_save_as(self, menu, data)
            f = self.getFilename(false, 'Select a File name');
            if f
                self.FileName = f;
                self.save();
            end
        end
        function filemenu_on_save(self, menu, data)
            if self.IsAutomaticFilename
                f = self.getFilename(false, 'Select a File name', self.FileName);
                if f
                    self.FileName = f;
                    self.save();
                end
            else
                self.save();
            end
            
        end
        
        function importmenu_on_import(self, menu, data)
            directory = self.getSetting('LastImportDir', pwd());
            [f,p] = uigetfile(...
                    {'*.sicm', "SICM recordings"}, ...
                    'Select sicm recording', directory ...
                );  
            figure(self.Figure);
            if ~isequal(f, 0)
                self.setSetting('LastImportDir', p);
                self.import([p f]);
            end
        end
        function importmenu_on_importmult(self, menu, data)
            
        end
        
        function show_alert(self, ~, ~)
            uialert(self.Figure, sprintf(self.AboutMessage, self.AppName, self.AppVersionMajor, self.AppVersionMinor), 'About', 'Icon', 'Info');
        end
    end
end