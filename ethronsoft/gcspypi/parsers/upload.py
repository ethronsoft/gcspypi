from ethronsoft.gcspypi.package.package_manager import PackageManager, PackageBuilder
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository
import os

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c, overwrite=data["overwrite"])
        pkg = PackageBuilder(os.path.abspath(data["file"])).build()
        c.info("uploading {}...".format(str(pkg)))
        pkg_mgr.upload(pkg, os.path.abspath(data["file"]))
        c.badge("uploaded", "success")

class UploadParser(object):

    def __init__(self, subparsers):
        self.name = "upload"
        updload_parser = subparsers.add_parser(self.name,
                                           description="Upload a package built by setup.py as either source or wheel")
        updload_parser.add_argument("file", metavar="FILE", type=str, help="Package to upload")
        updload_parser.add_argument("-o", "--overwrite", nargs="?", const=True, default=False, type=bool,
                                    help="Overwrites an existing package if user has delete permission on the GCS repository")

    def handle(self, config, data):
        handle_(config, data)