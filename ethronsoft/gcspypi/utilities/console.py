from __future__ import print_function
from ethronsoft.gcspypi.exceptions import *
from colorama import Fore, Back, Style, init
import traceback
import sys


class Console(object):
    """Helper class to do I/O with command line
    """

    def __init__(self, verbose=False, exit_on_error=True):
        self._verbose = verbose
        self._exit_on_error = exit_on_error

    def info(self, msg, end="\n"):
        """writes an info message to the console. 
           using an `end`="\r" allows the message to be overwritten.
        
        Arguments:
            msg {str} -- message to write
        
        Keyword Arguments:
            end {str} -- end sequence for message (default: {"\n"})
        
        Returns:
            str -- formatted message to be written
        """

        formatted = "{}{}".format(msg, end)
        sys.stderr.write(formatted)
        sys.stderr.flush()
        return formatted
        # print("{}".format(msg), end=end)

    def error(self, msg):
        """writes an error message to the console. 
        
        Arguments:
            msg {str} -- message to write
        
        Returns:
            str -- formatted message to be written
        """
        formatted = "{}".format(msg)
        print(formatted, file=sys.stderr)

    def warning(self, msg):
        """writes an warning message to the console. 
        
        Arguments:
            msg {str} -- message to write
        
        Returns:
            str -- formatted message to be written
        """
        formatted = "{}".format(msg)
        print(formatted.format(msg), file=sys.stderr)

    def output(self, msg):
        """writes an output message to the console. 
           Compared to to Console.info, this method does 
           not format the message in any way. It is also
           the only Console method to write to stdout. This is 
           so that outputs may easily be separated from any other
           cpm message and easily parsed 
        
        Arguments:
            msg {str} -- message to output
        """

        print(msg)

    def input(self, msg, default_value):
        """prints message `msg` and waits user to type in some input.
           If the input is empty, the `default_value` is used
        
        Arguments:
            msg {str} -- the message to show the user
            default_value {object} -- the default input to use if user does not provide any input
        
        Returns:
            str -- the user input
        """

        formatted = "{}{}: ".format(msg, "({})".format(default_value) if default_value else "")
        sys.stderr.write(formatted)
        line = sys.stdin.readline().strip()
        return line if line else default_value            

    def selection(self, msg, options):
        """displays `msg` to user and waits for the user to type in one of the outputs
        
        Arguments:
            msg {str} -- the message to show the user
            options {list} -- options the user can choose from
        
        Returns:
            str -- the chosen option
        """

        line = ""
        while line not in options:
            sys.stderr.write("{} [{}]: ".format(msg, "|".join(options)))
            line = sys.stdin.readline()
            line = line.strip()
        return line
    
    def blank(self, pending):
        """used in conjuction with info(msg, end="\r"), to clear the 
           line before overwriting it with another message.
           blank takes in a message and writes as many white spaces as 
           the characters in that message, effectively clearing out the 
           previous message.
        
        Arguments:
            pending {str} -- the last message written to console.
        """

        self.info(" " * len(pending), end="\r")

    def badge(self, msg, status, overwrite=False):
        """print a badge to the console
        
        Arguments:
            msg {str} -- badge message
            status {str} -- badge status [danger|warning|danger]. Determines the color of the badge
        
        Keyword Arguments:
            overwrite {bool} -- whether or not this badge can be overwritten (default: {False})
        
        Returns:
            str -- the formatted string representing the badge printed to the console
        """

        if status == "danger":
            return self.info(Style.RESET_ALL + Back.RED + " {} ".format(msg) + Style.RESET_ALL, end="\n" if not overwrite else "\r")
        elif status == "warning":
            return self.info(Style.RESET_ALL + Back.YELLOW + Fore.BLACK + " {} ".format(msg) + Style.RESET_ALL, end="\n" if not overwrite else "\r")
        elif status == "success":
            return self.info(Style.RESET_ALL + Back.GREEN + " {} ".format(msg) + Style.RESET_ALL, end="\n" if not overwrite else "\r")

    def __enter__(self):
        return self

    def __exit__(self, typ, value, tb):
        def _print(header):
            if self._verbose:
                self.error(Style.RESET_ALL + Fore.RED + header + Style.RESET_ALL + " {}\n{}".format(
                    value if value else value.__cause__,
                    "".join(traceback.format_exception(typ, value, tb))
                ))
            else:
                self.error(Style.RESET_ALL + Fore.RED + header +
                           Style.RESET_ALL + " {}".format(value if value else value.__cause__))
        if isinstance(value, InvalidParameter):
            _print("invalid parameter:")
        elif isinstance(value, InvalidState):
            _print("invalid state:")
        elif isinstance(value, NotFound):
            _print("boundary error:")
        elif isinstance(value, RepositoryError):
            _print("repository error:")
        elif isinstance(value, ScriptError):
            _print("script error:")
        elif isinstance(value, Exception):
            _print("error:")

        if value and self._exit_on_error: #pragma: no cover
            sys.exit(1)
