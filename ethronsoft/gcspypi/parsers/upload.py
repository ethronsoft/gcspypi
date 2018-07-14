class UploadParser(object):

    def __init__(self, subparsers):
        self.name = "upload"
        updload_parser = subparsers.add_parser(self.name,
                                           description="Upload a package built by setup.py as either source or wheel")
        updload_parser.add_argument("file", metavar="FILE", type=str, help="Package to upload")
        updload_parser.add_argument("-o", "--overwrite", nargs="?", const=True, default=False, type=bool,
                                    help="Overwrites an existing package if user has delete permission on the GCS repository")

    def handle(self, config, data):
        pass