class DownloadParser(object):

    def __init__(self, subparsers):
        self.name = "download"
        download_parser = subparsers.add_parser(self.name,
                                           description="Download a package by the provided name")
        download_parser.add_argument("obj", metavar="FILE", type=str, help="Package to download")
        download_parser.add_argument("dir", default=".", type=str,
                                    help="directory where to download the file")

    def handle(self, config, data):
        pass