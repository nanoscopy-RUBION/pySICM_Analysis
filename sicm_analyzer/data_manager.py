from sicm_analyzer import sicm_data
import copy
from typing import Callable

# Constants for data collection value indexing
UNDO_STACK = 0
REDO_STACK = 1


class DataManager:
    """
    This class stores all imported SICM data, manages undo/redo functionality for
    individual SICMData objects and handles function calls which manipulate the data.
    If a function is passed as an optional argument this function will be called each
    time data manipulations occur.

    :param Callable func:
    """
    def __init__(self, func: Callable = None):
        if func:
            self.listener_function = func
        else:
            self.listener_function = self.__empty_function

        self.data_collection: dict[str, tuple[
                                                list[UndoRedoData],
                                                list[UndoRedoData]]
                                   ] = {}
        self.current_data_key: str = ""

    def __empty_function(self):
        """This is a placeholder in case no function
        has been passed to the constructor."""
        pass

    def clear_all_data(self):
        self.data_collection.clear()
        self.current_data_key = ""

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
        [2] list[SICMdata]: This list is also handled as a stack and stores undone data (redoable)
        manipulations.

        Note: SICM data files should always be imported using this function!
        """
        data = UndoRedoData(sicm_data.get_sicm_data(file), "raw_data")
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
        if len(dataset[UNDO_STACK]) > 1:
            data = dataset[UNDO_STACK].pop()
            dataset[REDO_STACK].append(data)

    def redo_manipulation(self, key):
        dataset = self.data_collection.get(key)
        data = dataset[REDO_STACK].pop()
        dataset[UNDO_STACK].append(data)

    def is_undoable(self, key) -> bool:
        """Returns true if actions can be undone."""
        return len(self.data_collection.get(key)[UNDO_STACK]) > 1

    def is_redoable(self, key) -> bool:
        """Returns true if actions can be redone."""
        return len(self.data_collection.get(key)[REDO_STACK]) > 0

    def get_undo_text(self, key) -> str:
        """Returns the action name for the last element on the
        undo stack or an empty string if there is no action to
        be made undone."""
        try:
            if len(self.data_collection.get(key)[UNDO_STACK]) > 1:
                return self.data_collection.get(key)[UNDO_STACK][-1].name
            return ""
        except IndexError:
            return ""

    def get_redo_text(self, key) -> str:
        """Returns the action name for the last element on the
        redo stack or an empty string if there is no action to
        be made redone."""
        try:
            return self.data_collection.get(key)[REDO_STACK][-1].name
        except IndexError:
            return ""

    def get_undoable_manipulations_list(self, key) -> list[str]:
        """Returns a list with all data manipulations names
        that can be made undone.

        If there are no undoable manipulations an empty list
        will be returned."""
        items = []
        try:
            # The first item in the undo stack contains raw data
            # Therefore, all items but the first should be listed
            for item in self.data_collection.get(key)[UNDO_STACK][1:]:
                items.append(item.name)
        except IndexError:
            pass
        except TypeError:
            pass
        return items

    def _make_undoable_data_copy(self, key, action_name="action"):
        """
        Creates a new UndoRedoData object and clears the redo stack.

        The new object contains a copy of the top element of the undo stack.
        Since a new operation has been executed on the data, previous redo
        would cause errors. Therefore, the redo stack must be cleared.
        """
        undo_stack = self.data_collection.get(key)[UNDO_STACK]
        undo_stack.append(UndoRedoData(name=action_name, data=undo_stack[-1].data))
        self.data_collection.get(key)[REDO_STACK].clear()

    # Misc
    ####################################################################################################################
    def get_data(self, key: str) -> sicm_data.SICMdata:
        """
        Returns a SICMdata object.

        This method is equivalent to peek on stack since it returns
        the data of the last object added to the list without removing
        it from the stack.

        :param str key:
        """
        return self.data_collection.get(key)[UNDO_STACK][-1].data

    def reset_manipulations(self, key: str):
        """Clears the list of data manipulations and resets
        the data to the original data.

        In this special case of undo/redo actions a copy of
        the first element is stored in an UndoRedoData object. This is
        because the first element contains the raw data.
        """
        undo_stack = self.data_collection.get(key)[UNDO_STACK]
        raw_data = UndoRedoData(name="Reset data", data=undo_stack[0].data)
        undo_stack.append(raw_data)

    def remove_data(self, key: str):
        """Removes the data from the collection."""
        del self.data_collection[key]

    def execute_func_on_current_data(self, func: Callable, key: str, action_name: str = "action"):
        """This wrapper function is used to make other functions undo/redoable.
        Wrap the function and pass a name for that action.

        Before calling the function, an UndoRedoData object will be created to store a copy
        of the current state of the data object. A listener_function will be called directly
        after the wrapped function.

        Example to use the wrapper:
            execute_func_on_current_data(
                        func=do_something_with_data,
                        key=key_for_data_object,
                        action_name="Name for that action"
            )(args, kwargs)
        """

        # copy data and put on stack
        # do manipulation on this new data object
        def wrapper(*args, **kwargs):
            """This wrapper will call the wrapped function first
            and then the listener_function of the DataManager if exists.
            """
            func(*args, **kwargs)
            self.listener_function()

        self._make_undoable_data_copy(key, action_name)

        return wrapper


class UndoRedoData:
    def __init__(self, data: sicm_data.SICMdata, name: str = ""):
        """
        This is a simple class to hold information for
        undo and redo actions. This implementation of undo/redo
        creates a copy of the underlying data before manipulations should
        be performed.

        It stores a string describing the performed action and a deepcopy the data
        before it is manipulated. Although a deepcopy might be overkill for the current
        implementation, for future extensions it might be necessary.

        :param str name: a name describing the performed action
        :param SICMdata data: SICMdata object
        """
        self.data = copy.deepcopy(data)
        self.name = name
