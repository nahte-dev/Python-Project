"""
This module is for the command line interface (CLI) and
allows for dynamic creation and improving commands
"""

import cmd
import sys
import tigrextended
from piper import write_file


class View(cmd.Cmd):
    """
    Command Line Interface class. Defines all commands and their functionality.

    Prints all commands entered for testing purposes and for seeing
    what drawings have already been made
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = "Welcome to a interactive drawing application!"
        self.prompt = "Cmd >> "
        self.command_list = []
        self.is_pen_down = 0
        self.source_reader = ""

    def do_engine(self, line):
        """
        Allows selection of which graphical engine/package the
        output will be drawn to
        """
        command = "G"

        formatted_line = line.lower()
        cmd_input = [(command, formatted_line)]
        print(cmd_input)
        self.command_list.append(cmd_input)

    def do_pen(self, line):
        """
        Allows selection of pen width and other properties
        """
        command = "P"

        formatted_line = line.lower()
        cmd_input = [(command, formatted_line)]
        print(cmd_input)
        self.command_list.append(cmd_input)

    def help_pen(self):
        print("\n")
        print("Allows you to change width of pen")
        print("Adding switch '-c' allows you change color")
        print("Syntax: pen 5")
        print("Syntax: pen 5 -c 2")
        print("1 - black")
        print("2 - red")
        print("3 - blue")

    def do_pen_down(self, line):
        """
        Activates drawing mode
        """
        command = "D"

        self.is_pen_down = 1
        cmd_input = [(command, 0)]
        print(cmd_input)
        self.command_list.append(cmd_input)

    def help_pen_down(self):
        print("\n")
        print("Activates drawing mode (not case sensitive)")
        print("Shortcut: d")
        print("Syntax: d")

    def do_draw(self, line):
        """
        Command takes a direction (N, S) and a number for distance (5, 10)
        and then sends that command through to the source reader
        which then parses the commands - will check if pen down
        flag is true or not
        """
        # checks if pen is already down and if not, restarts the command line
        if self.is_pen_down == 0:
            print("You must place pen down first")
            self.loop()
        else:
            draw_request = line.strip().split()

            direction = draw_request[0].upper()
            distance = draw_request[1]
            cmd_input = [(direction, distance)]
            print(cmd_input)
            self.command_list.append(cmd_input)

    def help_draw(self):
        print("\n")
        print("Draws lines relative to input on direction and distance")
        print("Syntax: draw N 5")
        print("draw E 5")

    def do_pen_up(self, line):
        """
        Finalizes the command inputs and sends the commands to the
        source reader and graphics engine and displays the
        canvas with the drawn shape
        """
        command = "U"

        cmd_input = [(command, 0)]
        print(cmd_input)
        self.command_list.append(cmd_input)
        self.source_reader = tigrextended.SourceReader(self.command_list)
        # resets the command list after sending to source reader
        self.command_list = []
        self.is_pen_down = 0
        self.source_reader.go()

    def help_pen_up(self):
        print("\n")
        print("Finishes drawing and displays canvas (not case sensitive)")
        print("Shortcuts: u")
        print("Syntax: u")

    def do_import_file(self, line):
        """
        Imports a file that has pre-written commands for
        drawing objects i.e. a square
        """
        # if command is called with a file name
        if line != "":
            with open(line, "r") as reader:
                for line in reader:
                    print(line, end="")
                    # calls draw command to
                    # parse commands in same format
                    self.do_draw(line)
        else:
            # calls a piping script to write
            # to a file
            try:
                write_file()
                with open("pipe.txt", "r+") as reader:
                    for line in reader:
                        print(line, end="")
                        self.do_draw(line)
                    # deletes contents of file for writing again
                    reader.truncate(0)
            except FileNotFoundError as fnf_error:
                print(fnf_error)

    def do_exit(self, line):
        """ Exits the CLI """
        return 1

    def help_exit(self):
        print("\n")
        print("Exits the command line")
        print("Syntax: exit")

    def loop(self):
        """
        Begins the command prompt
        """
        cmd.Cmd.cmdloop(self)

    # shortcuts for longer/complicated commands
    do_u = do_pen_up
    do_d = do_pen_down
    do_g = do_engine
    do_import = do_import_file
