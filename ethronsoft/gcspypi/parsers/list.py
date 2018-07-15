from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c)
        for path in sorted(pkg_mgr.list_items(data["package"], from_cache=True)):
            c.output(path.split("/")[-1])

class ListParser(object):

    def __init__(self, subparsers):
        self.name = "list"
        list_parser = subparsers.add_parser(self.name,
                                        description="""Displays all versions of a certain package
                                        or all content of the repository if package name is omitted""")
        list_parser.add_argument("package", nargs="?", default="", help="Package Name")

    def handle(self, config, data):
        handle_(config, data)