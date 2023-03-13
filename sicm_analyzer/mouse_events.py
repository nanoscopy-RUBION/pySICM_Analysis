from PyQt6.QtCore import QPoint
import numpy

ROW = "row"
COLUMN = "column"
CROSS = "cross"


class MouseInteraction:
    """A class for storing references to mouse pointer
    coordinates.

    Three mouse events can be bound:
        - button_press_event: triggers when a mouse
        button is pressed (the release is not necessary)
        - motion_notify_event: triggers when moving
        the mouse pointer
        - button_release_event: triggers when a mouse
        button is released

    In args and kwargs optional arguments can be stored
    which can, for example, be used to define conditions
    when a mouse event should be registered.
    """
    def __init__(self, *args, **kwargs):
        self.cid_move = None
        self.cid_press = None
        self.cid_release = None

        self.mouse_point1 = None
        self.mouse_point2 = None
        self.args = args
        self.kwargs = kwargs


# Helper functions
# ______________________________________________________________________________________________________________________
def is_in_range(point: QPoint, array: numpy.ndarray) -> bool:
    """
    Checks if point coordinates are within the array size.

    Note: ndarray.shape[0] is y and [1] is x!
    """
    return 0 <= point.x() <= array.shape[1] - 1 and 0 <= point.y() <= array.shape[0] - 1


def get_coordinate_of_click(event) -> QPoint or None:
    """Returns a QPoint with coordinates of mouse click event or None if the click event
    was not inside the graph.
    """
    if event.inaxes and event.name == "button_press_event":
        return QPoint(int(event.xdata), int(event.ydata))
    else:
        return None


def points_are_not_equal(point1: tuple[int, int], point2: tuple[int, int]) -> bool: #point1: QPoint, point2: QPoint) -> bool:
    """Checks if two points have the same coordinates."""
    return point1 != point2
    #return point1.x() != point2.x() and point1.y() != point2.y()
