class UninstallParser(object):

    def __init__(self, subparsers):
        self.name = "uninstall"
        uninstall_parser = subparsers.add_parser(self.name, description="Uninstall a local package")
        uninstall_parser.add_argument("packages", metavar="P", nargs="*", type=str, help="Package(s) to uninstall")

    def handle(self, config, data):
        pass