from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c)
        for syntax in data["syntax"]:
            pkg = pkg_mgr.search(syntax)
            if pkg:
                c.output(pkg)

class SearchParser(object):

    def __init__(self, subparsers):
        self.name = "search"
        seach_parser = subparsers.add_parser(self.name,
                                         description="Search for packages in the GCS repository. View syntax using command syntax")
        seach_parser.add_argument("syntax", nargs="+", help="Search syntax")

    def handle(self, config, data):
        handle_(config, data)