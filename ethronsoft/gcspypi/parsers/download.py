from ethronsoft.gcspypi.package.package_manager import PackageManager
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c)
        downloaded = pkg_mgr.download_by_name(data["obj"], data["dir"])
        c.info("Downloaded: {0}".format(downloaded))

class DownloadParser(object):

    def __init__(self, subparsers):
        self.name = "download"
        download_parser = subparsers.add_parser(self.name,
                                           description="Download a package by the provided name")
        download_parser.add_argument("obj", metavar="FILE", type=str, help="Package to download")
        download_parser.add_argument("dir", default=".", type=str,
                                    help="directory where to download the file")

    def handle(self, config, data):
        handle_(config, data)