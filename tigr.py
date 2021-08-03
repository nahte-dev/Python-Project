""" Tiny Interpreted GRaphic = TIGR
Keep the interfaces defined below in your work.
The implementation should be replaced,
by more flexible, portable and extensible solutions. """


class Drawer:
    """ Responsible for defining an interface for drawing """

    def __init__(self):
        pass

    def select_pen(self, pen_num):
        print(f'Selected pen {pen_num}')

    def pen_down(self):
        print('pen down')

    def pen_up(self):
        print('pen up')

    def draw_line(self, direction, distance):
        print(f'drawing line of length {distance} at {direction}')


class Parser:
    def __init__(self):
        self.drawer = Drawer()
        self.source = []
        self.command = ""
        self.data = 0

    def parse(self, raw_source):
        """ hard coded parsing like this is a Bad Thing!
            It is inflexible and has no error checking """
        self.source = raw_source
        for line in self.source:
            self.command = line[0]
            if line[2].isdigit():
                self.data = int(line[2])
            else:
                self.data = 0
            if self.command == 'P':
                self.drawer.select_pen(self.data)
            if self.command == 'D':
                self.drawer.pen_down()
            if self.command == 'N':
                self.drawer.draw_line(0, self.data)
            if self.command == 'E':
                self.drawer.draw_line(90, self.data)
            if self.command == 'S':
                self.drawer.draw_line(180, self.data)
            if self.command == 'W':
                self.drawer.draw_line(270, self.data)
            if self.command == 'U':
                self.drawer.pen_up()


class SourceReader:
    """ responsible for providing source text for parsing and drawing
        Initiates the Draw use-case.
        Links to a parser and passes the source text onwards """

    def __init__(self):
        self.parser = Parser()
        self.source = []

    def go(self):
        self.source.append('P 2 # select pen 2')
        self.source.append('D	# pen down')
        self.source.append('W 2	# draw west 2cm')
        self.source.append('N 1	# then north 1')
        self.source.append('E 2	# then east 2')
        self.source.append(' S  12.7 ')
        self.source.append(' U	# pen up')
        self.parser.parse(self.source)


if __name__ == "__main__":
    s = SourceReader()
    s.go()
