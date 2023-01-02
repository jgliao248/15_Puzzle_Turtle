"""
border.py
Contains the Border class, a child class of the Button class.
"""
from View.button import Button


class Border(Button):
    """
    Border
    This class is a child class of the Button class. It still represents a rectangular area within a turtle screen.
    This class represents a bordered area on the turtle screen to isolate content. The center point is the reference.
    It can be created from any corner point as well as the center point. It is able to return these points as well
    """

    def __init__(self, width, height, x=0, y=0):
        """
        Initializes the Border class at (0,0)
        :param width: The width of the Border
        :param height: The height of the Border
        :param x: the center point x coordinate of the Border instance
        :param y: the center point y coordinate of the Border instance
        """
        super().__init__(width, height, x=x, y=y, shape="triangle", visible=False)
        self.center = x, y
        self.pensize(2)
        self.speed("fastest")

    def set_point(self, coordinates, point="top-left") -> None:
        """
        Sets the border to the position is needs to be at based on the given coordinates and which point it represents
        on the rectangular area. It defaults to the top-left of the rectangle
        :param coordinates: the x, y coordinates
        :param point: One of the 5 points of the Border; top-left, top-right, bottom-left, bottom-right, center
        :return: None
        """

        # all calculations are referenced from the center of the represented rectangle that is the border
        half_width = self.width / 2
        half_height = self.height / 2
        match point.lower():
            case "top-left":
                self.center = coordinates[0] + half_width, coordinates[1] - half_height
            case "top-right":
                self.center = coordinates[0] - half_width, coordinates[1] - half_height
            case "bottom-left":
                self.center = coordinates[0] + half_width, coordinates[1] + half_height
            case "bottom-right":
                self.center = coordinates[0] - half_width, coordinates[1] + half_height
            case "center":
                self.center = coordinates
            case _:  # default top left
                self.center = coordinates[0] + half_width, coordinates[1] - half_height

    def get_point(self, point="top-left", x_offset=0, y_offset=0) -> tuple:
        """
        Returns the given point name along with any offsets in the x or y directions. The default is the top-left
        corner with no offsets
        :param point: One of the 5 points of the Border; top-left, top-right, bottom-left, bottom-right, center
        :param x_offset: The x coordinate offset
        :param y_offset: The y coordinate offset
        :return: A tuple containing the resultant coordinates
        """
        # all calculations are referenced from the center of the represented rectangle that is the border
        half_width = self.width / 2
        half_height = self.height / 2

        match point:
            case "top-left":
                return self.center[0] - half_width - x_offset, self.center[1] + half_height + y_offset
            case "top-right":
                return self.center[0] + half_width + x_offset, self.center[1] + half_height + y_offset
            case "bottom-left":
                return self.center[0] - half_width - x_offset, self.center[1] - half_height - y_offset
            case "bottom-right":
                return self.center[0] + half_width + x_offset, self.center[1] - half_height - y_offset
            case "center":
                return self.center
            case _:  # default top left
                return self.center[0] - half_width - x_offset, self.center[1] + half_height + y_offset

    def draw_rectangle(self, color="BLACK", fillcolor=None) -> None:
        """
        This function draws a rectangle with the current x, y position as the center point. The default is a
        rectangle with black borders and no fill
        :param color: The border color; can be a turtle defined color or hex
        :param fillcolor: The fill color; can be a turtle defined color or hex
        :return: None
        """
        self.penup()
        # start at the top left
        self.goto(self.get_point("top-left"))
        self.pendown()
        # check for fill
        if fillcolor is not None:
            self.fillcolor(fillcolor)
            self.begin_fill()
        self.pen(pencolor=color, pensize=5)

        for i in range(4):
            if i % 2 == 0:
                self.forward(self.width)
            else:
                self.forward(self.height)
            self.right(90)

        if fillcolor is not None:
            self.end_fill()

        self.penup()
        # Return turtle object back to the center of the rectangle
        self.goto(*self.center)
