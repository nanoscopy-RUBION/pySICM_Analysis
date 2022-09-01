"""
A module implementing undo/redo functionality

TODO:
undo/redo manager
undoable objects which contain the current state

"""
import copy

'''
NOT USED
AT THE MOMENT A DECORATOR DECLARED IN Controller.py IS USED
def undoable_action(func):
    """This wrapper can be used to make data manipulating actions
    undo/redoable by storing the current state of the data before
    and after the function call."""

    def wrap(*args, **kwargs):
        return func(*args, **kwargs)
    return wrap
'''

class UndoRedoData:
    """This is a simple class to hold information for
    undo and redo actions. This implementatino of undo/redo
    needs two data objects: one before an action has manipulated that data
    and one after the manipulation.

    It stores a string describing the performed action and a deepcopy the data
    before manipulation. Although a deepcopy might be overkill for the current
    implementation, for future extensions it might be necessary.

    Before restoring, data should be validated because depending on the type of measurement
    the data object contains x, y, and z data, or only x and z.

    :param name: a name describing the performed action
    :param data: a 2- or 3-tuple containing the data"""
    def __init__(self, name: str, data: tuple):
        self.name = name
        self.undodata = copy.deepcopy(data)
        self.redodata = tuple()

    def has_redoable(self):
        """Return true if redo data exists."""
        return len(self.redodata) > 0
