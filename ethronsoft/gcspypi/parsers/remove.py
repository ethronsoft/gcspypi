from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c)
        for syntax in data["packages"]:
            pkg = pkg_mgr.search(syntax)
            ok = pkg is not None
            if ok:
                ok = pkg_mgr.remove(pkg, interactive=not data["non_interactive"])
            if ok:
                c.badge("removed", "success")

class RemoveParser(object):

    def __init__(self, subparsers):
        self.name = "remove"
        remove_parser = subparsers.add_parser(self.name,
                                          description="""Removes packages from the GCS if user has delete permission
                                                        on the GCS repository. WARNING: Once executed,
                                                        this command cannot be undone if not by reinstalling
                                                        the packages. View syntax using command syntax""")
        remove_parser.add_argument("packages", metavar="P", nargs="+", type=str,
                               help="Package(s) to remove. View syntax using command syntax")

        remove_parser.add_argument("--non-interactive", "-ni", action="store_true", default=False,
                               help="Interactive Mode")

    def handle(self, config, data):
        handle_(config, data)