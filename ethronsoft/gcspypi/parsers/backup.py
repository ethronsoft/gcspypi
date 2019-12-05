from ethronsoft.gcspypi.package.package_manager import PackageManager,PackageInstaller
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.parsers.commons import init_repository

def handle_pull(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        is_python3 = config.get("python3", False)
        pkg_mgr = PackageManager(repo, console=c, installer=None, is_python3=config.get("python3", False))
        pkg_mgr.clone(data["destination"])

def handle_push(config, data):
    with Console(verbose=config.get("verbose", False), exit_on_error=True) as c:
        repo = init_repository(c, config["repository"])
        pkg_mgr = PackageManager(repo, console=c, installer=None, is_python3=config.get("python3", False))
        pkg_mgr.restore(data["zipped_repo"])

class BackupParser(object):

    def __init__(self, subparsers):
        self.name = "backup"
        backup_parser = subparsers.add_parser(self.name, description="Allows to backup and restore a repository")
        backup_subparser = backup_parser.add_subparsers(title="backup commands", help="use command --help for help", dest="sub_command")
        pull_parser = backup_subparser.add_parser("pull", description="Pulls the repository at the provided location")
        pull_parser.add_argument("destination", default=".", help="Directory to pull into")
        push_parser = backup_subparser.add_parser("push", description="Pushes the local copy of the repository to the repository")
        push_parser.add_argument("zipped_repo", help="Name o zipped repository to push")

    def handle(self, config, data):
        if data["sub_command"] == "pull":
            handle_pull(config, data)
        elif data["sub_command"] == "push":
            handle_push(config, data)