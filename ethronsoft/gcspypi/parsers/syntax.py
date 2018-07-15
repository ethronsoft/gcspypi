from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def print_syntax(console):
    console.info("""
Syntax:
    ((?:\w|-)*)(==|<=?|>=?)?((?:\d*\.?){0,3})?,?(==|<=?|>=?)?((?:\d*\.?){0,3})?

Example:
    1) Refer to package 'abc' with version == 1.0.0
            abc==1.0.0
    2) Refer to package 'abc' with version  > 1.0.0
            abc>1.0.0
    3) Refer to package 'abc' with version <= 1.0.0
            abc<=1.0.0
    4) Refer to package 'abc' with version within a range.
       Selects the first match from the range lower bound
            abc>1.0.0,<=1.2.0
    5) Refer to last version of package 'abc'
            abc
    6) Refer to last version of all packages
            [empty]
    7) Refer to every version of all packages
            >0.0.0

Note: a 0 may be omitted in specifying the version if followed by zeros
    i.e.
        > would be equivalent to >0.0.0
        1 would be equivalent to 1.0.0
        1.1 would be equivalent to 1.1.0
""")

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        print_syntax(c)
        
class SyntaxParser(object):

    def __init__(self, subparsers):
        self.name = "syntax"
        subparsers.add_parser(self.name, description="Describes syntax used in search and remove commands")

    def handle(self, config, data):
        handle_(config, data)