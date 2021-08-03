import unittest
import tigrextended
import guiengine
import cli
# Some testing cases and layout
# inspired from Greg's previous example


class CLITestCase(unittest.TestCase):
    # Tests related to commands in the command interface
    # and the commands appending the list correctly
    def setUp(self):
        self.command_list = []
        self.is_pen_down = 0

    def test_select_tkinter(self):
        command = "G"
        line = "tkinter"
        formatted_line = line.lower()
        cmd_input = [(command, formatted_line)]
        self.command_list.append(cmd_input)

        self.assertEqual(cmd_input, [('G', 'tkinter')])
        self.assertIn(cmd_input, self.command_list)

    def test_select_turtle(self):
        command = "G"
        line = "turtle"
        formatted_line = line.lower()
        cmd_input = [(command, formatted_line)]
        self.command_list.append(cmd_input)

        self.assertEqual(cmd_input, [('G', 'turtle')])
        self.assertIn(cmd_input, self.command_list)

    def test_select_pygame(self):
        command = "G"
        line = "pygame"
        formatted_line = line.lower()
        cmd_input = [(command, formatted_line)]
        self.command_list.append(cmd_input)

        self.assertEqual(cmd_input, [('G', 'pygame')])
        self.assertIn(cmd_input, self.command_list)

    def test_is_pen_down_false(self):
        command = "D"
        expected = False
        actual = self.is_pen_down
        cmd_input = [(command, 0)]
        self.command_list.append(cmd_input)

        self.assertEqual(expected, actual, "You must place pen down first")
        self.assertIn(cmd_input, self.command_list)

    def test_is_pen_down(self):
        command = "D"
        expected = True
        self.is_pen_down = 1
        actual = self.is_pen_down
        cmd_input = [(command, 0)]
        self.command_list.append(cmd_input)

        self.assertEqual(expected, actual, "You must place pen down first")
        self.assertIn(cmd_input, self.command_list)

    def test_select_pen_width(self):
        command = "P"
        line = "5"
        cmd_input = [(command, line)]
        self.command_list.append(cmd_input)

        self.assertEqual(cmd_input, [("P", "5")])
        self.assertIn(cmd_input, self.command_list)

    def test_select_pen_width_and_color(self):
        command = "P"
        line = "5 -c 2"
        cmd_input = [(command, line)]
        self.command_list.append(cmd_input)

        self.assertEqual(cmd_input, [("P", "5 -c 2")])
        self.assertIn(cmd_input, self.command_list)

    def test_draw(self):
        command = "N 5"
        draw_request = command.strip().split()
        direction = draw_request[0].upper()
        distance = draw_request[1]

        expected_direction = "N"
        actual_direction = direction

        expected_distance = "5"
        actual_distance = distance

        self.assertEqual(expected_direction,
                         actual_direction, "Direction is invalid")
        self.assertEqual(expected_distance,
                         actual_distance, "Distance is invalid")

    def test_draw_with_invalid_direction(self):
        command = "NW 10"
        draw_request = command.strip().split()
        direction = draw_request[0].upper()
        distance = draw_request[1]

        expected_direction = "N"
        actual_direction = direction

        expected_distance = "10"
        actual_distance = distance

        self.assertNotEqual(expected_direction,
                            actual_direction, "Direction is invalid")
        self.assertEqual(expected_distance,
                         actual_distance, "Distance is invalid")


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.drawer = ""
        self.source_reader = tigrextended.SourceReader()

    def test_source_reader(self):
        source = ["N 5"]
        self.source_reader.go()

        for line in self.source_reader.source:
            self.assertEqual(source, line)

    def test_set_pen_width(self):
        data = "5"
        pen_request = data.strip().split()
        pen_width = pen_request[0]

        self.assertEqual(pen_width, "5")

    def test_set_pen_width_and_color(self):
        pen_colors = {"1": "black",
                      "2": "red",
                      "3": "blue"}
        pen_args = {"-c": pen_colors}

        data = "5 -c 3"
        pen_request = data.strip().split()
        arg = pen_request[1]
        arg_value = pen_request[2]
        pen_arg = pen_args[arg][arg_value]

        self.assertEqual(pen_arg, "blue")


class EngineTestCase(unittest.TestCase):
    # tests related to gui engines and selecting them
    def setUp(self):
        self.engines = {"tkinter": guiengine.TkinterDrawer(),
                        "turtle": guiengine.TurtleDrawer(),
                        "pygame": guiengine.PygameDrawer()
                        }

    def test_tkinter_engine(self):
        test_engine = "tkinter"
        gfx_engine = self.engines[test_engine]

        self.assertIsInstance(gfx_engine, guiengine.TkinterDrawer)

    def test_turtle_engine(self):
        test_engine = "turtle"
        gfx_engine = self.engines[test_engine]

        self.assertIsInstance(gfx_engine, guiengine.TurtleDrawer)

    def test_pygame_engine(self):
        test_engine = "pygame"
        gfx_engine = self.engines[test_engine]

        self.assertIsInstance(gfx_engine, guiengine.PygameDrawer)


def cli_test_suite():
    cli_suite = unittest.TestSuite()
    cli_suite.addTest(unittest.makeSuite(CLITestCase))
    return cli_suite


def gui_test_suite():
    gui_suite = unittest.TestSuite()
    gui_suite.addTest(unittest.makeSuite(EngineTestCase))
    return gui_suite


def parser_test_suite():
    parser_suite = unittest.TestSuite()
    parser_suite.addTest(unittest.makeSuite(ParserTestCase))
    return parser_suite


if __name__ == '__main__':
    # unittest.main()
    test_cli = cli_test_suite()
    test_gui = gui_test_suite()
    test_parser = parser_test_suite()

    runner = unittest.TextTestRunner()
    runner.run(test_cli)
    runner.run(test_gui)
    runner.run(test_parser)
