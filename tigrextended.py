import tigr
import cli
import guiengine


def _test():
    """
    Function to call doc testing when required instead of in main

    >>> v = cli.View()

    Test: Testing with tkinter engine
    >>> v.do_engine('tkinter')
    ...
    [('G', 'tkinter')]

    >>> v.do_pen('pen 5')
    ...
    [('P', 'pen 5')]

    >>> v.do_pen('pen 5 -c 2')
    ...
    [('P', 'pen 5 -c 2')]

    >>> v.do_pen_down('D 0')
    ...
    [('D', 0)]

    >>> v.do_draw('N 5')
    ...
    [('N', '5')]

    >>> v.do_draw('E 5')
    ...
    [('E', '5')]

    >>> v.do_draw('S 5')
    ...
    [('S', '5')]

    >>> v.do_draw('W 5')
    ...
    [('W', '5')]

    >>> v.do_pen_up('U 0')
    ...
    [('U', 0)]
    Unknown argument
    Unknown argument

    Test: Testing with turtle engine
    >>> v.do_engine('turtle')
    ...
    [('G', 'turtle')]

    >>> v.do_pen('pen 5')
    ...
    [('P', 'pen 5')]

    >>> v.do_pen('pen 5 -c 2')
    ...
    [('P', 'pen 5 -c 2')]

    >>> v.do_pen_down('D 0')
    ...
    [('D', 0)]

    >>> v.do_draw('N 10')
    ...
    [('N', '10')]

    >>> v.do_draw('E 10')
    ...
    [('E', '10')]

    >>> v.do_draw('S 10')
    ...
    [('S', '10')]

    >>> v.do_draw('W 10')
    ...
    [('W', '10')]

    >>> v.do_pen_up('U 0')
    ...
    [('U', 0)]
    Unknown argument
    Unknown argument
    """
    import doctest
    doctest.testmod(verbose=True)


class Drawer(tigr.Drawer):
    def __init__(self, the_engine):
        self.engines = {"tkinter": guiengine.TkinterDrawer(),
                        "turtle": guiengine.TurtleDrawer(),
                        "pygame": guiengine.PygameDrawer()
                        }
        self.__set_engine(the_engine)

    def __set_engine(self, engine):
        """
        Method sets the value of the engines dictionary to the gfx_engine
        field so the engine collection can be expanded easily
        """
        try:
            self.gfx_engine = self.engines[engine]
        except KeyError as invalid_engine_err:
            print(invalid_engine_err)
            print("Invalid engine - please choose tkinter, turtle or pygame")
        finally:
            self.gfx_engine = self.engines[engine]

    def select_pen(self, pen_width=1, pen_color="black"):
        self.gfx_engine.select_pen(pen_width, pen_color)

    def draw_line(self, direction, distance):
        self.gfx_engine.draw_line(direction, distance)

    def pen_down(self):
        self.gfx_engine.start_draw()

    # once drawing has finished, the canvas is displayed
    def pen_up(self):
        self.gfx_engine.show_canvas()


class Parser(tigr.Parser):
    """
    Essentially a controller (in a MVC format) for the drawer, command line
    and the graphics engine
    """
    # coordinate data for which direction to go
    direction_data = {"N": [0, -25], "S": [0, 25], "E": [25, 0], "W": [-25, 0]}

    def __init__(self):
        self.command = ""
        self.source = []
        self.data = 0
        # list of Parser methods based on CLI input
        self.command_list = {"U": self.__pen_up,
                             "N": self.__create_line,
                             "S": self.__create_line,
                             "E": self.__create_line,
                             "W": self.__create_line,
                             "D": self.__pen_down,
                             "P": self.__select_pen,
                             "G": self.__set_engine}

    def parse(self, raw_source):
        """
        Separates two elements, command and data type from a list
        which then calls a method based on a key/value
        dictionary defined in the constructor
        """
        self.source = raw_source

        for line in self.source:
            self.command = line[0][0]
            self.data = line[0][1]
            self.command_list[self.command](self.data)

    def __set_engine(self, data):
        self.drawer = Drawer(data)

    def __pen_up(self, data):
        self.drawer.pen_up()

    def __create_line(self, data):
        """
        Method that calls the drawer draw_line method
        """
        self.drawer.draw_line(self.direction_data[self.command],
                              (int(self.data)))

    def __pen_down(self, data):
        self.drawer.pen_down()

    def __select_pen(self, data):
        pen_colors = {"1": "black",
                      "2": "red",
                      "3": "blue"}
        pen_args = {"-c": pen_colors}

        pen_request = data.strip().split()
        pen_width = int(pen_request[0])

        # calls select pen method in drawer and passes
        # arg value if found, otherwise just passes width
        if len(pen_request) > 1:
            try:
                if pen_request[1] in pen_args:
                    arg = pen_request[1]
                    arg_value = pen_request[2]
                    pen_arg = pen_args[arg][arg_value]

                    self.drawer.select_pen(pen_width, pen_arg)
            except KeyError:
                raise Exception("Invalid color - please choose 1, 2 or 3 "
                                "for black, red or blue respectively")
        else:
            self.drawer.select_pen(pen_width)


class SourceReader(tigr.SourceReader):
    def __init__(self, new_source):
        self.source = new_source
        self.parser = Parser()

    def go(self):
        self.parser.parse(self.source)


def main():
    """
    Function for instantiating classes and calling their
    methods - much tidier than the system method
    __main__
    """
    view = cli.View()
    view.loop()


if __name__ == "__main__":
    # _test()

    main()
