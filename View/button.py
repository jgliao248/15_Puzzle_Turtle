"""
button.py
Contains the button class turtle.Turtle child class.
"""

from turtle import Turtle, Screen, done, update


class Button(Turtle):
    """
    Class: Button
    Description:
    This class is a child class of the turtle.Turtle class
    that automatically sets the shape to a specific game element to the desired location.

    """
    def __init__(self, width, height, x=0, y=0, shape='circle', visible=True):
        """
        Initializes the Button class
        :param width: the width of the button
        :param height: the height of the button
        :param x: the initial x coordinate of the button
        :param y: the initial y coordinate of the button
        :param shape: the shape of the button. Can be a turtle based shape or a gif photo
        :param visible: shows the button if true, hides if false
        """
        super().__init__(shape=shape, visible=visible)
        self.height = height
        self.width = width
        self.speed('fastest')
        self.penup()
        self.goto(x, y)
        update()

        # set the default bound function
        self.funct = lambda: print("Button pressed")

    def get_width(self):
        """
        get_width:
        Returns the width of the current button instance
        :return: the width of the current button instance
        """
        return self.width

    def get_height(self):
        """
        get_height:
        Returns the height of the current button instance
        :return: the height of the current button instance
        """
        return self.height

    def is_clicked(self, x, y):
        """
        is_clicked
        This function will take an x and y coordinate and will return true if
        it is within the rectangular areas of the button
        :param x: The given x coordinate to be checked
        :param y: The given y coordinate to be checked
        :return: True if the x y coordinate is within the rectangle representing the button. False otherwise
        """

        return (self.xcor() - self.width / 2 <= x <= self.xcor() + self.width / 2) and \
            (self.ycor() - self.height / 2 <= y <= self.ycor() + self.height / 2)

    def bind_function(self, funct):
        """
        bind_function
        This function binds a unique function to the button class
        :param funct: the function that is bounded to the instance of the button class
        :return: none
        """
        self.funct = funct

    def __str__(self):
        """
        __str__
        This function returns the string representation of the button class in terms of its current shape and position
        :return: the string representation of the button class in terms of its current shape and position
        """
        return f"{self.shape()} {self.pos()}"


if __name__ == '__main__':
    s = Screen()
    b = Button(50, 50, 100, 100, shape="square")

    def test(x, y):
        print(b.is_clicked(x, y))
    s.onscreenclick(test)
    done()
