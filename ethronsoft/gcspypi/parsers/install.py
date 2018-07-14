class InstallParser(object):

    def __init__(self, subparsers):
        self.name = "install"
        install_parser = subparsers.add_parser(self.name,
                                           description="""Downloads a package from the GCS repository,
                                      (or pypi index if mirroring is enabled) and installs it locally""")
        install_parser.add_argument("packages", metavar="P", nargs="*", type=str,
                                    help="Package(s) to install. View syntax using command syntax")
        install_parser.add_argument("-r", "--requirements", metavar="F", nargs="?", default=None, type=str,
                                    help="Additional requirements to install, provided in a requirements.txt file.")
        install_parser.add_argument("-m", "--mirror", nargs="?", default=True, type=bool,
                                    help="""If package to install is not found
                                                    in the GCS repository, attempts to
                                                    use pip install, using the global configuration""")
        install_parser.add_argument("-nd", "--no-dependencies", nargs="?", default=False, type=bool,
                                    help="""Omit downloading package dependencies""")
        install_parser.add_argument("-t", "--type", nargs="?", default="SOURCE", choices=['SOURCE', 'WHEEL'])
        install_parser.add_argument("--no-user", default=False, const=True, nargs="?", type=bool, help="do not use option --user when installing a package via `pip install`")

    def handle(self, config, data):
        pass