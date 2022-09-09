from sicm_analyzer import sicm_data
import copy

# Constants for data collection value indexing
DATA_UNDO = 0
REDO = 1



class DataManager:
    """
    This class stores all imported SICM data, manages undo/redo functionality for
    individual SICMData objects and handles function calls which manipulate the data.
    If a function is passed as an optional argument this function will be called each
    time data manipulations occur.
    """
    def __init__(self, func=None):
        if func:
            self.listener_function = func
        else:
            self.listener_function = self.__empty_function

        self.data_collection: dict[str, tuple[
                                                list[UndoRedoData],
                                                list[UndoRedoData]]
                                   ] = {}

    def __empty_function(self):
        """This is a placeholder in case no function
        has been passed to the constructor."""
        pass

    def clear_all_data(self):
        self.data_collection.clear()

    # Import and add data
    ####################################################################################################################
    def import_files(self, files):
        """One file or multiple files will be imported."""
        # do some file checks?
        for file in files:
            self._create_data_container_for_file(file=file)

    def _create_data_container_for_file(self, file: str):
        """This function adds data imported from the passed to data collection.
        Data collection is a dictionary in which the absolute file path is
        mapped to a tuple value. This tuple contains the following data at the
        indicated indexes:

        [0] SICMdata: The SICMdata imported from and mapped to file
        [1] list[SICMdata]: This list is handled as a stack and holds copies of the data. The
                            first object are the raw data and should never be manipulated or
                            removed!
        [2] list[SICMdata]: This list is also handled as a stack and stores undone data manipulations.

        Note: SICM data files should always be imported using this function!
        """
        data = UndoRedoData(sicm_data.SICMDataFactory().get_sicm_data(file), "raw_data")
        self.data_collection[file] = ([data], [])



    def get_files_without_duplicates(self, files):
        """Returns a list which only includes files that
        have not already been imported.

        A file is a new file if its full file path is not already
        a dictionary key in views."""
        new_files = []
        for file in files:
            if file not in self.data_collection.keys():
                new_files.append(file)
        return new_files



    # Undo/Redo data manipulations
    ####################################################################################################################
    def undo_manipulation(self, key):
        dataset = self.data_collection.get(key)
        if len(dataset[DATA_UNDO]) > 1:
            data = dataset[DATA_UNDO].pop()
            dataset[REDO].append(data)

    def redo_manipulation(self, key):
        dataset = self.data_collection.get(key)
        data = dataset[REDO].pop()
        dataset[DATA_UNDO].append(data)

    def is_undoable(self, key):
        return len(self.data_collection.get(key)[DATA_UNDO]) > 1

    def is_redoable(self, key):
        return len(self.data_collection.get(key)[REDO]) > 0

    def get_undo_text(self, key):
        try:
            if len(self.data_collection.get(key)[DATA_UNDO]) > 1:
                return self.data_collection.get(key)[DATA_UNDO][-1].name
            return ""
        except IndexError:
            return ""

    def get_redo_text(self, key):
        try:
            return self.data_collection.get(key)[REDO][-1].name
        except IndexError:
            return ""

    def get_undoable_manipulations_list(self, key) -> list[str]:
        """Returns a list with all data manipulations that can be made undone."""
        items = []
        try:
            # The first item in the undo stack contains raw data
            # Therefore, all items but the first should be listed
            for item in self.data_collection.get(key)[DATA_UNDO][1:]:
                items.append(item.name)
        except IndexError:
            pass
        return items

    def _make_undoable_data_copy(self, key, action_name="action"):
        """Creates a new UndoRedoData object and clears the redo stack. The new object
        contains a copy of the top element of the undo stack.
        Since a new operation has been executed on the data, previous redos
        would cause errors. Therefore, the redo stack must be cleared."""
        undo_stack = self.data_collection.get(key)[DATA_UNDO]
        undo_stack.append(UndoRedoData(name=action_name, data=undo_stack[-1].data))
        self.data_collection.get(key)[REDO].clear()

    # Misc
    ####################################################################################################################

    def get_data(self, key) -> sicm_data.SICMdata:
        """Returns a SICMdata object."""
        # This is equivalent to peek on stack. It returns the data of
        # the last object added to the list
        return self.data_collection.get(key)[DATA_UNDO][-1].data

    def reset_manipulations(self, key: str):
        """In this special case of undo/redo actions a copy of
        the first element is stored in an UndoRedoData object. This is
        because the first element contains the raw data."""
        undo_stack = self.data_collection.get(key)[DATA_UNDO]
        raw_data = UndoRedoData(name="Reset data", data=undo_stack[0].data)
        undo_stack.append(raw_data)

    def execute_func_on_current_data(self, func, key:str, action_name: str = "action"):
        """This wrapper function is used to make other functions undo/redoable.
        Wrap the function and pass a name for that action.

        Before calling the function, store_undoable_action will be called to store the
        state of the current view object. After the function call, the readoable state
        will be stored and figures will be updated.

        Example to use the wrapper:
            undo_wrapper_test(function, name="Name for that function")(currentView, args)
        """

        # copy data and put on stack
        # do manipulation on this new data object
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            self.listener_function()

        self._make_undoable_data_copy(key, action_name)

        return wrapper


class UndoRedoData:
    """This is a simple class to hold information for
    undo and redo actions. This implementation of undo/redo
    creates a copy of the underlying data before manipulations should
    be performed.

    It stores a string describing the performed action and a deepcopy the data
    before it is manipulated. Although a deepcopy might be overkill for the current
    implementation, for future extensions it might be necessary.

    :param name: a name describing the performed action
    :param data: SICMdata object
    """
    def __init__(self, data: sicm_data.SICMdata, name: str = ""):
        self.data = copy.deepcopy(data)
        self.name = name
