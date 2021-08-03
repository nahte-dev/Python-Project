def write_file():
    """
    Writes commands to a file for piping into application
    """
    # hard coded content to write - could implement
    # dynamic file writing in another iteration
    instruction = ["N 5\n", "W 10\n", "S 5\n", "E 10\n"]

    with open('pipe.txt', 'w') as writer:
        writer.writelines(instruction)
