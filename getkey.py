# source : https://code.activestate.com/recipes/134892/
import os.path

SEQUENCE_FILE_NAME = "sequence.txt"

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        if os.path.isfile(SEQUENCE_FILE_NAME):
            abs_path = os.path.abspath(SEQUENCE_FILE_NAME)
            print("!! TEST MODE ACTIVATED: Will use", abs_path, "for input. Remove this file to use keyboard input !!")
            self.impl = _GetchTest()
        else:
            try:
                self.impl = _GetchWindows()
            except ImportError:
                self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchTest:
    def __init__(self):
        with open(SEQUENCE_FILE_NAME, 'r') as f:
            self.sequence = f.read().splitlines()

    def __call__(self):
        try:
            return self.sequence.pop(0)
        except IndexError:
            raise IOError("Sequence file is empty")


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch1 = sys.stdin.read(1)
            # Handle the arrow keys
            if ch1 == '\x1b':  # ESC
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':
                        return 'UP'
                    if ch3 == 'B':
                        return 'DOWN'
                    if ch3 == 'C':
                        return 'RIGHT'
                    if ch3 == 'D':
                        return 'LEFT'
                else:
                    return 'ESCAPE'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch1


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        from msvcrt import getch
        ch1 = getch()
        if ch1 in (b'\x00', b'\xe0'):
            ch2 = getch()
            print(ch2)
            if ch2 == b'H':
                return 'UP'
            elif ch2 == b'P':
                return 'DOWN'
            elif ch2 == b'M':
                return 'RIGHT'
            elif ch2 == b'K':
                return 'LEFT'
        elif ch1 == b'\x1b':
            return 'ESCAPE'
        return str(ch1, 'utf-8')


getkey = _Getch()
