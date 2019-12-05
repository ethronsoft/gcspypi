from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo,
                                 console=c,
                                 installer=None,
                                 is_python3=config.get("python3", False),
                                 mirroring=data["mirror"],
                                 install_deps=not data["no_dependencies"])
        if data["requirements"]:
            c.info("installing from requirements file...")
            for syntax in open(data["requirements"], "r").readlines():
                c.info("installing {}".format(syntax))
                pkg_mgr.install(syntax, data["type"], data["no_user"])
        else:
            for syntax in data["packages"]:
                c.info("installing {}".format(syntax))
                pkg_mgr.install(syntax, data["type"], data["no_user"])

class InstallParser(object):

    def __init__(self, subparsers):
        self.name = "install"
        install_parser = subparsers.add_parser(self.name,
                                           description="""Downloads a package from the GCS repository,
                                      (or pypi index if mirroring is enabled) and installs it locally""")
        install_parser.add_argument("packages", metavar="P", nargs="*", type=str,
                                    help="Package(s) to install. View syntax using command syntax")
        install_parser.add_argument("-r", "--requirements", metavar="F", nargs="?", default=None, type=str,
                                    help="Dependencies to install, provided in a requirements.txt file.")
        install_parser.add_argument("-m", "--mirror", nargs="?", default=True, type=bool,
                                    help="""If package to install is not found
                                                    in the GCS repository, attempts to
                                                    use pip install, using the global configuration""")
        install_parser.add_argument("-nd", "--no-dependencies", nargs="?", default=False, type=bool,
                                    help="""Omit downloading package dependencies""")
        install_parser.add_argument("-t", "--type", nargs="?", default="SOURCE", choices=['SOURCE', 'WHEEL'])
        install_parser.add_argument("--no-user", default=False, const=True, nargs="?", type=bool, help="do not use option --user when installing a package via `pip install`")

    def handle(self, config, data):
        handle_(config, data)