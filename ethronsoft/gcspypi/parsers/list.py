class ListParser(object):

    def __init__(self, subparsers):
        self.name = "list"
        list_parser = subparsers.add_parser(self.name,
                                        description="""Displays all versions of a certain package
                                        or all content of the repository if package name is omitted""")
        list_parser.add_argument("package", nargs="?", default="", help="Package Name")

    def handle(self, config, data):
        pass