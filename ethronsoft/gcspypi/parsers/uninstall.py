from ethronsoft.gcspypi.package.package_manager import PackageManager, Package
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c, installer=None, is_python3 = config.get("python3", False))
        for syntax in data["packages"]:
            pkg_mgr.uninstall(Package.from_text(syntax))

class UninstallParser(object):

    def __init__(self, subparsers):
        self.name = "uninstall"
        uninstall_parser = subparsers.add_parser(self.name, description="Uninstall a local package")
        uninstall_parser.add_argument("packages", metavar="P", nargs="*", type=str, help="Package(s) to uninstall")

    def handle(self, config, data):
        handle_(config, data)