"""
This module is for creating and running the different graphics
engines that are available (currently Tkinter, Turtle.py and pygame)
"""

from tkinter import *
import turtle
import pygame


class Board(Frame):
    """
    Abstract superclass that holds the main window/board and canvas setup.
    Also allows multiple engine modules to inherit the constructor setup
    """
    def __init__(self):
        self.board = Tk()
        self.board.title("Interactive Drawing Application")
        Frame.__init__(self, self.board)
        self.canvas_width = 500
        self.canvas_height = 500
        self.start_x = self.canvas_width / 2
        self.start_y = self.canvas_height / 2
        self.canvas = Canvas(self.board, width=self.canvas_width,
                             height=self.canvas_height, bg="white")

    def show_canvas(self):
        pass

    def select_pen(self):
        pass

    def start_draw(self):
        pass

    def draw_line(self):
        pass


class TkinterDrawer(Board):
    """
    Main tkinter class which inherits Board. This allows grouping and
    better organization of GUI elements within the Tkinter engine
    """

    def __init__(self):
        super().__init__()
        self.board.title("Interactive Drawing Application - tkinter")
        self.pen_width = 1
        self.pen_color = "black"

    def show_canvas(self):
        """
        Displays canvas and method allows more control over displaying it
        """
        self.canvas.pack(pady=20)
        self.pack()
        self.mainloop()

    def select_pen(self, new_width, new_color):
        self.pen_width = new_width
        self.pen_color = new_color

    def start_draw(self):
        pass

    def draw_line(self, direction, distance):
        """
        Draws line by adding method argument value onto
        base value for both co-ords
        """
        destination_x = direction[0] * distance
        destination_y = direction[1] * distance

        initial_x = self.start_x
        initial_y = self.start_y
        self.start_x += destination_x
        self.start_y += destination_y
        self.canvas.create_line(initial_x, initial_y, self.start_x,
                                self.start_y, width=self.pen_width,
                                fill=self.pen_color)


class TurtleDrawer(Board):
    """
    Turtle.py class which sets and groups turtle
    properties and fields together
    """

    def __init__(self):
        super().__init__()
        self.board.title("Interactive Drawing Application - turtle")
        self.t = turtle.RawTurtle(self.canvas)
        self.t.pensize(1)
        self.pen_color = "black"
        self.distance_multiplier = 20
        self.turtle_headings = {"N": 90,
                                "S": 270,
                                "E": 360,
                                "W": 180}

    def select_pen(self, new_width, new_color):
        self.t.pensize(new_width)
        self.t.pencolor(new_color)

    def start_draw(self):
        self.t.pendown()

    def show_canvas(self):
        self.t.penup()

        self.canvas.pack(pady=20)
        self.pack()
        self.mainloop()

    def draw_line(self, direction, distance):
        """
        Turtle graphics drawing uses headings instead of exact coordinates.
        This method evaluates data from parser and converts them
        into headings
        """
        if direction[1] < 0:
            heading = "N"
        elif direction[1] > 0:
            heading = "S"
        elif direction[0] < 0:
            heading = "W"
        else:
            heading = "E"

        turtle_heading = self.turtle_headings[heading]
        self.t.setheading(turtle_heading)
        self.t.forward(self.distance_multiplier * distance)


class PygameDrawer(Board):
    """
    Class for pygame engine and related modules
    """

    def __init__(self):
        pygame.init()
        self.screen_width = 500
        self.screen_height = 500
        self.start_x = self.screen_width / 2
        self.start_y = self.screen_height / 2
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.screen.fill("white")
        self.pen_width = 1
        self.pen_color = (0, 0, 0)

    def show_canvas(self):
        pass

    def select_pen(self, new_width, new_color):
        self.pen_width = new_width
        self.pen_color = new_color

    def start_draw(self):
        pass

    def draw_line(self, direction, distance):
        """
        Draws line by adding method argument value onto
        base value for both co-ords
        """
        destination_x = direction[0] * distance
        destination_y = direction[1] * distance

        initial_x = self.start_x
        initial_y = self.start_y
        self.start_x += destination_x
        self.start_y += destination_y
        start_pos = (initial_x, initial_y)
        destination_pos = (self.start_x, self.start_y)

        pygame.draw.line(self.screen, self.pen_color,
                         start_pos, destination_pos, self.pen_width)
        pygame.display.update()

        # allows closing of pygame window
        # will crash upon attempting to exit without loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
