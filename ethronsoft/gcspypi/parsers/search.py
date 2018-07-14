class SearchParser(object):

    def __init__(self, subparsers):
        self.name = "search"
        seach_parser = subparsers.add_parser(self.name,
                                         description="Search for packages in the GCS repository. View syntax using command syntax")
        seach_parser.add_argument("syntax", nargs="+", help="Search syntax")

    def handle(self, config, data):
        pass