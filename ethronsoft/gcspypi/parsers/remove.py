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

    def handle(self, config, data):
        pass